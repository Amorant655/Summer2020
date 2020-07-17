from task1.imitator import VarImitator
from task1.database import DataBase
import random
import time


class LoopStopper:
    run = True

    @classmethod
    def stop(cls):
        cls.run = False


def infinity_imitation_loop():
    vi = VarImitator()
    db = DataBase()
    for a in "opertsza":
        vi.add_var(a, 20 * random.random())
    while True:
        db.write_data(vi.get_var_dict())
        vi.imitate_change()
        time.sleep(1)


if __name__ == "__main__":
    infinity_imitation_loop()