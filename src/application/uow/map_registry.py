from typing import Type

from src.application.protocols.mapper import DataMapperProtocol, EntityT


class MapperRegistry:
    def __init__(self) -> None:
        self._mappers = {}

    def get(self, __key: Type[EntityT]) -> DataMapperProtocol[EntityT]:
        mapper = self._mappers.get(__key)

        if mapper is None:
            raise KeyError(f"Mapper for {__key} not registered")

        return mapper

    def register(
        self, entity: Type[EntityT], mapper: DataMapperProtocol[EntityT]
    ) -> None:
        self._mappers[entity] = mapper

    def unregister(self, entity: Type[EntityT]) -> None:
        if entity in self._mappers:
            del self._mappers[entity]
        else:
            raise KeyError(f"Mapper for {entity} not registered")
