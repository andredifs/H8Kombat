from argparse import ArgumentParser
import subprocess as sp
from sys import executable as py
from paths import VENV, ROOT
import os

# Cria um ambiente virtual e instala as dependências
def setup(parser: ArgumentParser = None):
    def _setup(_):
        if not VENV.is_dir():
            print('Creating virtual environment...')

            sp.run([py, '-m', 'venv', '.venv'], cwd=ROOT, check=True)

            print('Virtual environment created.')

        print('Installing dependencies...')

        if os.name == 'posix':
            _pip = str(VENV.joinpath('bin', 'pip').absolute())
        else:
            _pip = str(VENV.joinpath('Scripts', 'pip.exe').absolute())

        sp.run([_pip, 'install', '-r', 'requirements.txt'], cwd=ROOT, check=True)

        print('Dependencies installed.')

    if parser:
        parser.set_defaults(func=_setup)
