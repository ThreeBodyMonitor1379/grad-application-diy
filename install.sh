#!/bin/sh
set -eu
if ! command -v python3 >/dev/null 2>&1; then
    echo '建项目需要 Python 3.8 或更新版本（不安装任何 Python 包）。请先安装 Python 3，再运行同一条指令。' >&2
    exit 1
fi
base=$(CDPATH= cd -P "$(dirname "$0")" && pwd)
exec python3 -I -B "$base/install.py" "$@"
