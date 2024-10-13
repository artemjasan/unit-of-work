from typing import Protocol

from src.domain.entities import Post


class PostRepositoryProtocol(Protocol):
    def load_post(self, post_id: int) -> Post:
        pass

    def save_post(self, post: Post) -> None:
        pass

    def delete_post(self, post_id: int) -> None:
        pass
