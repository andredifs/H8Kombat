from pathlib import Path

ROOT = Path(__file__).parent.resolve()

SCRIPTS = ROOT.joinpath('scripts')

INCLUDE = ROOT.joinpath('include')

VENV = ROOT.joinpath('.venv')

CONSTANTS = ROOT.joinpath('constants')
