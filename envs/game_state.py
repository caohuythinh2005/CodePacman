from dataclasses import dataclass
import numpy as np
from envs.directions import Actions  # import class Actions

@dataclass
class GameState:
    object_matrix: np.ndarray
    infor_vector: np.ndarray
    score: float
    win: bool = False
    lose: bool = False

    def copy(self) -> "GameState":
        return GameState(
            object_matrix=self.object_matrix.copy(),
            infor_vector=self.infor_vector.copy(),
            score=self.score,
            win=self.win,
            lose=self.lose,
        )

    # ---- Query helpers ----
    def pacman_pos(self):
        return int(self.infor_vector[0]), int(self.infor_vector[1])

    def ghost_pos(self, i: int):
        idx = 2 + i * 2
        return int(self.infor_vector[idx]), int(self.infor_vector[idx + 1])

    def num_food_left(self):
        return int(self.infor_vector[17])

    def isWin(self):
        return self.win

    def isLose(self):
        return self.lose

    # ---- Legal Actions ----
    def getLegalActions(self, agent_index: int):
        """
        agent_index == 0: Pacman
        agent_index >= 1: Ghosts
        """
        if agent_index == 0:
            pos = self.pacman_pos()
        else:
            pos = self.ghost_pos(agent_index - 1)

        walls = self.object_matrix == 1
        return Actions.getLegalActions(pos, walls)
    

def serialize_state(state: GameState) -> dict:
    """Chuyển GameState thành dict để serialize JSON"""
    return {
        "object_matrix": state.object_matrix.tolist(),
        "infor_vector": state.infor_vector.tolist(),
        "score": state.score,
        "win": state.win,
        "lose": state.lose
    }

def deserialize_state(state_dict: dict) -> GameState:
    """Chuyển dict JSON thành GameState"""
    return GameState(
        object_matrix=np.array(state_dict["object_matrix"]),
        infor_vector=np.array(state_dict["infor_vector"]),
        score=state_dict["score"],
        win=state_dict["win"],
        lose=state_dict["lose"]
    )
