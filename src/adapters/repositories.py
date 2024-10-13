from src.adapters.mappers import CommentMapper, PostMapper
from src.application.protocols.unit_of_work import UnitOfWorkProtocol
from src.domain.entites import Post


class PostRepository:
    def __init__(
        self,
        uow: UnitOfWorkProtocol,
        post_mapper: PostMapper,
        comment_mapper: CommentMapper,
    ) -> None:
        self._uow = uow
        self._post_mapper = post_mapper
        self._comment_mapper = comment_mapper

    def load_post(self, post_id: int) -> Post:
        post = self._post_mapper.find_by_id(post_id)
        comments = self._comment_mapper.find_by_post_id(post_id)
        post.load_comments(comments)
        return post

    def save_post(self, post: Post) -> None:
        if self._post_mapper.exists(post.id):
            self._uow.register_dirty(post)
        else:
            self._uow.register_new(post)

        for comment in post.comments:
            if not self._comment_mapper.exists(comment.id):
                self._uow.register_new(comment)

    def delete_post(self, post: Post) -> None:
        self._uow.register_removed(post)
        for comment in post.comments:
            self._uow.register_removed(comment)

        post.drop_comments()
