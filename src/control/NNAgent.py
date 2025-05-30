import os

import pandas as pd
from joblib import load
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from control.baseAgent import BaseAgent
import random

class NNAgent(BaseAgent):
    def __init__(self):
        self.clf = load(os.path.join("control", "training_data", "NN-CLF-trainer.joblib"))
        self.encoder = load(os.path.join("control", "training_data", "NN-encoder.joblib"))
        self.scaler = load(os.path.join("control", "training_data", "NN-scaler.joblib"))

    def _choose_action(self, agent):
        encoded_move = self.clf.predict(self._preprocess_encode(self._encode_state(agent)))
        return self.decode_move(agent, encoded_move)

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
        match encoded[0]:
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

        neighbour_col = ["at_up", "at_down", "at_left", "at_right"]
        transformed_columns = self.encoder.transform(df[neighbour_col])
        df_dropped = df.drop(columns=neighbour_col)

        df_encoded = pd.concat([df_dropped, transformed_columns], axis=1)

        return self.scaler.transform(df_encoded)