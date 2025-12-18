"""
UI Implementations Package (impls)

Concrete implementations of abstract UI interfaces for different frameworks.

Available:
- tkinter: Tkinter/Tk GUI (graphical)
- console: Console/text mode (terminal)
- (future) pygame: Pygame
- (future) web: HTML5/WebSocket
"""

"""
UI Implementations Package (impls)

Concrete implementations of abstract UI interfaces for different frameworks.

This module only imports available submodules. Missing optional UI backends
will be ignored so that headless command-line usage does not fail when a
GUI/backend dependency or file is absent.
"""

__all__ = []

import warnings

# Try to import the Tkinter-based UI (optional)
try:
    from .tkinter import (
        TkinterDisplay,
        TkinterFoodRenderer,
        TkinterGhostRenderer,
        TkinterInfoPane,
        TkinterPacmanRenderer,
        TkinterWallRenderer,
    )

    __all__.extend(
        [
            "TkinterDisplay",
            "TkinterInfoPane",
            "TkinterPacmanRenderer",
            "TkinterGhostRenderer",
            "TkinterFoodRenderer",
            "TkinterWallRenderer",
        ]
    )
except Exception as e:  # pragma: no cover - optional dependency
    warnings.warn(f"Tkinter UI implementation not available: {e}")


# The console implementation has been removed from the codebase.
# Provide a minimal NullDisplay here so headless training and tests
# can continue to import `NullDisplay` from `ui.impls` without
# depending on a separate console backend module.


class NullDisplay:
    """Minimal no-op display used for headless runs or training.

    Methods mirror the display interface used by the game loop:
    - `initialize(stateData)` called once at start
    - `update(stateData)` called every frame
    - `finish()` called at the end
    """

    def initialize(self, stateData):
        return None

    def update(self, stateData):
        return None

    def finish(self):
        return None


__all__.extend(["NullDisplay"])
