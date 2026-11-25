# 给当前申请项目添加 CV／PS 写作技能

选校时不用装写作包。准备写简历或个人陈述时，把下面任一句发给当前 Codex 对话；不需要开终端。如果是从较早版本建的项目，也可以使用这三句。

**只装 CV（学术简历）：**

```text
请按 https://raw.githubusercontent.com/ThreeBodyMonitor1379/grad-application-diy/v1.2.0/payload/WRITING-SKILLS.md 只安装 CV 写作技能到我的申请项目，核验后在本对话告诉我写简历第一步需要什么。
```

**只装 PS（个人陈述／SOP）：**

```text
请按 https://raw.githubusercontent.com/ThreeBodyMonitor1379/grad-application-diy/v1.2.0/payload/WRITING-SKILLS.md 只安装 PS 写作技能到我的申请项目，核验后在本对话先问我要申请项目的文书题目。
```

**两套一起装：**

```text
请按 https://raw.githubusercontent.com/ThreeBodyMonitor1379/grad-application-diy/v1.2.0/payload/WRITING-SKILLS.md 把 CV 和 PS 两套写作技能都安装到我的申请项目，分别核验，留在本对话继续。
```

## 两套技能分别从哪里来？

| 我想做什么 | 下载来源 | 写作入口 |
|---|---|---|
| 从成绩、项目与经历整理出一份针对目标项目的 CV | [Academic-application-CV · v0.2.0](https://github.com/ThreeBodyMonitor1379/Academic-application-CV/tree/v0.2.0)（7 项） | `evidence-first-admissions-cv` |
| 按目标项目题目准备 PS／SOP，先确认证据与大纲，再起草 | [Academic-application-PS · v0.2.0](https://github.com/ThreeBodyMonitor1379/Academic-application-PS/tree/v0.2.0)（3 项） | `evidence-first-graduate-personal-statement` |

两库继续独立维护，仍可单独安装。总项目只分发指令，不转载技能正文，也不改两库的许可证和第三方声明。只选 PS 时不额外下载 CV；用得到的 `two-way-academic-fit` 包含在 CV 套件中，没装时按 PS 自带说明处理。

## 给执行安装的 Codex

1. **定位和选包。** 沿用本对话已确定的申请项目，核对其 `.application-agent/version`。未定位时，只问要用哪个项目；如果用户同时要求建项，则先按总项目引导创建。将目标显式设为该项目的 `.agents/skills/`，核对目录及各目标不是符号链接、解析后未越出项目。不要写全局技能目录。没有明确选哪套时问一句，不因用户仅提到 CV／PS 就自动下载。
2. **取固定源。** 把用户选定的上游检出到各自的临时目录，标签均为 `v0.2.0`。用 `git rev-parse HEAD` 核对：CV 为 `ffb6e9e482417a5d09318dfd78e4a8f6b30ca6a7`，PS 为 `74417fe37a8bccf690c786abb94a680fd1138ed2`。无 Git 时只用这两个提交对应的官方 GitHub 源码归档；无法核对来源就停止，不改用 main。不要读取申请人材料；上游的许可证与第三方说明见各自固定版本仓库。
3. **比较后安装。** 对固定源 `skills/` 下每个技能，将目录名与 `SKILL.md` 的 `name` 对上，比较源和目标的相对文件清单与逐文件 SHA-256。不存在才安装完整目录；完全一致记 `identical`；同名但不同、包含软链或不是普通目录记 `conflict`，保留原状。不用另一个同名的全局技能充数。确认没有其他安装任务同时写目标。
   - **CV：** 优先用系统的 `skill-installer` 助手脚本 `install-skill-from-github.py`：显式传 `--repo ThreeBodyMonitor1379/Academic-application-CV --ref ffb6e9e482417a5d09318dfd78e4a8f6b30ca6a7 --dest "<项目绝对路径>/.agents/skills" --path …`，将省略处展开为步骤 2 检出的、尚未安装的每个 `skills/<目录名>`。没有助手脚本时，可将已核对源码中的完整技能目录分别复制到不存在的项目目标；不合并、不覆盖。
   - **PS：** 用 Python 3.10+ 在固定源码目录执行 `python3 -B scripts/install_skills.py --target-dir "<项目绝对路径>/.agents/skills" --json`。不可省略 `--target-dir`。若已发现不安全的目标，先排除该项，只对安全项逐个传 `--skill <目录名>`；如没有安全项可装则停止。
4. **回读与验收。** 每项回读已安装文件，与固定源重新比对清单和 SHA-256；报告 `installed / identical / conflict / 未完成`。只选 CV 应核 7 项，只选 PS 应核 3 项，两套都选则分别列出 7＋3。失败或中断时不要自动清空或覆盖目标；重试先重新比对。文件已下载不等于写作验证工具都可用。
5. **分清文件与运行环境。** 按上游说明分别检查结构。需要完整工具链验收时，在独立环境使用上游固定依赖：CV 跑编排器的 validator 测试并检测 LaTeX/PDF 能力；PS 跑 `scripts/validate_release.py`、各技能的 `scripts/quick_validate.py` 和仓库测试。未经确认不安装系统软件或大型 TeX 发行版。没运行的检查、缺失的能力和冲突单列，不能报告完整验收通过。
6. **在原对话接着写。** 如果入口包已核对，直接读本项目中的 `.agents/skills/evidence-first-admissions-cv/SKILL.md` 或 `.agents/skills/evidence-first-graduate-personal-statement/SKILL.md`。CV 先问目标项目和可使用的经历证据；PS 先问正式题目、字数或字符限制。两个都装好且没有指定先后时，让用户挑先写哪份。若入口有冲突，不使用未经核验的本地版本冒充上游。下载本身不授权检索私有原件、撰写推荐人评价或提交申请。
