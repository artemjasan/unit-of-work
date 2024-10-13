from sqlite3 import Connection

from src.application.uow.map_registry import MapperRegistry
from src.application.uow.unit_of_work import UnitOfWork


class SQLiteUnitOfWork(UnitOfWork):
    def __init__(self, connection: Connection, registry: MapperRegistry) -> None:
        super().__init__(registry)
        self._conneciton = connection

    def commit(self) -> None:
        self._conneciton.execute("BEGIN")

        try:
            super().commit()
        except Exception:
            self._connection.execute("ROLLBACK")
            raise

        self._connection.execute("COMMIT")
