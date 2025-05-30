import tkinter as tk
from view.baseView import BaseView

CELL_SIZE = 30  # cell size

class TkView(BaseView):
    def __init__(self, model):
        super().__init__(model)
        self.root = tk.Tk()
        self.root.title("Warehouse Tkinter View")
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()

    def render(self):
        # get grid with agents
        showGrid = self.model.gridWithAgent()
        # get target & carrying list
        targets = []
        carrying = []
        for agent in self.model.agents:
            if agent.hasItem:
                carrying.append(agent.pos)
            else:
                targets.append(self.model.id_to_pos(agent.orderItem))

        rows = self.model.grid_size[0]
        cols = self.model.grid_size[1]

        self.canvas.config(width=cols * CELL_SIZE, height=rows * CELL_SIZE)
        self.canvas.delete("all")

        for row in range(rows):
            for col in range(cols):
                value = showGrid[row, col]

                # bg colour
                if value == 0:
                    color = "white" # pathway
                elif value == 1:
                    if (row, col) in carrying:
                        color = "blue2"
                    else:
                        color = "dodger blue" # agent
                elif value == 2:
                    color = "lime green" # charging station
                elif value == 3:
                    color = "saddle brown" # drop off
                elif (row, col) in targets:
                    color = "red" # target
                else:
                    color = "lightgray" # shelves

                # render block
                self.canvas.create_rectangle(
                    col * CELL_SIZE,
                    row * CELL_SIZE,
                    (col + 1) * CELL_SIZE,
                    (row + 1) * CELL_SIZE,
                    fill=color,
                    outline="black"
                )

                # add text to block
                if value != 1:
                    self.canvas.create_text(
                        col * CELL_SIZE + CELL_SIZE // 2,
                        row * CELL_SIZE + CELL_SIZE // 2,
                        text=str(value),
                        fill="black"
                    )
        # add text for agents
        for agent in self.model.agents:
            self.canvas.create_text(
                agent.pos[1] * CELL_SIZE + CELL_SIZE // 2,
                agent.pos[0] * CELL_SIZE + CELL_SIZE // 2,
                text=str("A" + str(agent.id)),
                fill="black"
            )
        self.root.update()

    def endView(self):
        self.root.destroy()