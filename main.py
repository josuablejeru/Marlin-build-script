#!/usr/local/bin/python
from marlin_build_script.logger import log
import marlin_build_script.git as git
from typing import Dict, List
import yaml
import requests
import os
import shutil


def load_config(path="./config.yml") -> Dict:
    with open(path, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    return data


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

    # Repo configs
    repo_url = config.get("marlin_repo").get('url')
    branch = config.get('marlin_repo').get("branch")
    build_branch = config.get('marlin_repo').get("build_branch")

    # Configuration
    configuration_h = config.get('config_url').get("configuration_h")
    configuration_adv_h = config.get('config_url').get("configuration_adv_h")
    platformio = config.get('config_url').get('platformio')

    # Git
    author = config.get('git_config').get('author')
    email = config.get('git_config').get('email')

    # Parameter
    custom_settings_configuration_h = config.get(
        'custom_settings').get('configuration_h')
    custom_settings_configuration_adv_h = config.get(
        'custom_settings').get('configuration_adv_h')

    ### checkout the project ###
    log.info("checkout Marlin")
    marlin_repo = git.checkout_repo(repo_url, f"{os.getcwd()}/Marlin", branch)
    log.info("Marlin was checked out")

    git.create_build_branch(marlin_repo, branch, build_branch)

    log.info("download the provided custom Configuration files")
    download_configfiles(
        urls=[configuration_h, configuration_adv_h, platformio])

    log.info("move config files inside of Marlin")
    move_files([configuration_h.get('name'), configuration_adv_h.get('name')])
    move_files([platformio.get('name')], "./Marlin")

    log.info("Commit Changes!")
    git.commit_all(marlin_repo, "Set base build configs", author, email)


if __name__ == "__main__":
    main()
