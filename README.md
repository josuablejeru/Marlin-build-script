# Marlin build script

Creating a custom Marlin build involes multiple steps and look-ups and downloads and modifing the header files.
If you want to change something, for example settings, you need to maintain a seperate spreadcheet for documentation.
Things get even complicated if you want to get settings from others and include you own on top of it.

To solve this I created this script which insures I have always the latest changes and don't have to maintain a spreadcheed with my configs.

At it's core this small "build-tool" interacts with your own Marlin fork.
- It creates a new branch
- Get's your dependencies and commits them
- Then it will get your own configs provided in `config.yml` and applies them and commits your changes


## Requirements
- Own Marlin fork
- Vscode if you want to use the devcontainer config
- Python 3.10

## Usage


## TODO
- [settings Management with pydantic](https://pydantic-docs.helpmanual.io/usage/settings/#customise-settings-sources)
- [change build settings interactivly](https://github.com/tmbo/questionary)