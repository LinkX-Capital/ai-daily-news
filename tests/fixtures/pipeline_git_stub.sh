#!/usr/bin/env bash
set -Eeuo pipefail

: "${CALL_LOG:?CALL_LOG is required}"
printf 'git %s\n' "$*" >>"$CALL_LOG"

case "${1:-}" in
    diff)
        exit "${STUB_GIT_DIFF_RC:-1}"
        ;;
    push)
        exit "${STUB_GIT_PUSH_RC:-0}"
        ;;
    *)
        exit 0
        ;;
esac
