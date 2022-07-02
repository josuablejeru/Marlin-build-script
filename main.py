#!/usr/local/bin/python
from marlin_build_script.logger import log
from typing import Dict, List
import yaml
import git
import requests
import os
import shutil


def load_config(path="./config.yml") -> Dict:
    with open(path, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    return data


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


def download_configfiles(urls: List):
    for url in urls:
        r = requests.get(url.get('url'), allow_redirects=True)
        with open(url.get('name'), 'wb') as f:
            f.write(r.content)


def move_files(files: List, dest="./Marlin/Marlin/"):
    for f in files:
        shutil.copy(f, dest)
        os.remove(f)


def main():
    ### Load configs ###
    config = load_config()
    log.debug(config)
    repo_url = config.get("marlin_repo").get('url')
    branch = config.get('marlin_repo').get("branch")
    build_branch = config.get('marlin_repo').get("build_branch")
    configuration_h = config.get('config_url').get("configuration_h")
    configuration_adv_h = config.get('config_url').get("configuration_adv_h")
    platformio = config.get('config_url').get('platformio')

    ### checkout the project ###
    log.info("checkout Marlin")
    marlin_repo = checkout_repo(repo_url, f"{os.getcwd()}/Marlin", branch)
    log.info("Marlin was checked out")

    create_build_branch(marlin_repo, branch, build_branch)

    log.info("download the provided custom Configuration files")
    download_configfiles(
        urls=[configuration_h, configuration_adv_h, platformio])

    log.info("move config files inside of Marlin")
    move_files([configuration_h.get('name'), configuration_adv_h.get('name')])
    move_files([platformio.get('name')], "./Marlin")


if __name__ == "__main__":
    main()
