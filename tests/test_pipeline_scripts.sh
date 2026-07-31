#!/usr/bin/env bash
set -Eeuo pipefail

REPO_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
REAL_PYTHON="$(command -v python3)"
TEST_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/ai-daily-pipeline-test.XXXXXX")"
TEST_DATE="2099-01-02"

cleanup() {
    if [ "${KEEP_TEST_ROOT:-0}" = "1" ]; then
        echo "test artifacts: $TEST_ROOT" >&2
    else
        rm -rf -- "$TEST_ROOT"
    fi
}
trap cleanup EXIT

fail() {
    echo "FAIL: $*" >&2
    exit 1
}

new_project() {
    local name="$1"
    local project="$TEST_ROOT/$name"
    mkdir -p "$project/archive/manifests" "$project/logs" "$project/bin"
    cp "$REPO_DIR/run.sh" "$REPO_DIR/catchup.sh" \
        "$REPO_DIR/pipeline_manifest.py" "$REPO_DIR/pipeline_notify.py" \
        "$project/"
    cp "$REPO_DIR/tests/fixtures/pipeline_python_stub.sh" "$project/bin/python-stub"
    cp "$REPO_DIR/tests/fixtures/pipeline_git_stub.sh" "$project/bin/git-stub"
    chmod +x "$project/run.sh" "$project/catchup.sh" \
        "$project/bin/python-stub" "$project/bin/git-stub"
    : >"$project/empty.env"
    printf '%s\n' "$project"
}

run_pipeline() {
    local project="$1"
    shift
    env \
        AI_DAILY_NEWS_DIR="$project" \
        MANIFEST_DIR="$project/archive/manifests" \
        PIPELINE_LOCK_DIR="$project/pipeline.lock" \
        PIPELINE_ENV_FILE="$project/empty.env" \
        PYTHON_BIN="$project/bin/python-stub" \
        GIT_BIN="$project/bin/git-stub" \
        MINIMAX_API_KEY="offline-test-key" \
        REAL_PYTHON="$REAL_PYTHON" \
        CALL_LOG="$project/calls.log" \
        "$@" \
        "$project/run.sh" "$TEST_DATE"
}

assert_manifest_status() {
    local project="$1"
    local status="$2"
    "$REAL_PYTHON" "$project/pipeline_manifest.py" check \
        --path "$project/archive/manifests/$TEST_DATE.json" \
        --date "$TEST_DATE" \
        --status "$status" ||
        fail "expected manifest status $status in $project"
}

make_ready_project() {
    local project="$1"
    printf '# report\n' >"$project/daily-ai-news-$TEST_DATE.md"
    printf '<html>report</html>\n' >"$project/daily-ai-news-$TEST_DATE.html"
    printf '<html>index</html>\n' >"$project/index.html"
    printf '{"date":"%s","count":1,"articles":[{}]}\n' "$TEST_DATE" \
        >"$project/archive/news_$TEST_DATE.json"
    "$REAL_PYTHON" -c \
        'import hashlib,json,pathlib,sys; manifest,date,md_path,archive_path,html_path=map(pathlib.Path,[sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]]); archive=json.loads(archive_path.read_text()); digest=hashlib.sha256(); digest.update(md_path.read_text().encode()); digest.update(json.dumps(archive,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()); digest.update(html_path.read_bytes()); manifest.write_text(json.dumps({"date": str(date), "status": "ready", "run_id": "resume-run", "content_hash": digest.hexdigest(), "artifacts": {"markdown": str(md_path), "archive": str(archive_path), "html": str(html_path)}, "qa": {"blockers": 0}}), encoding="utf-8")' \
        "$project/archive/manifests/$TEST_DATE.json" "$TEST_DATE" \
        "$project/daily-ai-news-$TEST_DATE.md" \
        "$project/archive/news_$TEST_DATE.json" \
        "$project/daily-ai-news-$TEST_DATE.html"
}

echo "1/9 generation failure stops every publish side effect"
project="$(new_project generation_failure)"
set +e
run_pipeline "$project" STUB_FEED_RC=42 >"$project/output.log" 2>&1
rc=$?
set -e
[ "$rc" -eq 42 ] || fail "generation failure returned $rc instead of 42"
assert_manifest_status "$project" running
if [ -e "$project/calls.log" ] && grep -Eq '^(screenshot|git) ' "$project/calls.log"; then
    fail "publish side effect ran after feed failure"
fi

echo "2/9 successful run preserves ready metadata and marks published"
project="$(new_project successful)"
run_pipeline "$project" >"$project/output.log" 2>&1
assert_manifest_status "$project" published
"$REAL_PYTHON" -c \
    'import json, pathlib, sys; d=json.loads(pathlib.Path(sys.argv[1]).read_text()); assert d["run_id"]=="stub-run"; assert len(d["content_hash"])==64; assert d["qa"]=={"blockers": 0}; assert d["published_at"]' \
    "$project/archive/manifests/$TEST_DATE.json" ||
    fail "mark-published did not preserve ready metadata"
