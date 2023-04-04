from argparse import ArgumentParser
from paths import VENV

from scripts.setup import setup

if __name__ == '__main__':
    if not VENV.is_dir():
        setup()

    parser = ArgumentParser(
        description='Manage packages for the project.',
    )

    cmds = parser.add_subparsers(dest='cmd', required=True)

    setup_parser = cmds.add_parser(
        'setup',
        help='Setup the environment',
    )

    run_parser = cmds.add_parser(
        'run',
        help='Run game',
    )

    run_parser.add_argument('--dev', action='store_true')

    args = parser.parse_args()

    if args.cmd == 'setup':
        setup(setup_parser)

    if args.cmd == 'run':
        __import__('scripts.run').run.run(run_parser)

    args = parser.parse_args()

    try:
        args.func(args)
    except KeyboardInterrupt:
        print('Aborted.')
        exit(1)
