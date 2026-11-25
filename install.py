"""Build a new, local project. No network or user account is needed here."""
import argparse
import errno
import os
from pathlib import Path
import shutil
import sys
import tempfile


BASE = Path(__file__).resolve().parent
SOURCE = BASE / "payload"
SKILLS = ("grad-application-roadmap", "grad-application-packet-audit",
          "grad-application-follow-up", "grad-offer-review")
FORMS = ("项目要求", "事实与证据", "提交前核对", "提交后待办")
STAMP = ".application-agent/version"
EDITION = "grad-application-diy/v1.1.1\n"
KNOWN_STAMPS = {EDITION.encode(), b"grad-application-diy/v1.1.0\n", b"grad-application-diy/v1.0.0\n"}


def copy(source, destination):
    if not source.is_file() or source.is_symlink() or BASE not in source.resolve().parents:
        raise ValueError("安装包不完整或含意外链接：" + source.name)
    shutil.copyfile(str(source), str(destination))


def build(stage):
    work = stage / "我的申请"
    guide = stage / "使用手册"
    sysdir = stage / ".application-agent"
    for directory in (work, guide, work / "材料原件", work / "文书草稿",
                      work / "提交与回执", sysdir / "logs"):
        directory.mkdir(parents=True, exist_ok=True)
    for form in FORMS:
        copy(SOURCE / "模板" / (form + ".md"), work / (form + ".md"))
    copy(BASE / "starter" / "申请计划.md", work / "申请计划.md")
    for skill in SKILLS:
        dest = stage / ".agents" / "skills" / skill
        dest.mkdir(parents=True)
        copy(SOURCE / "skills" / skill / "SKILL.md", dest / "SKILL.md")
    special = Path("skills/grad-application-packet-audit/双学籍填表指南.md")
    for out in (guide / special.name, stage / ".agents" / special):
        copy(SOURCE / special, out)
    # Rebase the source handout's repository links to the reader's working copies.
    dest = guide / "从这里开始.md"
    copy(SOURCE / dest.name, dest)
    handout = dest.read_text(encoding="utf-8")
    dest.write_text(handout.replace("](" + special.as_posix() + ")", "](" + special.name + ")")
                    .replace("](模板/", "](../我的申请/").replace("](skills/", "](../.agents/skills/"),
                    encoding="utf-8")
    for name in ("先读我.md", "AGENTS.md", "启动对话.command"):
        copy(BASE / "starter" / name, stage / name)
    copy(BASE / "starter" / "开场.txt", sysdir / "开场.txt")
    (stage / "启动对话.command").chmod(0o700)
    (sysdir / "logs/工作记录.md").write_text("# 项目工作记录\n\n安装完成；尚未录入申请资料。\n", encoding="utf-8")
    (stage / STAMP).write_text(EDITION, encoding="utf-8")
    (stage / ".gitignore").write_text("# Personal application workspace: keep all files local.\n*\n", encoding="utf-8")


def is_installed(dest):
    marker = dest / STAMP
    if (dest.is_symlink() or marker.parent.is_symlink() or marker.is_symlink()
            or not marker.is_file() or marker.stat().st_size != len(EDITION)
            or marker.read_bytes() not in KNOWN_STAMPS):
        return False
    required = ["先读我.md", "启动对话.command", "AGENTS.md", "使用手册/从这里开始.md", "使用手册/双学籍填表指南.md",
                ".application-agent/开场.txt", ".application-agent/logs/工作记录.md",
                ".agents/skills/grad-application-packet-audit/双学籍填表指南.md"]
    required.extend(".agents/skills/" + skill + "/SKILL.md" for skill in SKILLS)
    for entry in required:
        member = dest / entry
        if member.resolve() != member or not member.is_file():
            raise ValueError("现有安装不完整。原文件已保留；请另选空目录安装，再复制个人资料。")
    return True


