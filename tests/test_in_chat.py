"""Offline acceptance tests for installation inside the user's current Codex chat."""
from pathlib import Path
import subprocess
import tempfile
import unittest


RELEASE = Path(__file__).resolve().parents[1]
SKILLS = {
    "grad-application-roadmap", "grad-application-packet-audit",
    "grad-application-follow-up", "grad-offer-review",
}


class SameChatTest(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory(prefix="diy-same-chat-")
        self.addCleanup(scratch.cleanup)
        self.work = Path(scratch.name).resolve()
        self.project = self.work / "我的 研究生申请"

    def invoke(self, *args):
        return subprocess.run(args, cwd=self.work, stdin=subprocess.DEVNULL,
                              capture_output=True, text=True, timeout=30)

    def install(self, mode="--in-chat", source=RELEASE):
        return self.invoke("/bin/sh", str(source / "install.sh"), mode, str(self.project))

    def test_install_hands_off_in_place_without_another_launcher(self):
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"(当前|本|这[个条]?)(会话|对话)")
        self.assertNotRegex(result.stdout, r"请在终端运行|需要时运行项目中的")
        self.assertTrue((self.project / "我的申请/申请计划.md").is_file())
        installed = {p.parent.name for p in self.project.glob(".agents/skills/*/SKILL.md")}
        self.assertEqual(installed, SKILLS)

    def test_repeat_preserves_plan_and_user_evidence(self):
        self.assertEqual(self.install().returncode, 0)
        plan = self.project / "我的申请/申请计划.md"
        evidence = self.project / "我的申请/材料原件/保留的示例.txt"
        plan.write_text("自己排的下一步：问教务处。\n", encoding="utf-8")
        evidence.write_bytes(b"do not replace")
        original = {p: p.read_bytes() for p in (plan, evidence)}
        again = self.install()
        self.assertEqual(again.returncode, 0, again.stderr)
        for path, data in original.items():
            self.assertEqual(path.read_bytes(), data)

    def test_default_in_chat_stays_in_workspace_then_reuses_it(self):
        command = ["/bin/sh", str(RELEASE / "install.sh"), "--in-chat"]
        first = self.invoke(*command)
        self.assertEqual(first.returncode, 0, first.stderr)
        project = self.work / "我的研究生申请"
        self.assertTrue((project / "我的申请/申请计划.md").is_file())
        again = subprocess.run(command, cwd=project, capture_output=True, timeout=30)
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertFalse((project / "我的研究生申请").exists())

    def test_real_v1_project_can_continue_without_overwriting_user_files(self):
        # A ZIP / shallow checkout need not contain historical source.
        if not (RELEASE / ".git").exists() or self.invoke(
            "git", "-C", str(RELEASE), "rev-parse", "--verify", "--quiet",
            "refs/tags/v1.0.0^{commit}",
        ).returncode:
            self.skipTest("requires a local Git checkout containing the historical v1.0.0 tag")
        legacy = self.work / "v1.0.0"
        cloned = self.invoke("git", "-c", "advice.detachedHead=false", "clone", "-q",
                             "--no-local", "--depth", "1", "--branch", "v1.0.0", str(RELEASE), str(legacy))
        self.assertEqual(cloned.returncode, 0, cloned.stderr)
        first = self.install("--no-chat", legacy)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertIn("v1.0.0", (self.project / ".application-agent/version").read_text(encoding="utf-8"))
        private = self.project / "我的申请"
        plan = private / "申请计划.md"
        self.assertFalse(plan.exists(), "the historical release must not already contain the new plan")
        (private / "事实与证据.md").write_text("学生自己确认的事实。", encoding="utf-8")
        snapshots = {p: p.read_bytes() for p in private.rglob("*") if p.is_file()}
        resumed = self.install()
        self.assertEqual(resumed.returncode, 0, resumed.stderr)
        self.assertRegex(resumed.stdout, r"(当前|本|这[个条]?)(会话|对话)")
        self.assertTrue(plan.is_file())
        self.assertFalse(plan.is_symlink())
        for path, data in snapshots.items():
            self.assertEqual(path.read_bytes(), data)

    def test_incomplete_existing_skill_is_not_reported_as_ready(self):
        self.assertEqual(self.install().returncode, 0)
        skill = self.project / ".agents/skills/grad-application-roadmap/SKILL.md"
        remaining = skill.with_name("手动改了名.md")
        skill.rename(remaining)
        failed = self.install()
        self.assertNotEqual(failed.returncode, 0)
        self.assertFalse(skill.exists())
        self.assertTrue(remaining.exists())
        self.assertNotIn("项目已创建", failed.stdout)

    def test_plan_or_parent_link_cannot_redirect_writes_outside(self):
        self.assertEqual(self.install().returncode, 0)
        user = self.project / "我的申请"
        plan = user / "申请计划.md"
        original = user / "自己的计划.md"
        plan.rename(original)
        outside = self.work / "别处"
        outside.mkdir()
        sentinel = outside / "个人资料.txt"
        sentinel.write_bytes(b"untouched")
        # A dangling link is just as unacceptable as an existing target.
        for dest in (sentinel, outside / "不存在.md"):
            with self.subTest(target=dest.name):
                plan.symlink_to(dest)
                self.assertNotEqual(self.install().returncode, 0)
                self.assertTrue(plan.is_symlink())
                self.assertEqual(list(outside.iterdir()), [sentinel])
                self.assertEqual(sentinel.read_bytes(), b"untouched")
                plan.unlink()
        former = self.project / "原来的申请目录"
        user.rename(former)
        user.symlink_to(outside, target_is_directory=True)
        self.assertNotEqual(self.install().returncode, 0)
        self.assertTrue(user.is_symlink())
        self.assertEqual(list(outside.iterdir()), [sentinel])
        self.assertEqual(sentinel.read_bytes(), b"untouched")
        self.assertTrue((former / original.name).is_file())


if __name__ == "__main__":
    unittest.main()
