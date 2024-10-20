from sqlite3 import Connection

from src.domain.entities import Comment, Post
from src.application.protocols.mapper import DataMapperProtocol


class PostMapper(DataMapperProtocol[Post]):
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def insert(self, entity: Post) -> None:
        self._connection.execute(
            "INSERT INTO posts (title) VALUES (?)", (entity.title,)
        )

    def update(self, entity: Post) -> None:
        self._connection.execute(
            "UPDATE posts SET title = ? WHERE id = ?", (entity.title, entity.id)
        )

    def delete(self, entity: Post) -> None:
        self._connection.execute("DELETE FROM posts WHERE id = ?", (entity.id))

    def exists_by_id(self, id_: int) -> bool:
        cursor = self._connection.execute("SELECT 1 FROM posts WHERE id = ?", (id_,))
        return cursor.fetchone() is not None

    def find_by_id(self, id_: int) -> Post | None:
        cursor = self._connection.execute(
            "SELECT id, title FROM posts WHERE id = ?", (id_,)
        )
        row = cursor.fetchone()
        if row:
            return Post(*row)
        return row

    def find_all(self) -> list[Post]:
        cursor = self._connection.execute("SELECT id, title FROM posts")
        return [Post(*row) for row in cursor.fetchall()]


class CommentMapper(DataMapperProtocol[Comment]):
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def insert(self, entity: Comment) -> None:
        self._connection.execute(
            "INSERT INTO comments (body, post_id) VALUES (?,?)",
            (entity.body, entity.post_id),
        )

    def update(self, entity: Comment) -> None:
        self._connection.execute(
            "UPDATE commenta SET body = ? WHERE id = ?", (entity.body, entity.id)
        )

    def delete(self, id_: int) -> None:
        self._connection.execute("DELETE FROM comments WHERE id = ?", (id_,))

    def exist_by_id(self, id_: int) -> bool:
        cursor = self._connection.execute("SELECT 1 FROM comments WHERE id = ?", (id_,))
        return cursor.fetchone() is None

    def find_by_id(self, id_: int) -> Comment | None:
        cursor = self.connection.execute(
            "SELECT id, body, post_id FROM comments WHERE id = ?", (id_,)
        )
        row = cursor.fetchone()
        if row:
            return Comment(*row)
        return row

    def find_by_post_id(self, post_id: int) -> list[Comment]:
        cursor = self._connection.execute(
            "SELECT id, body, post_id FROM comments WHERE post_id = ?", (post_id,)
        )
        return [Comment(*row) for row in cursor.fetchall()]

    def find_all(self) -> list[Comment]:
        cursor = self._connection.execute("SELECT id, body, post_id FROM comments")
        return [Comment(*row) for row in cursor.fetchall()]