def install(raw, in_chat=False):
    if not raw.strip() or Path(raw).name in ("", "..") or any(c in raw for c in "\r\n\x00"):
        raise ValueError("请指定一个新的项目文件夹名称。")
    path = Path(raw).expanduser()
    dest = path.parent.resolve(strict=True) / path.name
    if (dest.is_symlink() or dest == Path.home().resolve() or dest == BASE or BASE in dest.parents
            or (dest == Path.cwd().resolve() and not (in_chat and is_installed(dest)))):
        raise ValueError("请选择独立的项目子目录，不要选择主目录、当前目录、安装包内目录或符号链接。")
    if dest.exists():
        if is_installed(dest):
            return dest, False
        if not dest.is_dir() or any(dest.iterdir()):
            raise ValueError("目标不是空目录；未改动原有文件，请另选目录。")
    # Stage on the same filesystem: interrupted builds never expose half a project.
    # POSIX rename replaces an empty directory, never a non-empty competing one.
    with tempfile.TemporaryDirectory(prefix=".grad-diy-", dir=str(dest.parent)) as scratch:
        stage = Path(scratch) / "project"
        stage.mkdir(mode=0o700)
        build(stage)
        try:
            stage.rename(dest)
        except OSError as exc:
            if exc.errno in (errno.EEXIST, errno.ENOTEMPTY) and is_installed(dest):
                return dest, False
            raise
    return dest, True


def main():
    parser = argparse.ArgumentParser(description="创建一份空白的本地研究生申请项目。")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--no-chat", action="store_true", help="只建目录，不启动 Codex")
    modes.add_argument("--in-chat", action="store_true", help="在调用方的现有 Codex 对话中继续规划")
    parser.add_argument("directory", nargs="?")
    args = parser.parse_args()
    os.umask(0o077)
    raw = args.directory
    if raw is None:
        parent = Path.cwd() if args.in_chat else Path.home()
        raw = str(parent if args.in_chat and is_installed(parent) else parent / "我的研究生申请")
    dest, fresh = install(raw, in_chat=args.in_chat)
    print(("项目已创建：" if fresh else "项目已经存在，保留全部原文件：") + str(dest), flush=True)
    print("入口：" + str(dest / "先读我.md"), flush=True)
    if args.in_chat:
        # Keep old personal work untouched. Add the newly introduced blank plan only
        # if absent, using an atomic exclusive link (also safe for concurrent retries).
        work = dest / "我的申请"
        plan = work / "申请计划.md"
        if not work.is_dir() or work.is_symlink() or plan.is_symlink():
            raise ValueError("计划目录不完整或含符号链接；未改动个人资料。")
        for form in FORMS:
            member = work / (form + ".md")
            if member.is_symlink() or not member.is_file():
                raise ValueError("申请工作表不完整；未改动个人资料。")
        if not plan.exists():
            with tempfile.TemporaryDirectory(prefix=".grad-plan-", dir=str(work)) as temp:
                candidate = Path(temp) / "plan"
                copy(BASE / "starter" / "申请计划.md", candidate)
                try:
                    os.link(candidate, plan)
                except FileExistsError:
                    pass
        if plan.is_symlink() or not plan.is_file():
            raise ValueError("申请计划不是普通文件；未改动个人资料。")
        print("留在当前对话，读取项目规则和立项技能；个人计划：" + str(plan))
        print("新项目首问：你的本科属于普通国内本科、中外合办（可能有双学籍），还是暂时不确定？已有回答就从未完成事项继续。")
        return
    if not fresh or args.no_chat:
        print("本次未启动对话。需要时运行项目中的「启动对话.command」。")
        return
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        print("没有交互终端，未启动对话。请在终端运行项目中的「启动对话.command」。")
        return
    launcher = str(dest / "启动对话.command")
    os.execl("/bin/sh", "sh", launcher)


if __name__ == "__main__":
    if sys.version_info < (3, 8):
        sys.exit("请使用 Python 3.8 或更新版本；无须安装第三方包。")
    try:
        main()
    except (OSError, ValueError) as error:
        sys.exit("安装未完成：" + str(error))
