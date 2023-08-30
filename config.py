from typing import Any
from pydantic import BaseModel, ValidationError
import aiofile

from exceptions import Config_Error, Unknown_Entity, Incorrect_Value


class Element(BaseModel):
    entry_id: str
    title: str | None = None
    data: dict[str, Any] = []
    options: dict[str, Any] = []

class Config:
    def __init__(self):
        self.entries: dict[str, Element] = {}

    async def get_entries(self) -> dict[str, Element]:
        return self.entries
    
    async def get_ids(self) -> list[str]:
        return [entry.entry_id for entry in self.entries]

    async def get_entry(self, entry_id: str) -> Element | None:
        """Return entry with matching entry_id"""
        return self.entries.get(entry_id)
    
    async def add(self, entry: Element) -> None:
        """Add and setup an entry."""
        if entry.entry_id in self.entries:
            raise Config_Error(f"An entry with the id: {entry.entry_id} already exist")
        self.entries[entry.entry_id] = entry
        pass                                                            # SAVE

    async def remove(self, entry_id: str) -> bool:
        entry = await self.get_entry(entry_id)
        if entry == None:
            raise Unknown_Entity
        pass                                                            # REMOVE
        del self.entries[entry.entry_id]
        return True

    async def update_entry(
            self, 
            entry: Element, 
            **kwargs
        ):
        """Update a config entry."""
        try:
            entry.update(**kwargs)
        except ValidationError as e:
            assert Incorrect_Value(e)
        
        pass                                                            # SAVE
    
    async def load_config(self):
        pass                                                            #LOAD

    async def save_config(self):
        pass                                                            # SAVE ALL