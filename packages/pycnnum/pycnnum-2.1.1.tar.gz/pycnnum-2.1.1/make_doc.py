"""Create documents in /doc folder using pdoc
"""

import os
import shlex
import shutil
import sys
from pathlib import Path

from pdoc.__main__ import cli

from pycnnum import __version__

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    shutil.rmtree("doc", ignore_errors=True)
    cmd = f"pdoc pycnnum test -d google -o doc --math --footer-text PyCNNum-{__version__}"
    sys.argv = shlex.split(cmd)
    cli()