grep -q '^screenshot ' "$project/calls.log" || fail "screenshot did not run"
grep -q '^git push' "$project/calls.log" || fail "git push did not run"

echo "3/9 published manifest is the only idempotent skip marker"
: >"$project/calls.log"
run_pipeline "$project" >"$project/second-output.log" 2>&1
[ ! -s "$project/calls.log" ] || fail "published retry performed pipeline work"

echo "4/9 ready manifest resumes publishing without regenerating"
project="$(new_project ready_resume)"
make_ready_project "$project"
run_pipeline "$project" >"$project/output.log" 2>&1
assert_manifest_status "$project" published
if grep -q '^feed ' "$project/calls.log"; then
    fail "ready resume unexpectedly regenerated feed"
fi
grep -q '^screenshot ' "$project/calls.log" || fail "ready resume did not continue publishing"

project="$(new_project tampered_ready)"
make_ready_project "$project"
printf 'tampered after gate\n' >>"$project/daily-ai-news-$TEST_DATE.md"
run_pipeline "$project" >"$project/output.log" 2>&1
assert_manifest_status "$project" published
grep -q '^feed ' "$project/calls.log" ||
    fail "tampered ready artifacts were published without regeneration"

echo "5/9 shared lock returns temporary-failure status"
project="$(new_project shared_lock)"
mkdir "$project/pipeline.lock"
printf '%s\n' "$$" >"$project/pipeline.lock/pid"
printf '%s\n' "$TEST_DATE" >"$project/pipeline.lock/report_date"
set +e
run_pipeline "$project" >"$project/output.log" 2>&1
rc=$?
set -e
[ "$rc" -eq 75 ] || fail "busy lock returned $rc instead of 75"

echo "6/9 catchup propagates failure and rejects false success"
project="$(new_project catchup)"
set +e
env \
    AI_DAILY_NEWS_DIR="$project" \
    MANIFEST_DIR="$project/archive/manifests" \
    PIPELINE_LOCK_DIR="$project/pipeline.lock" \
    PIPELINE_ENV_FILE="$project/empty.env" \
    PYTHON_BIN="$project/bin/python-stub" \
    GIT_BIN="$project/bin/git-stub" \
    MINIMAX_API_KEY="offline-test-key" \
    REAL_PYTHON="$REAL_PYTHON" \
    CALL_LOG="$project/calls.log" \
    STUB_FEED_RC=23 \
    CATCHUP_HISTORY_LOG="$project/logs/catchup.log" \
    "$project/catchup.sh" "$TEST_DATE" >"$project/catchup-output.log" 2>&1
rc=$?
set -e
[ "$rc" -eq 23 ] || fail "catchup returned $rc instead of child status 23"
if grep -q '发布完成' "$project/logs/catchup.log"; then
    fail "catchup falsely reported completion after failure"
fi

cp "$REPO_DIR/tests/fixtures/noop_success.sh" "$project/noop-success"
chmod +x "$project/noop-success"
set +e
env \
    AI_DAILY_NEWS_DIR="$project" \
    MANIFEST_DIR="$project/archive/manifests" \
    PYTHON_BIN="$project/bin/python-stub" \
    REAL_PYTHON="$REAL_PYTHON" \
    CALL_LOG="$project/calls.log" \
    AI_DAILY_RUN_SCRIPT="$project/noop-success" \
    CATCHUP_HISTORY_LOG="$project/logs/false-success.log" \
    "$project/catchup.sh" "$TEST_DATE" >"$project/false-success-output.log" 2>&1
rc=$?
set -e
[ "$rc" -eq 1 ] || fail "catchup accepted false success with status $rc"
grep -q 'published manifest 缺失' "$project/logs/false-success.log" ||
    fail "catchup did not diagnose missing published manifest"

echo "7/9 real local Git push publishes only the expected artifacts"
project="$(new_project real_git)"
remote="$TEST_ROOT/remote.git"
printf '*_mobile.png\n' >"$project/.gitignore"
git init -q "$project"
git -C "$project" config user.name "Pipeline Test"
git -C "$project" config user.email "pipeline-test@example.invalid"
git -C "$project" add .
git -C "$project" commit -qm "initial"
git init -q --bare "$remote"
git -C "$project" remote add origin "$remote"
git -C "$project" push -qu origin HEAD

env \
    AI_DAILY_NEWS_DIR="$project" \
    MANIFEST_DIR="$project/archive/manifests" \
    PIPELINE_LOCK_DIR="$project/pipeline.lock" \
    PYTHON_BIN="$project/bin/python-stub" \
    GIT_BIN="$(command -v git)" \
    PIPELINE_ENV_FILE="$project/empty.env" \
    MINIMAX_API_KEY="offline-test-key" \
    REAL_PYTHON="$REAL_PYTHON" \
    CALL_LOG="$project/calls.log" \
    "$project/run.sh" "$TEST_DATE" >"$project/output.log" 2>&1
