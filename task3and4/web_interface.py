import asyncio
from fastapi import FastAPI
from uvicorn import Server, Config


class Handler:
    def __init__(self, path, f):
        self.func = f
        self.descr = ''
        self.path = path

    def get_dict(self):
        return {"path": self.path, "usage": self.descr}


class WebApi:
    def __init__(self):
        self._web = FastAPI(docs_url=None, redoc_url=None)
        self._bind_web_api()
        self._handler_mass = []

    def _bind_web_api(self):
        @self._web.get('/help')
        async def info():
            return {
                "funcs": [a.get_dict() for a in self._handler_mass]
                }

    def add_handler(self, handler: Handler):
        self._handler_mass.append(handler)
        self._web.get(handler.path)(handler.func)

    def start(self):
        loop = asyncio.get_event_loop()
        config = Config(app=self._web, host="0.0.0.0", port=8083)
        server = Server(config)
        if loop.is_running():
            loop.create_task(server.serve())
        else:
            loop.run_until_complete(server.serve())  # run server loop
