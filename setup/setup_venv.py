import json
import os

def update_requirements():
    pass

def install_venvs(venvs, **kwargs):
    pass

def main():
    with open('virtualenvs.json') as f:
        data = json.load(f)

        print('\033[0;33mInstalling virtualenvs...\033[0m')
        install_venvs(**data)

        print('\033[0;33mUpdating requirements...\033[0m')
        update_requirements(**data)

    print('\033[0;32mAll virtualenvs have been set up!\033[0m')


if __name__ == '__main__':
    main()
