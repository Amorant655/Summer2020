import asyncio
from typing import Optional
from task1.database import DataBase
from task1.imitator import MyVar, VarImitator
from task3and4plus7.web_interface import WebApi, Handler
from task3and4plus7.mosq import start_coroutine
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel


# did the same as https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "fakehashedsecret",
    },
    "alice": {
        "username": "alice",
        "hashed_password": "fakehashedsecret2",
    },
}


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


app = WebApi()
data_base = DataBase()
var_imitator = VarImitator()
imitate = False


async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

h = Handler('/token', login)
h.descr = 'post request to get token'
app.add_post_handler(h)


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


async def start_mqtt(topic: str, name: str, current_user: User = Depends(get_current_user)):
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
