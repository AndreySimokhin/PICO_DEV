from typing import Any, Iterator
from pydantic import BaseModel, ValidationError
import aiofile
import json

from exceptions import Config_Error, Unknown_Entity, Incorrect_Value


class Element(BaseModel):
    entry_id: str
    title: str | None = None
    data: dict[str, Any] = {}
    options: dict[str, Any] = {}

class ElementDict(BaseModel):
    __root__: dict[str, BaseModel] = {}

class Config:
    def __init__(self, path: str = 'config.json'):
        self.path = path
        self.base = ElementDict(__root__={})
        self.entries = self.base.__root__
    
    def items(self) -> dict[str, BaseModel]:
        return self.entries

    def keys(self) -> list[str]:
        return self.entries.keys()
    
    async def load_config(self) -> dict[str, BaseModel]:
        async with aiofile.async_open(self.path, 'r+') as afp:
            data = json.loads(await afp.read())
            self.entries = {}
            for key, val in data.items():
                self.entries.update({key: Element(**val)})
        return self.entries

    async def save_config(self) -> None:
        async with aiofile.async_open(self.path, 'w+') as afp:
            await afp.write(self.base.json(indent = 4))

    async def __save_item__(self, entry: Element):
        if entry.entry_id not in self.keys(): self.entries[entry.entry_id] = entry
        await self.save_config()

    async def __remove_item__(self, entry: Element):
        del self.entries[entry.entry_id]
        await self.save_config()
    
    async def add(self, entry: Element) -> None:
        '''Add and setup an entry.'''
        if entry.entry_id in self.entries:
            raise Config_Error(f'An entry with the id: {entry.entry_id} already exist')
        await self.__save_item__(entry)

    async def remove(self, entry_id: str) -> None:
        entry = self.__getitem__(entry_id)
        if entry == None:
            raise Unknown_Entity
        await self.__remove_item__(entry)

    async def update_entry(
            self, 
            entry: Element,
            entry_id: str | None = None,
            title: str | None = None,
            data: dict[str, Any] | None = None,
            options: dict[str, Any] | None = None
        ) -> None:
        '''Update a config entry.'''
        try:
            if entry_id is not None: entry.entry_id = entry_id
            elif title is not None: entry.title = title
            elif data is not None: entry.data = data
            elif options is not None: entry.options = options
        except ValidationError as e:
            assert Incorrect_Value(e)
        await self.__save_item__(entry)

    async def __setitem__(self, entry_id: str, entry: Element) -> None:
        if self.entries[entry_id]: await self.update_entry(self.entries[entry_id], entry.entry_id, entry.title, entry.data, entry.options)
        else: await self.add(entry)

    async def __delitem__(self, entry_id: str):
        await self.remove(entry_id)

    def __getitem__(self, entry_id: str) -> Element | None:
        return self.entries.get(entry_id)

    def __repr__(self) -> str:
        return repr(self.entries)

    def __len__(self) -> int:
        return len(self.entries)

    def __contains__(self, entry: Element) -> bool:
        return entry in self.entries

    def __iter__(self) -> Iterator[Element]:
        return iter(self.entries)
    
    def __str__(self) -> str:
        return str(self.base.json())