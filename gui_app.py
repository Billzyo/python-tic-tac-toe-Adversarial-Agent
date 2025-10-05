"""Compatibility wrapper for the previous top-level GUI module.

This module re-exports the `tictactoe.gui` module so code that imports
`gui_app` continues to work.
"""

from tictactoe.gui import *  # noqa: F401,F403
