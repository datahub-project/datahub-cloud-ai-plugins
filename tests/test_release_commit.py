import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.verify_release_commit import verify_release_commit


class ReleaseCommitTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.remote = Path(self.temporary.name) / "remote"
        self.checkout = Path(self.temporary.name) / "checkout"
        self.git("init", "--initial-branch=main", str(self.remote))
        self.git("config", "user.name", "Release test", cwd=self.remote)
        self.git("config", "user.email", "release-test@example.com", cwd=self.remote)
        self.git("commit", "--allow-empty", "-m", "Initial main", cwd=self.remote)
        self.initial = self.git("rev-parse", "HEAD", cwd=self.remote).strip()
        self.git("clone", str(self.remote), str(self.checkout))
        self.git("config", "user.name", "Release test", cwd=self.checkout)
        self.git("config", "user.email", "release-test@example.com", cwd=self.checkout)

    def git(self, *args, cwd=None):
        return subprocess.check_output(
            ["git", *args], cwd=cwd, text=True, stderr=subprocess.STDOUT
        )

    def test_accepts_main_tip(self):
        verify_release_commit(self.checkout)

    def test_accepts_annotated_tag_on_older_main_commit(self):
        self.git("commit", "--allow-empty", "-m", "Advance main", cwd=self.remote)
        self.git(
            "tag", "-a", "v1.0.0", "-m", "Release", self.initial, cwd=self.checkout
        )
        self.git("checkout", "--detach", "v1.0.0", cwd=self.checkout)
        verify_release_commit(self.checkout)

    def test_rejects_unmerged_commit_even_if_origin_main_is_stale(self):
        self.git("checkout", "-b", "unmerged", cwd=self.checkout)
        self.git("commit", "--allow-empty", "-m", "Unmerged change", cwd=self.checkout)
        self.git("update-ref", "refs/remotes/origin/main", "HEAD", cwd=self.checkout)
        with self.assertRaisesRegex(ValueError, "already merged into main"):
            verify_release_commit(self.checkout)
        self.assertEqual(
            self.git(
                "rev-parse", "refs/remotes/origin/main", cwd=self.checkout
            ).strip(),
            self.initial,
        )

    def test_accepts_commit_after_it_is_merged_into_main(self):
        self.git("checkout", "-b", "feature", cwd=self.remote)
        self.git("commit", "--allow-empty", "-m", "Feature", cwd=self.remote)
        feature = self.git("rev-parse", "HEAD", cwd=self.remote).strip()
        self.git("checkout", "main", cwd=self.remote)
        self.git("merge", "--no-ff", "feature", "-m", "Merge feature", cwd=self.remote)
        self.git("fetch", "origin", cwd=self.checkout)
        self.git("checkout", "--detach", feature, cwd=self.checkout)
        verify_release_commit(self.checkout)

    def test_fails_closed_if_main_is_unavailable(self):
        self.git("branch", "-m", "main", "renamed", cwd=self.remote)
        with self.assertRaises(subprocess.CalledProcessError):
            verify_release_commit(self.checkout)


if __name__ == "__main__":
    unittest.main()
