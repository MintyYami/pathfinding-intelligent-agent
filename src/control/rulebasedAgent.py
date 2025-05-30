import random

import numpy as np

from control.baseAgent import BaseAgent


class RBAgent(BaseAgent):
    def __init__(self, alpha=0.1):
        super().__init__()
        # % randomness of distance value
        self.alpha = alpha

    def _choose_action(self, agent):
        moves = self._get_valid_neighbours(agent)
        # stay still if no valid move
        moves.append(agent.pos)

        # find best move
        bestFitness = -np.inf
        bestMove = None
        for move in moves:
            fitness = self._fitness_function(move, agent)

            if fitness > bestFitness:
                bestFitness = fitness
                bestMove = move

        return bestMove

    def _fitness_function(self, move, agent):
        # best move: found target
        if move == agent.target_pos:
            return np.inf

        # heuristic calculation + random alpha weight to prevent circular
        score = (- self.manhattan_distance(move, agent.target_pos)
                 * (1 + round(random.uniform(-self.alpha, self.alpha), 2)))

        # discourage backtracking & staying constant
        if move == agent.prev_pos or move == agent.pos:
            score -= 2

        return score