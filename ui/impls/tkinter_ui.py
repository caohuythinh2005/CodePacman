import math
from ..renderers import BaseDisplay
from . import graphicsUtils
from envs import layouts
from envs.game_state import GameState

class TkinterDisplay(BaseDisplay):
    def __init__(self, zoom: float = 1.0, frame_time: float = 0.0):
        super().__init__(zoom=zoom, frame_time=frame_time)
        self.grid_size = layouts.GRID_SIZE
        self.canvas = None
        self.shapes = {}       
        self.pacman_shape = None
        self.ghost_shapes = {}
        

        # Lấy hằng số từ layouts.py
        self.PACMAN_RADIUS = layouts.PACMAN_RADIUS
        self.FOOD_RADIUS = layouts.FOOD_RADIUS
        self.CAPSULE_RADIUS = layouts.CAPSULE_RADIUS
        self.GHOST_RADIUS = layouts.GHOST_RADIUS
        self.WALL_COLOR = layouts.WALL_COLOR
        self.WALL_OUTLINE = layouts.WALL_OUTLINE
        self.FOOD_COLOR = layouts.FOOD_COLOR
        self.CAPSULE_COLOR = layouts.CAPSULE_COLOR
        self.PACMAN_COLOR = layouts.PACMAN_COLOR
        self.GHOST_COLORS = layouts.GHOST_COLORS
        self.SCARED_COLOR = layouts.SCARED_COLOR

    def initialize(self, state: GameState):
        h, w = state.object_matrix.shape
        graphicsUtils.begin_graphics(w * self.grid_size, (h + 1) * self.grid_size)

        self.canvas = graphicsUtils._canvas

        self.root = graphicsUtils._root_window

        self.score_id = graphicsUtils.text(
            (10, h * self.grid_size + 5), "white", "Score: 0"
        )


    def update(self, state: GameState):
        mat = state.object_matrix

        for y, row in enumerate(mat):
            for x, val in enumerate(row):
                pos = (x, y)

                # Wall
                if val == layouts.WALL:
                    if pos not in self.shapes:
                        x0, y0 = x * self.grid_size, y * self.grid_size
                        x1, y1 = x0 + self.grid_size, y0 + self.grid_size
                        self.shapes[pos] = self.canvas.create_rectangle(
                            x0, y0, x1, y1, fill=self.WALL_COLOR, outline=self.WALL_OUTLINE
                        )

                # Food / Capsule
                elif val in (layouts.FOOD, layouts.CAPSULE):
                    if pos not in self.shapes:
                        radius = self.CAPSULE_RADIUS if val == layouts.CAPSULE else self.FOOD_RADIUS
                        color = self.CAPSULE_COLOR if val == layouts.CAPSULE else self.FOOD_COLOR
                        sp = ((x + 0.5) * self.grid_size, (y + 0.5) * self.grid_size)
                        self.shapes[pos] = graphicsUtils.circle(sp, self.grid_size * radius, color, color)

                # Remove previous food/capsule
                else:
                    if pos in self.shapes and val not in (layouts.WALL, layouts.PACMAN,
                                                         layouts.GHOST1, layouts.GHOST2,
                                                         layouts.GHOST3, layouts.GHOST4):
                        graphicsUtils.remove_from_screen(self.shapes[pos])
                        del self.shapes[pos]

                # Pacman
                if val == layouts.PACMAN:
                    self._render_pacman(x, y, state.pacman.dir)

                # Ghosts
                if val in (layouts.GHOST1, layouts.GHOST2, layouts.GHOST3, layouts.GHOST4):
                    self._render_ghost(val, x, y, state)

        graphicsUtils.changeText(self.score_id, f"Score: {int(state.score)}")
        graphicsUtils.refresh()
        # graphicsUtils.sleep(self.frame_time)

    def _render_pacman(self, x, y, dir):
        if self.pacman_shape:
            graphicsUtils.remove_from_screen(self.pacman_shape)
        sp = (x * self.grid_size + self.grid_size / 2, y * self.grid_size + self.grid_size / 2)
        angles = {1: 90, 2: 0, 3: 270, 4: 180}.get(dir, 0)
        width = 30 + 80 * math.sin(math.pi * ((x % 1) + (y % 1)))
        self.pacman_shape = graphicsUtils.circle(
            sp, self.grid_size * self.PACMAN_RADIUS,
            self.PACMAN_COLOR, self.PACMAN_COLOR,
            endpoints=(angles + width / 2, angles - width / 2)
        )

    def _render_ghost(self, val, x, y, state):
        idx = val - layouts.GHOST1
        if idx in self.ghost_shapes:
            graphicsUtils.remove_from_screen(self.ghost_shapes[idx])
        sp = (x * self.grid_size + self.grid_size / 2, y * self.grid_size + self.grid_size / 2)
        color = self.SCARED_COLOR if getattr(state, 'is_ghost_scared', lambda i: False)(idx) else \
            self.GHOST_COLORS[idx % len(self.GHOST_COLORS)]
        self.ghost_shapes[idx] = graphicsUtils.circle(sp, self.grid_size * self.GHOST_RADIUS, color, color)

    def finish(self):
        graphicsUtils.end_graphics()

    def after(self, delay_ms, callback):
        from . import graphicsUtils
        if graphicsUtils._root_window:
            graphicsUtils._root_window.after(delay_ms, callback)

    def mainloop(self):
        from . import graphicsUtils
        if graphicsUtils._root_window:
            graphicsUtils._root_window.mainloop()

    def get_root(self): 
        return graphicsUtils._root_window
    
    
        return graphicsUtils._root_window