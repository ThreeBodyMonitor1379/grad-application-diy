# 港新研究生申请 DIY 工具包

复制一条命令，你会得到自己的空白申请文件夹。第一次对话先问你是普通国内本科、中外合办，还是暂不确定。已有两校学籍也不意味着要填两项学位；工具包会带你分别核对学籍、授位和成绩来源。

## 安装

在 Mac「终端」、Linux 终端或 Windows 的 WSL 终端粘贴下面一整行，按回车。需要 Git 和 Python 3.8+；不需要管理员权限、GitHub 账号或第三方 Python 包。原生 Windows PowerShell 不适用。

```sh
(d=$(mktemp -d) && git -c advice.detachedHead=false clone -q --depth 1 --branch v1.0.0 https://github.com/ThreeBodyMonitor1379/grad-application-diy.git "$d/kit" && sh "$d/kit/install.sh")
```

项目默认放在个人主目录的「我的研究生申请」下，终端会打印完整路径。已安装并登录 Codex CLI，就在这个文件夹自动进入新对话。首次登录或信任目录的提示由你自己确认。Mac 上只有 Codex 桌面端时，安装器会请求打开预填好的新对话，你还要点一次发送。没有 Codex 也能安装和阅读手册。安装器不替你安装软件、不上传材料、不代交申请。

没用过终端的 Mac 用户，可以[下载 v1.0.0 ZIP](https://github.com/ThreeBodyMonitor1379/grad-application-diy/archive/refs/tags/v1.0.0.zip)，解压，再双击「安装.command」。若系统阻止运行，请不要关闭系统安全保护；可改用上面的终端命令，或直接阅读手册。

想先看内容？直接读[新手手册](payload/从这里开始.md)或[双学籍填表指南](payload/skills/grad-application-packet-audit/双学籍填表指南.md)。不想开对话，可在上面命令的 `install.sh"` 后、右括号前加 ` --no-chat`。下载了源码 ZIP 的使用者也可在解压后的目录运行 `sh install.sh --no-chat`。

## 安装后只看这三处

| 入口 | 用途 |
|---|---|
| 先读我 | 打开第一张表，或启动对话 |
| 我的申请 | 你填写的四张表、材料原件、文书草稿、提交回执 |
| 使用手册 | 从选校到录取的步骤；普通本科与中外合办的区别 |

技能在项目的 `.agents/skills/`，安装标记和工作记录在 `.application-agent/`；根目录的 `AGENTS.md` 只负责给助手指路。不会修改全局技能，也不会给个人项目配置 GitHub 远端。普通文件可在本机直接阅读；隐藏目录并非加密，个人项目切勿公开上传。公开仓库只分发匿名手册、空白模板、项目技能和安装测试。

## 换目录、重试与验证

在源码目录运行 `sh install.sh --no-chat "/已有父目录/新项目名"` 可选目录，父目录须存在。再次安装会保留已经填写的材料，不重复开启对话；需要新对话时打开项目里的「启动对话.command」。别的非空目录不会被覆盖。若个人项目曾被手动删去关键文件，请在新位置重装，再复制自己的表单和材料；不需要先删旧目录。

只下载过工具包、没有登录 Codex 的人，也能运行 `python3 -B -m unittest discover -s tests -v` 做离线验收。用例只建临时项目。公开仓库的 [Actions](https://github.com/ThreeBodyMonitor1379/grad-application-diy/actions/workflows/install.yml) 分别在 macOS 和 Ubuntu 上运行；它们不会登录账号或发送模型请求。

使用 Codex 可参考[官方 CLI 入门](https://developers.openai.com/codex/cli/)、[桌面对话链接](https://learn.chatgpt.com/docs/reference/commands#chats)和[项目内技能](https://developers.openai.com/codex/skills/)。
