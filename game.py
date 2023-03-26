from argparse import ArgumentParser
from paths import VENV

from scripts import setup, run

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

    setup_parser.set_defaults(func=setup)
    run(run_parser)

    args = parser.parse_args()

    try:
        args.func(args)
    except KeyboardInterrupt:
        print('Aborted.')
        exit(1)