# Graduate Application DIY Skills

一套给第一次自己申请香港、新加坡授课型硕士的人用的中文 Codex 技能。你在同一条对话里选项目、核材料、跟进补件和读录取信。普通国内本科与中外合办双学籍各有自己的填表路线。

**稳定版：[`v1.1.1`](https://github.com/ThreeBodyMonitor1379/grad-application-diy/tree/v1.1.1)** · [版本差异](https://github.com/ThreeBodyMonitor1379/grad-application-diy/compare/v1.1.0...v1.1.1) · [新手手册](./payload/从这里开始.md) · [安装测试](https://github.com/ThreeBodyMonitor1379/grad-application-diy/actions/workflows/install.yml)

> [!IMPORTANT]
> 两校注册不等于两个学位。按注册证明核学籍，按授位材料核学位；学校只出具在读证明时，不把合作院校的 GPA 填进去。[双学籍填表指南](./payload/skills/grad-application-packet-audit/双学籍填表指南.md)列出了两条路线及需要问学校的例外。

## 🚀 懒人指令｜整句复制给 Codex（推荐）

> [!TIP]
> 在能保存文件的 Codex 对话中发送下面这一句。Codex 负责安装；你不用开终端、手选技能或另开对话。

```text
请按 https://raw.githubusercontent.com/ThreeBodyMonitor1379/grad-application-diy/v1.1.1/CODEX-START.md 在当前工作区建好我的研究生申请项目、安装项目专用技能，然后留在这条对话里一步步带我规划和推进申请，不用我运行命令。
```

第一问是：「你的本科属于普通国内本科、中外合办（可能有双学籍），还是暂时不确定？」可以直接答「两校都注册了，但我不知道最后发几个学位证」。助手会把已确认的事实和尚待查证的下一步分开记入个人计划。以后说「继续」即可。如果工作区不可写或无法联网，助手会说明卡在哪一步。

## 先选入口

| 你的情况 | 使用的 skill | 得到什么 |
|---|---|---|
| 还没选定项目，先想知道这周做什么 | [立项与选校](./payload/skills/grad-application-roadmap/SKILL.md) | 一份当季项目对照和首周计划 |
| 正在填教育经历，或担心成绩单放错了学校 | [字段与附件核对](./payload/skills/grad-application-packet-audit/SKILL.md) | 逐校核对的字段、对应证明和待确认项 |
| 提交后收到推荐信提醒、补件或更正通知 | [提交后跟进](./payload/skills/grad-application-follow-up/SKILL.md) | 已收到什么、还缺什么、下一步由谁处理 |
| 收到录取信，不清楚哪天答复、哪天付款 | [录取信核对](./payload/skills/grad-offer-review/SKILL.md) | 录取条件、两个期限和仍需本人作的决定 |

<details>
<summary><strong>三句可以直接接着问的话</strong></summary>

- 「我是普通国内本科，想申明年秋季的通信方向。这周先做哪件事？」
- 「我在两所学校都有学籍，外方还没出成绩。可以先填哪些字段，哪些要问学校？」
- 「学院来信说还缺中文成绩单，但门户显示已上传。先帮我核对是不是同一学期，不要重复提交。」

</details>

## 安装后，资料放在哪里？

| 入口 | 用途 |
|---|---|
| 先读我 | 打开自己的计划，回到刚才的对话继续 |
| 我的申请 | 申请计划、四张工作表、材料原件、文书草稿、提交回执 |
| 使用手册 | 从选校到录取的步骤；普通本科与中外合办的区别 |

技能在项目的 `.agents/skills/`，工作记录在 `.application-agent/`，根目录的 `AGENTS.md` 给助手指路。不会改全局技能，也不为个人项目设置 GitHub 远端。隐藏目录没有加密；不要把填好的个人项目推到公开仓库。公开仓库只分发匿名手册、空白模板、项目技能及安装测试。

## 手动安装与验证

<details>
<summary><strong>换目录、复用已有项目或验证安装结果</strong></summary>

[给助手的安装步骤](./CODEX-START.md)说明如何在原对话回读技能、更新计划。已有个人项目会原样续用，不覆盖旧版技能或已填材料；想单独体验新排版，可让 Codex 另建一个空项目。同名但不属于本工具包的非空目录不会被覆盖。想手动安装时，可在源码目录运行 `sh install.sh --no-chat "/已有父目录/新项目名"`。

只下载过工具包、没有登录 Codex 的人，也能运行 `python3 -B -m unittest discover -s tests -v` 做离线验收。用例只建临时项目。公开仓库的 [Actions](https://github.com/ThreeBodyMonitor1379/grad-application-diy/actions/workflows/install.yml) 分别在 macOS 和 Ubuntu 上运行；它们不会登录账号或发送模型请求。

安装测试检查的是文件和数据是否正确保留，不能证明学校已收件或认可某种填法。登录、保密推荐、确认声明和付款由相应当事人自己完成。

</details>

<details>
<summary><strong>维护技能时沿用哪种 Markdown 写法？</strong></summary>

首页给申请人看，保留一个安装指令和按情境选技能的入口。单项技能给执行者读：块式 YAML 描述写明什么时候用、什么时候不用；正文按来源（R）、判断方法（I）、示例（A1）、触发（A2）、步骤（E）、边界（B）排列，最后列相邻技能与审计依据。虚构案例须明说，测试用例与实际跑过的测试分开记。给申请人填写的空表不套这个结构。

</details>
