# from config import Config, Entry
import asyncio
import importlib
import logging
from typing import Any
import enum
from pydantic import BaseModel
import uuid

from exceptions import Core_Error


class CoreState(enum.Enum):
    not_running = "NOT_RUNNING"
    starting = "STARTING"
    running = "RUNNING"
    stopping = "STOPPING"
    final_write = "FINAL_WRITE"
    stopped = "STOPPED"

    def __str__(self) -> str:
        return self.value

class Event(BaseModel):
    ID: str = str(uuid.uuid4())
    title: str
    data: dict[str, Any] = []

class EventPool:
    def __init__(self):
        self._pool: list[Event] = []
        self.listeners: set[str] = set()
        self.is_alive = True
    
    async def listen(self):
        while is_alive:
            await asyncio.sleep(0)
            if not self._pool.isEmpty():
                yield self._pool.pop()

    def add_listener(self, title: str) -> None:
        self.listeners.append(title)

    def remove_listener(self, title: str) -> None:
        self.listeners.remove(title)

    def _push_event(self, event: Event) -> None:
        self.data.append(event)

class Core:
    def __init__(self, config_dir: str = 'config.json'):
        # self.config = Config(config_dir)
        self.loop: asyncio.EventLoop = asyncio.get_running_loop()
        self._logging = logging.getLogger(__name__)
        self._tasks: set[asyncio.Future[Any]] = set()
        self._state: CoreState = CoreState.not_running
        self._event_pools: set[EventPool] = set()

    async def start(self) -> int:
        _future = asyncio.run_coroutine_threadsafe(self.run(), self.loop)
        self.loop.run_forever()
        del _future
        return self._state

    async def run(self):
        if self.state is CoreState.running:
            self._logging.critical('Core already running')
            raise Core_Error
        
        self.state = CoreState.starting
        self._logging.info('Core starting up...')

        # push tasks to pull
        #
        #
        #

        asyncio.sleep(0)

        if self.state is not CoreState.starting:
            self._logging.critical('Core failed to start up...')
            raise Core_Error

    async def new_task(self, task: asyncio.Future) -> None:
        _future = self._loop.create_task(task)
        self._tasks.append(_furute)

    def flush_event(self, event: Event) -> None:
        for pool in self._event_pools:
            if event.title in pool.listeners:
                pool._push_event(event)