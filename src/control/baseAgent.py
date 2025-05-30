class BaseAgent:
    def __init__(self):
        self.model = None

    def initialise(self, model):
        self.model = model

    def _choose_action(self, agent):
        raise NotImplementedError

    def moveAgents(self):
        for agent in self.model.agents:
            # don't move if no target
            if agent.target_pos is None:
                continue
            # check has energy to move
            if agent.energy > 0:
                bestMove = self._choose_action(agent)

                if None != bestMove:
                    # move agent
                    agent.prev_pos = agent.pos
                    agent.pos = bestMove

            # return target order back to list, as no longer able to complete (dead)
            elif agent.orderItem is not None:
                self.model.order_list.insert(0, agent.orderItem)
                agent.orderItem = None

        # update model info
        self.model.update_status()
        self.model.timeStep += 1

    def manhattan_distance(self, from_pos, to_pos):
        return abs(to_pos[0] - from_pos[0]) + abs(to_pos[1] - from_pos[1])

    def _validate_move(self, pos_to, target_val):
        row, col = pos_to

        if row < 0 or row > self.model.grid_size[0]-1:
            return False
        if col < 0 or col > self.model.grid_size[1]-1:
            return False

        grid = self.model.gridSameShelf(self.model.gridWithAgent() , target_val)
        if grid[pos_to] == 1 or grid[pos_to] == 4:
            return False

        return True

    def _get_valid_neighbours(self, agent):
        valid = []
        for move in self.model.get_neighbours(agent.pos):
            if self._validate_move(move, agent.orderItem):
                valid.append(move)
        return valid

    def encode_move(self, agent_pos, mov):
        if mov is None:
            return 4 # stay (for invalid mov)

        row_pos, col_pos = agent_pos
        row_mov, col_mov = mov
        if col_pos == col_mov:
            if row_pos - 1 == row_mov:
                return 0 # up
            if row_pos + 1 == row_mov:
                return 1  # down
        if row_pos == row_mov:
            if col_pos - 1 == col_mov:
                return 2 # left
            if col_pos + 1 == col_mov:
                return 3  # right
        return 4

    def decode_move(self, agent, encoded):
        movesID = self.model.get_neighbours(agent.pos)
        match int(encoded[0]):
            case 0:
                if self._validate_move(agent.pos, movesID[0]):
                    return movesID[0] # up
            case 1:
                if self._validate_move(agent.pos, movesID[1]):
                    return movesID[1] # down
            case 2:
                if self._validate_move(agent.pos, movesID[2]):
                    return movesID[2] # left
            case 3:
                if self._validate_move(agent.pos, movesID[3]):
                    return movesID[3] # right
            case _:
                return agent.pos  # stay
        return agent.pos