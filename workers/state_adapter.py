from typing import Dict, Any, Tuple, List, Optional
from envs.directions import Directions, Actions
from envs.game_state import GameState
from rules.geometry import compute_legal_actions, find_position, build_wall_map
import numpy as np

def adapt_state(raw_state: Dict[str, Any], agent_code: int) -> Dict[str, str]:
    if raw_state is None:
        return {
            "object_matrix": np.array([[]], dtype=int),
            "position": None,
            "legal_actions": [],
            "score": 0.0,
            "done": False,
        }
    
    gs = GameState(
        object_matrix=np.array(raw_state.get("object_matrix", []), dtype=int),
        infor_vector=np.array(raw_state.get("infor_vector", []), dtype=float),
        scrore=raw_state.get("score", 0.0),
        win=raw_state.get("win", False),
        lose=raw_state.get("lose", False),
    )

    pos: Optional[Tuple[int, int]] = find_position(gs.object_matrix, agent_code)

    if pos is not None:
        legal: List[str] = compute_legal_actions(
            matrix=gs.object_matrix,
            pos=pos
        )
    else:
        legal = []

    done = gs.isWin() or gs.isLose()

    obs: Dict[str, Any] = {
        "object_matrix": gs.object_matrix,
        "position": pos,
        "legal_actions": legal,
        "score": gs.scrore,
        "done": done,
    }

    return obs
