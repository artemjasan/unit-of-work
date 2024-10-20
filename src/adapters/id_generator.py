from sqlite3 import Connection

from src.application.protocols.id_generator import IdGeneratorProtocol


class SQLiteIdGenerator(IdGeneratorProtocol):
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def generate_new_post_id(self) -> int:
        return self._base_generate_new_id("SELECT id FROM posts")

    def generate_new_comment_id(self) -> int:
        return self._base_generate_new_id("SELECT id FROM comments")

    def _base_generate_new_id(self, sql_query: str) -> int:
        cursor = self._connection.execute(sql_query)
        print("CUROSR", cursor, cursor.lastrowid)

        if cursor.lastrowid:
            return 1

        return cursor.lastrowid + 1
