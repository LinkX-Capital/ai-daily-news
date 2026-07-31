#!/usr/bin/env bash
set -Eeuo pipefail

: "${REAL_PYTHON:?REAL_PYTHON is required}"
: "${AI_DAILY_NEWS_DIR:?AI_DAILY_NEWS_DIR is required}"
: "${CALL_LOG:?CALL_LOG is required}"

command_name="${1:-}"
case "$command_name" in
    -c)
        exec "$REAL_PYTHON" "$@"
        ;;
    */pipeline_manifest.py|pipeline_manifest.py|*/pipeline_notify.py|pipeline_notify.py)
        exec "$REAL_PYTHON" "$@"
        ;;
    feed_v5.py|*/feed_v5.py)
        printf 'feed %s\n' "$*" >>"$CALL_LOG"
        if [ "${STUB_FEED_RC:-0}" -ne 0 ]; then
            exit "${STUB_FEED_RC}"
        fi

        report_date=""
        previous=""
        for argument in "$@"; do
            if [ "$previous" = "--date" ]; then
                report_date="$argument"
                break
            fi
            previous="$argument"
        done
        : "${report_date:?feed stub expected --date}"

        mkdir -p "$AI_DAILY_NEWS_DIR/archive/manifests"
        printf '# report\n' >"$AI_DAILY_NEWS_DIR/daily-ai-news-$report_date.md"
        printf '<html>report</html>\n' >"$AI_DAILY_NEWS_DIR/daily-ai-news-$report_date.html"
        printf '<html>index</html>\n' >"$AI_DAILY_NEWS_DIR/index.html"
        printf '{"date":"%s","count":1,"articles":[{}]}\n' "$report_date" \
            >"$AI_DAILY_NEWS_DIR/archive/news_$report_date.json"
        "$REAL_PYTHON" -c \
            'import hashlib,json,pathlib,sys; manifest,date,md_path,archive_path,html_path=map(pathlib.Path,[sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]]); archive=json.loads(archive_path.read_text()); digest=hashlib.sha256(); digest.update(md_path.read_text().encode()); digest.update(json.dumps(archive,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()); digest.update(html_path.read_bytes()); manifest.write_text(json.dumps({"date": str(date), "status": "ready", "run_id": "stub-run", "content_hash": digest.hexdigest(), "artifacts": {"markdown": str(md_path), "archive": str(archive_path), "html": str(html_path)}, "qa": {"blockers": 0}}), encoding="utf-8")' \
            "$AI_DAILY_NEWS_DIR/archive/manifests/$report_date.json" "$report_date" \
            "$AI_DAILY_NEWS_DIR/daily-ai-news-$report_date.md" \
            "$AI_DAILY_NEWS_DIR/archive/news_$report_date.json" \
            "$AI_DAILY_NEWS_DIR/daily-ai-news-$report_date.html"
        ;;
    screenshot_and_push.py|*/screenshot_and_push.py)
        printf 'screenshot %s\n' "$*" >>"$CALL_LOG"
        report_date="${2:?screenshot stub expected a date}"
        printf 'png\n' >"$AI_DAILY_NEWS_DIR/daily-ai-news-$report_date-mobile.png"
        ;;
    *)
        exec "$REAL_PYTHON" "$@"
        ;;
esac
