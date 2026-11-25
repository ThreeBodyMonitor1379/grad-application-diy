#!/bin/sh
set -eu
here=$(CDPATH= cd -P "$(dirname "$0")" && pwd)
if [ ! -t 0 ] || [ ! -t 1 ]; then
    echo '没有交互终端，未启动对话。请在终端运行此文件。'
    exit 0
fi
prompt=$(cat "$here/.application-agent/开场.txt")
if command -v codex >/dev/null 2>&1; then
    echo '正在打开 Codex。首次使用时，请本人完成登录或确认信任这个新文件夹。'
    exec codex -C "$here" --sandbox workspace-write --ask-for-approval on-request "$prompt"
fi
if [ "$(uname -s)" = Darwin ] && command -v open >/dev/null 2>&1; then
    uri=$(python3 -I -c 'import sys, urllib.parse; print("codex://new?" + urllib.parse.urlencode(dict(path=sys.argv[1], prompt=sys.argv[2]), quote_via=urllib.parse.quote))' "$here" "$prompt")
    if open "$uri" 2>/dev/null; then
        echo '已请求桌面端打开新对话。请在窗口中按发送；如未打开，见「先读我.md」。'
        exit 0
    fi
fi
echo '项目已经可以使用；未找到可启动的 Codex。请先读「先读我.md」，或安装并登录 Codex CLI 后重新运行此文件。'
