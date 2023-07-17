from pathlib import Path

import git

REPO_DIR = (Path(__file__).parent.parent.parent / "repos/").resolve()


def rebuild_is_required(user: str, repo: str) -> bool:
    # Check if a rebuild is required, also pull new changes if a rebuild is indeed required.
    repo_path = REPO_DIR / f"{user}/{repo}"

    if not repo_path.exists():
        git.Repo.clone_from(f"https://github.com/{user}/{repo}", repo_path)
        # this is obviously the first build for this repo and so a build is required.
        return True

    repo = git.Repo(repo_path)
    old_sha = repo.head.commit

    remote = repo.active_branch.tracking_branch()
    repo.git.clean("-xdf")  # Clean up any untracked files (just in case build files aren't in gitignore)
    repo.git.reset("--hard", f"{remote.remote_name}/{remote.remote_head}")
    repo.remote(remote.remote_name).pull()

    new_sha = repo.head.commit
    return not (old_sha == new_sha)
