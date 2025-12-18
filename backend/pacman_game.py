import numpy as np
from envs.game_state import GameState, AgentInfo, GhostInfo, serialize_state
from envs import layouts
from ui.renderers import BaseDisplay

class PacmanGame:
    def __init__(self, map_file: str, display: BaseDisplay = None):
        self.map_file = map_file
        self.state = self.load_map(map_file)
        self.last_actions = {}
        self.display = display

        # Nếu có display, khởi tạo cửa sổ và vẽ các vật thể tĩnh ban đầu
        if self.display:
            self.display.initialize(self.state)

    def load_map(self, file_path: str) -> GameState:
        with open(file_path, "r") as f:
            lines = [line.rstrip("\n") for line in f if line.strip()]

        H, W = len(lines), len(lines[0])
        object_matrix = np.zeros((H, W), dtype=int)
        pacman = None
        ghosts = []

        for y, line in enumerate(lines):
            for x, ch in enumerate(line):
                if ch == '%':
                    object_matrix[y, x] = layouts.WALL
                elif ch == '.':
                    object_matrix[y, x] = layouts.FOOD
                elif ch == 'o':
                    object_matrix[y, x] = layouts.CAPSULE
                elif ch == 'P':
                    object_matrix[y, x] = layouts.PACMAN
                    pacman = AgentInfo(x=x, y=y, dir=2)
                elif ch == 'G':
                    ghost_id = len(ghosts)
                    object_matrix[y, x] = getattr(layouts, f"GHOST{ghost_id+1}", layouts.GHOST1)
                    ghosts.append(GhostInfo(x=x, y=y, dir=0, scared_timer=0))
                else:
                    object_matrix[y, x] = layouts.EMPTY

        return GameState(
            object_matrix=object_matrix,
            pacman=pacman,
            ghosts=ghosts,
            score=0.0,
            win=False,
            lose=False
        )

    def get_state(self) -> GameState:
        return self.state

    def serialize_state(self) -> dict:
        return serialize_state(self.state)

    def move_pacman(self, action: str):
        pac = self.state.pacman
        action_map = {"North": 1, "East": 2, "South": 3, "West": 4}
        if action in action_map:
            pac.dir = action_map[action]

        # TODO: Tính nx, ny dựa trên dir, kiểm tra tường
        print(f"[Debug] Pacman at ({pac.x}, {pac.y}) moves {action}")

    def move_ghosts(self):
        for g in self.state.ghosts:
            # TODO: AI di chuyển ghost
            print(f"[Debug] Ghost at ({g.x}, {g.y}) moves randomly")

    def apply_action(self, agent_idx: int, action: str):
        self.last_actions[agent_idx] = action
        if agent_idx == 0:
            self.move_pacman(action)
        else:
            self.move_ghosts()

        # Cập nhật giao diện
        self.draw_ui()

    def check_game_over(self) -> bool:
        if self.state.win or self.state.lose:
            if self.display:
                self.display.finish()
            return True
        return False

    def draw_ui(self):
        if self.display:
            self.display.update(self.state)
        else:
            print(f"Score: {self.state.score} | Last actions: {self.last_actions}")

    def update_score(self, delta: float):
        self.state.score += delta
        self.draw_ui()
