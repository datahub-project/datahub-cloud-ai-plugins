"""Reject release tags whose commit is not reachable from the current main branch."""

import subprocess
from pathlib import Path


def verify_release_commit(repository: Path) -> None:
    subprocess.run(
        [
            "git",
            "fetch",
            "--no-tags",
            "origin",
            "+refs/heads/main:refs/remotes/origin/main",
        ],
        cwd=repository,
        check=True,
    )
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", "HEAD", "refs/remotes/origin/main"],
        cwd=repository,
    )
    if result.returncode == 1:
        raise ValueError("Release tags must point to a commit already merged into main")
    result.check_returncode()


if __name__ == "__main__":
    try:
        verify_release_commit(Path.cwd())
    except (ValueError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"::error::{error}") from error
