import os
import numpy as np
import pandas as pd
from joblib import load
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from control.baseAgent import BaseAgent
import random

class GAAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.final_weights = load(os.path.join("control", "training_data", "GAsolution.joblib"))
        self.scaler = load(os.path.join("control", "training_data", "GA-scaler.joblib"))

    def _choose_action(self, agent):
        input_state = self._preprocess_encode(self._encode_state(agent))

        # solution, solution_fitness, solution_idx = self.ga_instance.best_solution()

        weights = self.final_weights.reshape(11, 5)
        weights = np.mean(weights, axis=1)

        action_scores = np.dot(weights, input_state[0])
        predicted_action = np.argmax(action_scores)

        return self.decode_move(agent, predicted_action)

    def _encode_state(self, agent):
        grid = self.model.gridSameShelf(self.model.gridWithAgent() , agent.orderItem)
        neighbours = self.model.get_neighbour_encoded(agent)
        return (
            agent.pos[0], agent.pos[1], agent.target_pos[0], agent.target_pos[1], # agent_x, agent_y, target_x, target_y
            neighbours[0], neighbours[1], neighbours[2], neighbours[3], # at_up, at_down, at_left, at_right
            agent.hasItem, agent.energy, agent.charge # hasIte, energy, changed
        )

    def decode_move(self, agent, encoded):
        movesID = self.model.get_neighbours(agent.pos)
        id = None
        match encoded:
            case 0:
                id = 0
            case 1:
                id = 1
            case 2:
                id = 2
            case 3:
                id = 3
            case _:
                return agent.pos  # stay

        # validate before returning to ensure possible (if not, randomly find a valid move)
        movesID.append(agent.pos)
        tried = set()

        while not self._validate_move(movesID[id], agent.orderItem):
            tried.add(id)
            if len(tried) >= len(movesID):  # All moves tried
                return agent.pos
            id = random.choice([i for i in range(len(movesID)) if i not in tried])

        return movesID[id]

    def _validate_move(self, pos_to, target_val):
        row = pos_to[0]
        col = pos_to[1]

        if row < 0 or row > self.model.grid_size[0]-1:
            return False
        if col < 0 or col > self.model.grid_size[1]-1:
            return False

        grid = self.model.gridSameShelf(self.model.gridWithAgent() , target_val)
        if grid[pos_to] == 1 or grid[pos_to] == 4:
            return False

        return True

    def _preprocess_encode(self, encoded_input):
        state_columns = [
            "agent_x", "agent_y",
            "target_x", "target_y",
            "at_up", "at_down", "at_left", "at_right",
            "hasItem", "energy", "charge"
        ]

        # Create DataFrame
        df = pd.DataFrame([encoded_input], columns=state_columns)

        return self.scaler.fit_transform(df)