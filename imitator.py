import random


class MyVar:
    def __init__(self):
        self.imitate = True
        self.value: float = 0


class VarImitator:
    def __init__(self):
        self._var = {}

    def add_var(self, name, val, imitate=True):
        self._var[name] = MyVar()
        self._var[name].value = val
        self._var[name].imitate = imitate

    def imitate_change(self):
        for a in self._var:
            if self._var[a].imitate:
                self._var[a].value += -1 + 2 * random.random()

    def get_var_dict(self):
        return {x: float(self._var[x].value) for x in self._var}