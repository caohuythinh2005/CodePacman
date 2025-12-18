import random
from .agent import Agent
from envs.directions import Directions
from typing import Any
from envs.directions import Directions, Actions
from envs.game_state import GameState

class RandomAgent(Agent):
    def getAction(self, gameState: GameState) -> str:
        legalMoves = gameState.getLegalActions(self.index)
        return random.choice(legalMoves)