assert_manifest_status "$project" published
git --git-dir="$remote" cat-file -e "HEAD:daily-ai-news-$TEST_DATE.html" ||
    fail "dated HTML was not pushed"
git --git-dir="$remote" cat-file -e "HEAD:daily-ai-news-$TEST_DATE-mobile.png" ||
    fail "ignored screenshot was not force-added and pushed"
git --git-dir="$remote" cat-file -e "HEAD:index.html" ||
    fail "index was not pushed"

test "$(
    "$REAL_PYTHON" "$REPO_DIR/pipeline_manifest.py" resolve-date \
        --now 2099-01-02T06:39:59+08:00
)" = "2099-01-01" || fail "pre-cutoff default date is not the prior completed window"
test "$(
    "$REAL_PYTHON" "$REPO_DIR/pipeline_manifest.py" resolve-date \
        --now 2099-01-02T06:40:00+08:00
)" = "$TEST_DATE" || fail "cutoff boundary did not advance the default date"

echo "8/9 notification is optional when unset and strict when configured"
env -u FEISHU_WEBHOOK \
    "$REAL_PYTHON" "$REPO_DIR/pipeline_notify.py" --date "$TEST_DATE" \
    >"$TEST_ROOT/notify-unset.log" 2>&1 ||
    fail "missing optional webhook unexpectedly failed"

port_file="$TEST_ROOT/webhook-success.port"
"$REAL_PYTHON" "$REPO_DIR/tests/fixtures/webhook_server.py" \
    --port-file "$port_file" --response '{"code":0,"msg":"success"}' &
server_pid=$!
for _ in $(seq 1 100); do
    [ -s "$port_file" ] && break
    sleep 0.02
done
[ -s "$port_file" ] || fail "local success webhook did not start"
FEISHU_WEBHOOK="http://127.0.0.1:$(cat "$port_file")/hook" \
    "$REAL_PYTHON" "$REPO_DIR/pipeline_notify.py" --date "$TEST_DATE" \
    >"$TEST_ROOT/notify-success.log" 2>&1 ||
    fail "successful webhook response was rejected"
wait "$server_pid"

port_file="$TEST_ROOT/webhook-rejected.port"
"$REAL_PYTHON" "$REPO_DIR/tests/fixtures/webhook_server.py" \
    --port-file "$port_file" --response '{"code":19001,"msg":"rejected"}' &
server_pid=$!
for _ in $(seq 1 100); do
    [ -s "$port_file" ] && break
    sleep 0.02
done
[ -s "$port_file" ] || fail "local rejection webhook did not start"
set +e
FEISHU_WEBHOOK="http://127.0.0.1:$(cat "$port_file")/hook" \
    "$REAL_PYTHON" "$REPO_DIR/pipeline_notify.py" --date "$TEST_DATE" \
    >"$TEST_ROOT/notify-rejected.log" 2>&1
rc=$?
set -e
wait "$server_pid"
[ "$rc" -eq 1 ] || fail "rejected webhook returned $rc instead of 1"

echo "9/9 credentials load only from environment or configured environment file"
project="$(new_project env_loading)"
set +e
env -u MINIMAX_API_KEY \
    AI_DAILY_NEWS_DIR="$project" \
    MANIFEST_DIR="$project/archive/manifests" \
    PIPELINE_LOCK_DIR="$project/pipeline.lock" \
    PIPELINE_ENV_FILE="$project/empty.env" \
    PYTHON_BIN="$project/bin/python-stub" \
    GIT_BIN="$project/bin/git-stub" \
    REAL_PYTHON="$REAL_PYTHON" \
    CALL_LOG="$project/calls.log" \
    "$project/run.sh" "$TEST_DATE" >"$project/missing-key.log" 2>&1
rc=$?
set -e
[ "$rc" -eq 78 ] || fail "missing model credential returned $rc instead of 78"
if [ -e "$project/calls.log" ] && grep -q '^feed ' "$project/calls.log"; then
    fail "feed ran without a model credential"
fi

printf 'MINIMAX_API_KEY=offline-file-key\n' >"$project/pipeline.env"
env -u MINIMAX_API_KEY \
    AI_DAILY_NEWS_DIR="$project" \
    MANIFEST_DIR="$project/archive/manifests" \
    PIPELINE_LOCK_DIR="$project/pipeline.lock" \
    PIPELINE_ENV_FILE="$project/pipeline.env" \
    PYTHON_BIN="$project/bin/python-stub" \
    GIT_BIN="$project/bin/git-stub" \
    REAL_PYTHON="$REAL_PYTHON" \
    CALL_LOG="$project/calls.log" \
    "$project/run.sh" "$TEST_DATE" >"$project/env-file.log" 2>&1
assert_manifest_status "$project" published

echo "PASS: pipeline script tests"
