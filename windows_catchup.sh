#!/usr/bin/env bash
# Windows 任务计划程序入口：由 Git Bash 调用，替代 macOS launchd。
# 先加载 .env（PYTHON_BIN、API key 等），再交给 catchup.sh；
# 是否需要生成、并发控制都由 catchup.sh / run.sh 负责。

set -Eeuo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
mkdir -p logs

if [ -r .env ]; then
    set -a
    # shellcheck disable=SC1091
    source .env
    set +a
fi

exec bash catchup.sh "$@" >>logs/catchup.log 2>&1
