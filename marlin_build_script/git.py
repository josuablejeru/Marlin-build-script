import git
from .logger import log


def checkout_repo(url, to_path, branch) -> git.Repo:
    try:
        if git.Repo(to_path).git_dir:
            repo = git.Repo(to_path)
            repo.git.checkout(branch)
            repo.remotes.origin.pull(branch)
            return repo
    except git.NoSuchPathError:
        repo = git.Repo.clone_from(url, to_path)
        return repo


def create_build_branch(repo: git.Repo, base_branch_name, new_branch_name):
    log.info(f"checkout branch: {base_branch_name}")
    repo.git.checkout(base_branch_name)

    log.info(f"create new branch {new_branch_name} for custom config ")
    try:
        repo.git.checkout('-b', new_branch_name)
    except Exception:
        log.info("branch exist checking out")
        repo.git.checkout(new_branch_name)

        log.info(f"try merging {base_branch_name} into {new_branch_name}")
        repo.git.merge(base_branch_name)


def commit_all(repo: git.Repo, message: str, author_name: str, email: str):
    if len(repo.untracked_files) == 0:
        log.warn("no files to commit... skip")
        return
    author = git.Actor(author_name, email)
    committer = git.Actor(author_name, email)
    repo.index.add(items=repo.untracked_files)
    repo.index.commit(message, author=author, committer=committer)
