import random
import numpy as np
from model.modelAgent import ModelAgent

class Model:
    def __init__(self, grid_size, num_agents, order_size):
        # set initial values
        self.grid_size = grid_size
        self.num_agents = min(num_agents, self.grid_size[1])  # agent must not be greater than row size due to max charge station
        self.shelf_id = 4
        self.timeStep = 0
        # data lists
        self.grid = np.zeros(grid_size, dtype=int)
        self.grid_copy = np.zeros(grid_size, dtype=int)
        self.agents = []
        self.order_list = []
        # populate data structs
        self._place_shelves(num_agents, num_agents)
        self._place_orders(order_size)
        self._spawn_agents()
        self.update_status()

    ### INITIALISE FUNCTIONS ###

    def _place_shelves(self, num_charger, num_dropoff):
        # add charging station (002), drop off location (003), and shelves (004+) to grid
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                # spawning shelves in the middle section
                if row > 1 and row < self.grid_size[0] - 2:
                    if (col == 0):
                        self.grid[row, col] = self.shelf_id
                        self.shelf_id += 1
                    elif self.grid_size[1] - col > 1:
                        if col % 3 != 1 and row % 7 != 1 and row % 7 != 0:
                            self.grid[row, col] = self.shelf_id
                            self.shelf_id += 1
                    elif self.grid_size[1] % 3 == 0:
                        self.grid[row, col] = self.shelf_id
                        self.shelf_id += 1
                # first row
                elif row == 0:
                    if num_charger > col:
                        # charging stations
                        self.grid[row, col] = 2
                    else:
                        self.grid[row, col] = self.shelf_id
                        self.shelf_id += 1
                # final row
                elif row == self.grid_size[0] - 1:
                    if self.grid_size[1] - 1 - num_dropoff < col:
                        # drop offs
                        self.grid[row, col] = 3
                    else:
                        self.grid[row, col] = self.shelf_id
                        self.shelf_id += 1

    def _spawn_agents(self):
        coorList = []
        for i in range(self.num_agents):
            while True:
                # randomise until on path + not already an agent there
                row = random.randint(0, self.grid_size[0] - 1)
                col = random.randint(0, self.grid_size[1] - 1)
                if self.grid[row, col] == 0 and (row, col) not in coorList:
                    self.agents.append(ModelAgent(self.grid_size, i, (row, col)))
                    coorList.append((row, col))
                    break

    def _place_orders(self, order_size):
        for _ in range(order_size):
            self.order_list.append(random.randint(4, self.shelf_id - 1))

    ### UPDATE AGENTS ###

    def update_status(self):
        for agent in self.agents:
            # update charge status: need charging
            if agent.energy < agent.energy_thresh:
                agent.charge = True
            # update charge status: charging complete
            if agent.energy == agent.energy_max:
                agent.charge = False

            # update when item picked up
            if agent.pos == self.id_to_pos(agent.orderItem) and (not agent.hasItem):
                agent.hasItem = True
            # update when item dropped off
            if agent.hasItem and self.grid[agent.pos] == 3:
                agent.hasItem = False
                agent.orderItem = None

            # update order item if alive & free
            if agent.energy > 0 and agent.orderItem is None and len(self.order_list) > 0:
                agent.orderItem = self.order_list.pop(0)

            # check target status
            if agent.charge:
                # target charger
                agent.target_pos = (0, agent.id)
            else:
                if agent.hasItem:
                    # target dropoff
                    agent.target_pos = (self.grid_size[0] - 1, self.grid_size[1] - 1 - agent.id)
                else:
                    # target item shelf
                    agent.target_pos = self.id_to_pos(agent.orderItem)

            # check agent charging
            if self.grid[agent.pos] == 2:
                agent.energy = min(agent.energy + 4, agent.energy_max)
            elif agent.energy > 0:
                agent.energy -= 1

    def id_to_pos(self, shelf_id):
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                if self.grid[row, col] == shelf_id:
                    return (row, col)
        return None

    ### GRID UTIL ###

    def copyGrid(self):
        self.grid_copy = self.grid.copy()
        return self.grid_copy

    def gridWithAgent(self):
        # add agents to grids
        self.grid_copy = self.copyGrid()
        for agent in self.agents:
            self.grid_copy[agent.pos] = 1
        return self.grid_copy

    def gridSameShelf(self, grid, target_val=None):
        # encode shelves to 4, encode 5 for target item shelf
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                if grid[row, col] == target_val:
                    grid[row, col]  = 5
                elif grid[row, col] > 4:
                    grid[row, col]  = 4
        return grid

    def printAgents(self):
        str = ""
        for agent in self.agents:
            str += f" [{agent.print()}] "
        return str

    def get_neighbours(self, pos):
        row = pos[0]
        col = pos[1]
        return [
            (row - 1, col), # up
            (row + 1, col), # down
            (row, col - 1), # left
            (row, col + 1), # right
        ]

    def get_neighbour_encoded(self, agent):
        self.grid_copy = self.gridSameShelf(self.gridWithAgent(), agent.orderItem)
        neighbours = self.get_neighbours(agent.pos)
        encoded = []

        for n in neighbours:
            row, col = n
            # edges
            if row < 0 or row > self.grid_size[0] - 1:
                encoded.append(-1)
            elif col < 0 or col > self.grid_size[1] - 1:
                encoded.append(-1)
            # other blocks
            else:
                encoded.append(self.grid_copy[row][col])
        return encoded