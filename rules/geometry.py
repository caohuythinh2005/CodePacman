from typing import Any, List, Optional, Tuple
import numpy as np
from envs.directions import Directions, Actions


def find_position(matrix: np.ndarray, code: int) -> Optional[Tuple[int, int]]:
    if matrix is None:
        return None
    
    H, W = matrix.shape
    for y in range(H):
        for x in range(W):
            if matrix[y, x] == code:
                return (x, y)
    return None

def in_bounds(pos: Tuple[int, int], shape: Tuple[int, int]) -> bool:
    x, y = pos
    H, W = shape
    return 0 <= x < W and 0 <= y < H

def is_walL(matrix: np.ndarray, pos: Tuple[int, int]) -> bool:
    x, y = pos
    return matrix[y, x] == 1

def next_position(pos: Tuple[int, int], action: str) -> Tuple[int, int]:
    dx, dy = Actions.directionToVector(action)
    x, y = pos
    return (x + dx, y + dy)


def compute_legal_actions(
    matrix: np.ndarray,
    pos: Tuple[int, int]
) -> List[str]:
    if matrix is None or pos is None:
        return []
    
    H, W = matrix.shape
    legal: List[str] = []
    for action in Directions.ALL:
        nx, ny = next_position(pos, action)
        if nx < 0 or ny < 0 or nx >= W or ny >= H:
            continue

        if matrix[ny, nx] == 1:
            continue

        legal.append(action)
    
    return legal

def build_wall_map(matrix: np.ndarray) -> np.ndarray:
    if matrix is None:
        return np.array([[]], dtype=bool)
    
    return matrix == 1