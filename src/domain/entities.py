from dataclasses import dataclass, field

from src.domain.protocols import DomainEntity


@dataclass
class Comment(DomainEntity):
    id: int
    body: str
    post_id: int

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class Post(DomainEntity):
    id: int
    title: str
    comments: list[Comment] = field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.id)

    def load_comments(self, comments: list[Comment]) -> None:
        self.comments = comments

    def drop_comments(self) -> None:
        self.comments.clear()

    def add_comment(self, comment: Comment) -> None:
        self.comments.append(comment)

    def remove_comment(self, comment: Comment) -> None:
        self.comments.remove(comment)
