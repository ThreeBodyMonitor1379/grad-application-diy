"""Offline install checks for the optional, independently maintained writing packs."""
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


RELEASE = Path(__file__).resolve().parents[1]
GUIDE = Path("使用手册/WRITING-SKILLS.md")
CORE = {"grad-application-roadmap", "grad-application-packet-audit",
        "grad-application-follow-up", "grad-offer-review"}


class WritingGuideTest(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory(prefix="grad-writing-guide-")
        self.addCleanup(scratch.cleanup)
        self.work = Path(scratch.name).resolve()
        self.project = self.work / "申请 工作区"

    def run_in_scratch(self, *command):
        return subprocess.run(command, cwd=self.work, stdin=subprocess.DEVNULL,
                              capture_output=True, text=True, timeout=30)

    def install(self, source=RELEASE):
        return self.run_in_scratch(sys.executable, "-I", "-B", str(source / "install.py"),
                                   "--in-chat", str(self.project))

    def test_writing_sources_available_offline_but_not_installed_by_default(self):
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        installed = {p.name for p in (self.project / ".agents/skills").iterdir()}
        self.assertEqual(installed, CORE)
        text = (self.project / GUIDE).read_text(encoding="utf-8")
        sources = (("Academic-application-CV", "evidence-first-admissions-cv"),
                   ("Academic-application-PS", "evidence-first-graduate-personal-statement"))
        for repo, entry in sources:
            with self.subTest(repo=repo):
                self.assertRegex(text, rf"https://github\.com/ThreeBodyMonitor1379/"
                                       rf"{repo}/(?:tree|blob)/(?:v0\.2\.0|[0-9a-f]{{40}})\b")
                self.assertIn(entry, text)

    def test_reader_and_agent_can_find_installed_guide(self):
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        guide = self.project / GUIDE
        for entry in ("先读我.md", "使用手册/从这里开始.md", "AGENTS.md"):
            with self.subTest(entry=entry):
                doc = self.project / entry
                text = doc.read_text(encoding="utf-8")
                # Agent guidance may use a backticked path instead of a rendered link.
                paths = re.findall(r"\]\(([^)]+)\)|`([^`\n]+)`", text)
                candidates = [x.strip("<>") for pair in paths for x in pair
                              if x.endswith("WRITING-SKILLS.md") and "://" not in x]
                self.assertTrue(any((doc.parent / x).resolve() == guide.resolve()
                                    for x in candidates), entry)
                self.assertTrue(guide.is_file())

    def test_incomplete_new_install_preserves_applicant_evidence(self):
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        sentinel = self.project / "我的申请/材料原件/请保留.txt"
        sentinel.write_bytes(b"not a public resource")
        (self.project / GUIDE).unlink()
        self.assertNotEqual(self.install().returncode, 0)
        self.assertEqual(sentinel.read_bytes(), b"not a public resource")

    def test_v111_projects_do_not_need_the_new_guide_to_resume(self):
        ref = "refs/tags/v1.1.1^{commit}"
        if not (RELEASE / ".git").exists() or self.run_in_scratch(
                "git", "-C", str(RELEASE), "rev-parse", "--verify", "--quiet", ref).returncode:
            self.skipTest("requires the v1.1.1 tag (unavailable in ZIP or shallow clones)")
        old = self.work / "upstream-v111"
        clone = self.run_in_scratch("git", "clone", "--quiet", "--no-local", "--depth", "1",
                                    "--branch", "v1.1.1", str(RELEASE), str(old))
        self.assertEqual(clone.returncode, 0, clone.stderr)
        before = self.install(old)
        self.assertEqual(before.returncode, 0, before.stderr)
        self.assertFalse((self.project / GUIDE).exists())
        sentinel = self.project / "我的申请/申请计划.md"
        sentinel.write_bytes(b"private study plan")
        resumed = self.install()
        self.assertEqual(resumed.returncode, 0, resumed.stderr)
        self.assertEqual(sentinel.read_bytes(), b"private study plan")


if __name__ == "__main__":
    unittest.main()
