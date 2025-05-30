from view.baseView import BaseView

class TextView(BaseView):
    def render(self):
        # get grid with agents
        showGrid = self.model.gridWithAgent()
        # show grid
        for row in showGrid:
            print(" ".join(str(cell).zfill(3) for cell in row))
        # separate views
        print()

    def endView(self):
        pass