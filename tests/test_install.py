"""Offline black-box tests. Run: python3 -B -m unittest discover -s tests -v"""

import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
from urllib.parse import unquote, urlsplit


INSTALL = Path(__file__).resolve().parents[1] / "install.sh"
SKILLS = {
    "grad-application-roadmap",
    "grad-application-packet-audit",
    "grad-application-follow-up",
    "grad-offer-review",
}


class InstallTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="grad-diy-")
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name).resolve()
        self.project = self.base / "空白 研究生申请"

    def command(self, target, no_chat=True):
        return ["/bin/sh", str(INSTALL), *(["--no-chat"] if no_chat else []), str(target)]

    def run_install(self, target, no_chat=True):
        return subprocess.run(
            self.command(target, no_chat), cwd=self.base, stdin=subprocess.DEVNULL,
            capture_output=True, text=True, timeout=30, check=False,
        )

    def assert_layout(self):
        root = self.project
        for path in ("先读我.md", "启动对话.command", "使用手册/从这里开始.md"):
            self.assertTrue((root / path).is_file(), path)
        self.assertTrue(os.access(root / "启动对话.command", os.X_OK))
        self.assertTrue((root / ".application-agent/logs").is_dir())
        user = root / "我的申请"
        names = {p.name for p in user.rglob("*.md")}
        self.assertTrue({"项目要求.md", "事实与证据.md", "提交前核对.md", "提交后待办.md"} <= names, names)
        discovered = {p.parent.name for p in (root / ".agents/skills").glob("*/SKILL.md")}
        self.assertEqual(discovered, SKILLS)
        # Require each local Markdown link in the installed guide to work independently
        # of the source checkout. External links are deliberately not fetched.
        guide = root / "使用手册/从这里开始.md"
        for href in re.findall(r"\]\(([^)]+)\)", guide.read_text(encoding="utf-8")):
            parsed = urlsplit(href.strip("<>"))
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (guide.parent / unquote(parsed.path)).resolve()
            self.assertIn(root, target.parents, href)
            self.assertTrue(target.exists(), href)

    def test_new_project(self):
        result = self.run_install(self.project)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(self.project.name, result.stdout)
        self.assert_layout()

    def test_empty_existing_directory(self):
        self.project.mkdir()
        result = self.run_install(self.project)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_layout()

    def test_reinstall_preserves_changes(self):
        self.assertEqual(self.run_install(self.project).returncode, 0)
        work = self.project / "我的申请"
        form = next(work.rglob("项目要求.md"))
        form.write_bytes(b"edited user form\n")
        note = work / "自己的一页.md"
        note.write_bytes(b"personal notes\n")
        self.run_install(self.project)
        self.assertEqual(form.read_bytes(), b"edited user form\n")
        self.assertEqual(note.read_bytes(), b"personal notes\n")
        self.assert_layout()

    def test_rejects_unrelated_directory_and_regular_file(self):
        self.project.mkdir()
        sentinel = self.project / "已在用.md"
        sentinel.write_bytes(b"keep")
        for target in (self.project, sentinel):
            with self.subTest(target=target.name):
                self.assertNotEqual(self.run_install(target).returncode, 0)
                self.assertEqual(list(self.project.iterdir()), [sentinel])
                self.assertEqual(sentinel.read_bytes(), b"keep")

    def test_existing_version_marker_does_not_hide_missing_entry(self):
        self.assertEqual(self.run_install(self.project).returncode, 0)
        old = self.project / "先读我.md"
        old.rename(self.project / "我保存的手册.md")
        retry = self.run_install(self.project)
        self.assertNotEqual(retry.returncode, 0)
        self.assertIn("不完整", retry.stderr)
        self.assertFalse(old.exists())
        self.assertTrue((self.project / "我保存的手册.md").is_file())

    def test_rejects_directory_symlink_and_dangling_link(self):
        outside = self.base / "别处"
        outside.mkdir()
        for name, dest in (("link", outside), ("dangling", outside / "missing")):
            with self.subTest(link=name):
                target = self.base / name
                target.symlink_to(dest, target_is_directory=True)
                self.assertNotEqual(self.run_install(target).returncode, 0)
                self.assertTrue(target.is_symlink())
                self.assertEqual(list(outside.iterdir()), [])

    def test_incomplete_package_does_not_partially_install(self):
        package = self.base / "损坏的安装包"
        package.mkdir()
        for name in ("install.sh", "install.py"):
            shutil.copy2(INSTALL.parent / name, package / name)
        shutil.copytree(INSTALL.parent / "payload", package / "payload")
        shutil.copytree(INSTALL.parent / "starter", package / "starter",
                        ignore=shutil.ignore_patterns("开场.txt"))
        self.project.mkdir()
        result = subprocess.run(
            ["/bin/sh", str(package / "install.sh"), "--no-chat", str(self.project)],
            cwd=self.base, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=30,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(self.project.iterdir()), [])
        self.assertEqual(set(self.base.iterdir()), {package, self.project})
        self.assertEqual(self.run_install(self.project).returncode, 0)
        self.assert_layout()

    def test_two_installers_do_not_mix_projects(self):
        command = self.command(self.project)
        processes = []
        try:
            for _ in range(2):
                processes.append(subprocess.Popen(
                    command, cwd=self.base, stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                ))
            output = [p.communicate(timeout=30)[0] for p in processes]
            self.assertIn(0, [p.returncode for p in processes], output)
            self.assert_layout()
            # A racing installer must not move a second staged tree inside the first.
            self.assertEqual(list(self.project.rglob("启动对话.command")), [self.project / "启动对话.command"])
        finally:
            for proc in processes:
                if proc.poll() is None:
                    proc.kill()
                    proc.communicate()

    def test_no_terminal_does_not_claim_chat_was_sent(self):
        # An installer invoked from a pipe must not start a GUI or require login.
        result = self.run_install(self.project, no_chat=False)
        self.assert_layout()
        output = result.stdout + result.stderr
        self.assertRegex(output, r"终端|交互|TTY|tty")
        self.assertNotRegex(output, r"首条消息已发送|首问已发送|对话已成功启动")


if __name__ == "__main__":
    unittest.main()
