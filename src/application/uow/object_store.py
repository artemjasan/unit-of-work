from typing import Any

from src.application.uow.object_state import ObjectState


class ObjectStore:
    def __init__(self) -> None:
        self._store: dict[Any, ObjectState] = {}

    def attach(self, entity, state: ObjectState) -> None:
        print(self._store)
        self._store[entity] = state
        print(self._store)

    def detach(self, entity) -> None:
        if entity in self._store:
            del self._store[entity]
        else:
            raise ValueError(f"Object {entity} is not stored")

    def is_new(self, entity) -> bool:
        if entity not in self._store:
            return False

        return self._store[object] == ObjectState.NEW

    def is_dirty(self, entity) -> bool:
        if entity not in self._store:
            return False

        return self._store[object] == ObjectState.DIRTY

    def is_removed(self, entity) -> bool:
        if entity not in self._store:
            return False

        return self._store[object] == ObjectState.REMOVED

    def items(self) -> set[tuple[Any, ObjectState]]:
        return {(items[0], items[1]) for items in self._store.items()}

    def clear(self) -> None:
        self._store.clear()
