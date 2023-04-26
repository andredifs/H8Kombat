from argparse import ArgumentParser
from paths import VENV

from scripts.setup import setup

if __name__ == '__main__':
    """
    Main entry point for the package management system.
    """

    if not VENV.is_dir():
        """
        If the virtual environment directory does not exist, set it up.
        """
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
        """
        If the command is 'setup', execute the setup command.
        """
        setup(setup_parser)

    if args.cmd == 'run':
        """
        If the command is 'run', run the game with the specified arguments.
        """
        __import__('scripts.run').run.run(run_parser)

    args = parser.parse_args()

    try:
        """
        Execute the function specified by the arguments.
        """
        args.func(args)
    except KeyboardInterrupt:
        """
        If the user interrupts the program with Ctrl+C, exit with status code 1.
        """
        print('Aborted.')
        exit(1)
