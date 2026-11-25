# 港新研究生申请 DIY 工具包

打开一个可以保存文件的 Codex 对话，把下面这句话复制进去。安装、建项目和接下来的申请规划都在这条对话里完成。

```text
请按 https://raw.githubusercontent.com/ThreeBodyMonitor1379/grad-application-diy/v1.1.0/CODEX-START.md 在当前工作区建好我的研究生申请项目、安装项目专用技能，然后留在这条对话里一步步带我规划和推进申请，不用我运行命令。
```

第一次，Codex 会问你的本科属于普通国内本科、中外合办，还是暂时不确定。你直接回答，例如「我是中外合办，两校都注册了，但不知道最后发几个学位证」。它会把已确认的情况和今天要做的事写进「我的申请／申请计划.md」。下次说「继续」就能接着推进。你不必开终端、手选技能或再开对话；如果 Codex 没有联网或文件夹权限，它会告诉你需要允许哪一步。

想先看看这套方法？可以直接读[新手手册](payload/从这里开始.md)或[双学籍填表指南](payload/skills/grad-application-packet-audit/双学籍填表指南.md)。两校注册不一定有两个学位；填几条学籍、填几项资格要分开判断。

## 安装后只看这三处

| 入口 | 用途 |
|---|---|
| 先读我 | 打开自己的计划，回到刚才的对话继续 |
| 我的申请 | 申请计划、四张工作表、材料原件、文书草稿、提交回执 |
| 使用手册 | 从选校到录取的步骤；普通本科与中外合办的区别 |

技能在项目的 `.agents/skills/`，安装标记和工作记录在 `.application-agent/`；根目录的 `AGENTS.md` 只负责给助手指路。不会修改全局技能，也不会给个人项目配置 GitHub 远端。普通文件可在本机直接阅读；隐藏目录并非加密，个人项目切勿公开上传。公开仓库只分发匿名手册、空白模板、项目技能和安装测试。

## 换目录、重试与验证

日常使用直接和 Codex 说话。[给助手的安装步骤](CODEX-START.md)说明了如何在原对话续办、回读技能和更新计划。再次安装会保留已经填写的材料。遇到同名的非空目录，助手会先问你是否换一个位置。手动安装仍可在源码目录运行 `sh install.sh --no-chat "/已有父目录/新项目名"`，但这不是使用者必须做的步骤。

只下载过工具包、没有登录 Codex 的人，也能运行 `python3 -B -m unittest discover -s tests -v` 做离线验收。用例只建临时项目。公开仓库的 [Actions](https://github.com/ThreeBodyMonitor1379/grad-application-diy/actions/workflows/install.yml) 分别在 macOS 和 Ubuntu 上运行；它们不会登录账号或发送模型请求。

使用 Codex 可参考[官方 CLI 入门](https://developers.openai.com/codex/cli/)、[桌面对话链接](https://learn.chatgpt.com/docs/reference/commands#chats)和[项目内技能](https://developers.openai.com/codex/skills/)。
