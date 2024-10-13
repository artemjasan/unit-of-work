from src.application.protocols.repository import PostRepositoryProtocol
from src.application.protocols.unit_of_work import UnitOfWorkProtocol
from src.application.protocols.id_generator import IdGeneratorProtocol
from src.application.interactors.interactor import Interactor
from src.domain.entities import Post


class GetPost(Interactor[int, dict]):  # TODO: add correct DTOs
    def __init__(
        self,
        repository: PostRepositoryProtocol,
    ) -> None:
        self._repository = repository

    def execute(self, data: int) -> dict:
        post = self._repository.load_post(data)
        return dict(post)


class CreatePost(Interactor[dict, list]):  # TODO: add correct DTOs
    def __init__(
        self,
        uow: UnitOfWorkProtocol,
        repository: PostRepositoryProtocol,
        id_generator: IdGeneratorProtocol,
    ) -> None:
        self._uow = uow
        self._repository = repository
        self._id_generator = id_generator

    def execute(self, data: list) -> list:
        post_id = self._id_generator.generate_new_post_id()
        new_post = Post(post_id, data)

        self._repository.save_post(new_post)
        self._uow.commit()
        return dict(new_post)


class DeletePost(Interactor[int, None]):  # TODO: add correct DTOs
    def __init__(
        self,
        uow: UnitOfWorkProtocol,
        repository: PostRepositoryProtocol,
    ) -> None:
        self._uow = uow
        self._repository = repository

    def execute(self, data: int) -> None:
        post = self._repository.load_post(data)
        self._repository.delete_post(post)
        self._uow.commit()
