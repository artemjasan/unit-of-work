from typing import Protocol


class IdGeneratorProtocol(Protocol):
    def generate_new_post_id(self) -> int:
        pass

    def generate_new_comment_id(self) -> int:
        pass
