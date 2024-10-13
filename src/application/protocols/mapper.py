from typing import Protocol, TypeVar


EntityT = TypeVar("EntityT")


class DataMapperProtocol(Protocol[EntityT]):
    def insert(self, entity: EntityT) -> None:
        raise NotImplementedError

    def update(self, entity: EntityT) -> None:
        raise NotImplementedError

    def delete(self, entity: EntityT) -> None:
        raise NotImplementedError
