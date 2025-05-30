import heapq

from control.baseAgent import BaseAgent

class AStarAgent(BaseAgent):
    def __init__(self):
        # to store planned paths
        self.paths = {}

    def _choose_action(self, agent):
        move = agent.target_pos
        if move is None:
            return None

        path = self._a_star(agent.pos, move, agent.orderItem)
        if len(path) >= 2:
            return path[1]  # path[0] is current position
        return None

    def _a_star(self, start, goal, target_val):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.manhattan_distance(start, goal)}

        visited = set()

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                return self._reconstruct_path(came_from, current)

            if current in visited:
                continue
            visited.add(current)

            for neighbor in self.model.get_neighbours(current):
                if not self._validate_move(neighbor, target_val):
                    continue
                # Don't path through other agents
                if any(other.pos == neighbor for other in self.model.agents if other.pos != start):
                    continue

                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.manhattan_distance(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return [start]  # return cur pos if no path found (blocked by dead agents)

    def _reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.insert(0, current)
        return path