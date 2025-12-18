"""
Tkinter Wall Renderer Implementation (Classic Pac-Man Style)

Renders maze walls as continuous neon-like outlines around wall blocks.
"""

from ..wall_renderer import WallRenderer
from .graphicsUtils import formatColor

# Constants
WALL_COLOR = "#0033FF"  # Classic Pac-Man blue
WALL_THICKNESS = 2  # Thickness of inner blue line
WALL_GLOW_WIDTH = 2  # Glow line thickness
WALL_GLOW = "#3355FF"  # Outer glow (lighter blue)


def add(pos, delta):
    return (pos[0] + delta[0], pos[1] + delta[1])


class TkinterWallRenderer(WallRenderer):
    """
    Tkinter implementation of Wall renderer.
    Draws continuous outline around wall regions (Pac-Man arcade style).
    """

    def __init__(self, canvas, gridSize, height=None):
        self.canvas = canvas
        self.gridSize = gridSize
        self.height = height

    def renderWalls(self, wallGrid):
        """
        Draw outline edges between wall and empty cells to form the maze.
        """
        # Draw each wall cell as a filled block with a blue border to avoid seams
        half = self.gridSize / 2.0
        inner_inset = max(1.0, self.gridSize * 0.15)
        bg = formatColor(0, 0, 0)

        for x in range(wallGrid.width):
            for y in range(wallGrid.height):
                if not wallGrid[x][y]:
                    continue

                sx, sy = self._toScreen((x, y))
                x0 = sx - half
                y0 = sy - half
                x1 = sx + half
                y1 = sy + half

                # Glow/background outer rectangle (slightly larger)
                glow_id = self.canvas.create_rectangle(
                    x0 - 1, y0 - 1, x1 + 1, y1 + 1, outline=WALL_GLOW, fill=WALL_GLOW
                )
                # Main blue block
                main_id = self.canvas.create_rectangle(
                    x0, y0, x1, y1, outline=WALL_COLOR, fill=WALL_COLOR
                )
                # Inner cut-out to create the corridor effect (fill with background)
                inner_id = self.canvas.create_rectangle(
                    x0 + inner_inset,
                    y0 + inner_inset,
                    x1 - inner_inset,
                    y1 - inner_inset,
                    outline=bg,
                    fill=bg,
                )

                try:
                    self.canvas.addtag_withtag("walls", glow_id)
                    self.canvas.addtag_withtag("walls", main_id)
                    self.canvas.addtag_withtag("walls", inner_id)
                except Exception:
                    pass

    # -----------------------------------------------------------------
    # Edge & corner rendering
    # -----------------------------------------------------------------
    def _drawEdge(self, x, y, direction):
        """Draws one edge segment between wall and empty space."""
        sx, sy = self._toScreen((x, y))
        g = self.gridSize * 0.5

        if direction == "N":
            p1, p2 = (sx - g, sy - g), (sx + g, sy - g)
        elif direction == "S":
            p1, p2 = (sx - g, sy + g), (sx + g, sy + g)
        elif direction == "W":
            p1, p2 = (sx - g, sy - g), (sx - g, sy + g)
        else:  # "E"
            p1, p2 = (sx + g, sy - g), (sx + g, sy + g)

        # Glow layer
        id_glow = self.canvas.create_line(
            p1[0],
            p1[1],
            p2[0],
            p2[1],
            fill=WALL_GLOW,
            width=WALL_GLOW_WIDTH,
            capstyle="butt",
        )
        try:
            self.canvas.addtag_withtag("walls", id_glow)
        except Exception:
            pass
        # Main blue line
        id_main = self.canvas.create_line(
            p1[0],
            p1[1],
            p2[0],
            p2[1],
            fill=WALL_COLOR,
            width=WALL_THICKNESS,
            capstyle="butt",
        )
        try:
            self.canvas.addtag_withtag("walls", id_main)
        except Exception:
            pass

    def _drawCorners(self, x, y, wallGrid):
        """Draw rounded *outer* corners, skip inner and junction corners."""
        # Simplified: do not draw rounded arcs — keep straight edges only.
        # This removes curved corners and avoids small rendering artifacts.
        return

    def _drawArc(self, x0, y0, x1, y1, start, extent):
        """Draw perfectly aligned rounded corner."""
        inset = self.gridSize * 0.1  # dịch cung vào trong để khớp với cạnh
        id_arc = self.canvas.create_arc(
            x0 + inset,
            y0 + inset,
            x1 - inset,
            y1 - inset,
            start=start,
            extent=extent,
            style="arc",
            outline=WALL_COLOR,
            width=WALL_THICKNESS,
        )
        try:
            self.canvas.addtag_withtag("walls", id_arc)
        except Exception:
            pass

    # -----------------------------------------------------------------
    # Original helper methods (unchanged)
    # -----------------------------------------------------------------
    def _isWall(self, x, y, wallGrid):
        if x < 0 or x >= wallGrid.width:
            return False
        if y < 0 or y >= wallGrid.height:
            return False
        return wallGrid[x][y]

    def _toScreen(self, pos):
        x, y = pos
        x = (x + 1) * self.gridSize
        # Map grid Y directly: grid Y increases downward, same as Tkinter canvas
        y = (y + 1) * self.gridSize
        return (x, y)

    def _toScreen2(self, pos):
        x, y = pos
        x = (x + 1) * self.gridSize
        y = (y + 1) * self.gridSize
        return (x, y)

    def render(self, state):
        # Adapt GameState.object_matrix (numpy [H,W]) into the expected wallGrid interface
        matrix = state.object_matrix

        class _Col:
            def __init__(self, m, x):
                self.m = m
                self.x = x

            def __getitem__(self, y):
                return self.m[y, self.x]

        class WallGrid:
            def __init__(self, m):
                self._m = m
                self.width = m.shape[1]
                self.height = m.shape[0]

            def __getitem__(self, x):
                return _Col(self._m, x)

        self.renderWalls(WallGrid(matrix))


__all__ = ["TkinterWallRenderer"]
