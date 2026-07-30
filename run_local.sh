#!/usr/bin/env bash
# 本地/定时入口统一委托 run.sh，避免绕过 QA gate、共享锁和 published manifest。

set -Eeuo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/run.sh" "$@"
