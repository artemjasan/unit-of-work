from src.application.protocols.unit_of_work import UnitOfWorkProtocol
from src.application.uow.object_store import ObjectStore
from src.application.uow.object_state import ObjectState
from src.application.uow.map_registry import MapperRegistry


class UnitOfWork(UnitOfWorkProtocol):
    def __init__(
        self,
        registry: MapperRegistry,
        object_store: ObjectStore | None,
    ) -> None:
        self._registy = registry
        self._object_store = object_store if object_store else ObjectStore()

    def register_new(self, entity) -> None:
        self._ensure_not_registered(entity)
        self._object_store.attach(entity, ObjectState.NEW)

    def register_dirty(self, entity) -> None:
        if self._object_store.is_removed(entity):
            raise ValueError(f"Entity {entity} is already registered as removed")

        if self._object_store.is_dirty(entity) or self._object_store.is_new(entity):
            return None

        self._object_store.attach(entity, ObjectState.DIRTY)

    def register_removed(self, entity) -> None:
        if self._object_store.is_new(entity):
            return self._object_store.detach(entity)

        if self._object_store.is_dirty(entity):
            return self._object_store.detach(entity)

        if not self._object_store.is_removed(entity):
            self._object_store.attach(entity, ObjectState.REMOVED)

    def regitered_clean(self, entity) -> None:
        self._object_store.attach(entity, ObjectState.CLEAN)

    def commit(self) -> None:
        for entity, state in self._object_store.items():
            mapper = self._registy.get(type(entity))
            match state:
                case ObjectState.NEW:
                    mapper.insert(entity)
                case ObjectState.DIRTY:
                    mapper.update(entity)
                case ObjectState.REMOVED:
                    mapper.delete(entity)

        self._object_store.clear()

    def _ensure_not_registered(self, entity) -> None:
        if self._object_store.is_dirty(entity):
            raise ValueError(f"Entity {entity} is already registered as dirty")

        if self._object_store.is_removed(entity):
            raise ValueError(f"Entity {entity} is already registered as removed")

        if self._object_store.is_new(entity):
            raise ValueError(f"Entity {entity} is already registered as new")
