"""Compatibility wrapper for legacy top-level module `L4`.

This file re-exports the `tictactoe.l4` package module so old imports like
`import L4 as l4` continue to work.
"""

from tictactoe.l4 import *  # noqa: F401,F403


