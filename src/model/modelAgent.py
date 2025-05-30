class ModelAgent:
    def __init__(self, grid_size, agent_id, pos):
        self.energy_thresh = int((grid_size[0] + grid_size[1]) * 1.5)
        self.energy_max = grid_size[0] * grid_size[1]
        self.id = agent_id
        self.pos = pos
        self.prev_pos = (-1,-1)
        self.target_pos = None
        self.orderItem = None
        self.hasItem = False
        self.energy = self.energy_max
        self.charge = False

    def print(self):
        return (f"ID: {self.id}, POS: {self.pos}, TARGET: {self.orderItem} {self.target_pos}, "
              + f"hasItem: {self.hasItem}, energy: {self.energy}, charge: {self.charge}")