class BaseView:
    def __init__(self, model):
        self.model = model

    def render(self):
        raise NotImplementedError

    def endView(self):
        raise NotImplementedError