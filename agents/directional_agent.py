import random
from .agent import Agent
from envs.directions import Directions
from envs.game_state import GameState

class DirectionalAgent(Agent):
    def getAction(self, gameState: GameState) -> str:
        legal = gameState.getLegalActions(self.index)
        if not legal:
            return random.choice([Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST])

        x, y = gameState.getAgentPosition(self.index)
        pac_x, pac_y = gameState.getPacmanPosition()

        dx = pac_x - x
        dy = pac_y - y

        candidates = []
        if abs(dx) >= abs(dy):
            if dx > 0: candidates.append(Directions.EAST)
            elif dx < 0: candidates.append(Directions.WEST)
            if dy > 0: candidates.append(Directions.SOUTH)
            elif dy < 0: candidates.append(Directions.NORTH)
        else:
            if dy > 0: candidates.append(Directions.SOUTH)
            elif dy < 0: candidates.append(Directions.NORTH)
            if dx > 0: candidates.append(Directions.EAST)
            elif dx < 0: candidates.append(Directions.WEST)

        for action in candidates:
            if action in legal:
                return action

        return random.choice(legal)
