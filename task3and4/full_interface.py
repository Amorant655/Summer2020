import asyncio
from task1.database import DataBase
from task1.imitator import MyVar, VarImitator
from task3and4.web_interface import WebApi, Handler
from task3and4.mosq import start_coroutine

app = WebApi()
data_base = DataBase()
var_imitator = VarImitator()
imitate = False


async def async_imitation_loop(tts):
    global imitate
    while imitate:
        dc = var_imitator.get_var_dict()
        if dc:
            data_base.write_data(dc)
        var_imitator.imitate_change()
        await asyncio.sleep(tts)


async def start_imitate(tts: int):
    global imitate
    if imitate:
        return {"answer": "ERROR"}
    imitate = True
    loop = asyncio.get_event_loop()
    loop.create_task(async_imitation_loop(tts))
    return {"answer": "OK"}

h = Handler('/start', start_imitate)
h.descr = 'start imitation server, required param tts(time to sleep), it simulate changing on waking, and writes to db'
app.add_handler(h)


async def stop_imitate():
    global imitate
    if not imitate:
        return {"answer": "ERROR"}
    imitate = False
    return {"answer": "OK"}

h = Handler('/stop', stop_imitate)
h.descr = 'stops imitation server'
app.add_handler(h)


async def variable(name: str, bv: float = 1, flag: str = 'add'):
    if flag == 'add':
        var_imitator.add_var(name, bv)
        return {"answer": "OK"}
    elif flag == 'del':
        rt = var_imitator.del_var(name)
        if rt:
            return {"answer": "OK"}
        return {"answer": "ERROR"}
    return {"answer": "BADFLAG"}

h = Handler('/var', variable)
h.descr = 'add[add] or deleting[del] variable, use `flag` in query to set del'
app.add_handler(h)


async def all_v():
    ms = var_imitator.get_var_dict()
    return {"variables_count": len(ms), "vars": ms}

h = Handler('/all', all_v)
h.descr = 'returns count and variables whith their values'
app.add_handler(h)


async def start_mqtt(topic: str, name: str):
    def callback(a: float):
        var_imitator.add_var(name, a, False)
        return True
    start_coroutine(topic+'/'+name, callback)
    return {"answer": "OK"}

h = Handler('/mqtt', start_mqtt)
h.descr = 'starts mqtt listener, subscribes to topic/name'
app.add_handler(h)


if __name__ == "__main__":
    app.start()
