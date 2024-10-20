from logging import getLogger
from typing import Iterable
import sqlite3

from dishka import AnyOf, Provider, Scope, from_context, provide

from src.config import AppConfig
from src.application.protocols.id_generator import IdGeneratorProtocol
from src.adapters.id_generator import SQLiteIdGenerator
from src.adapters.mappers import PostMapper, CommentMapper
from src.application.uow.map_registry import MapperRegistry
from src.domain.entities import Post, Comment
from src.application.protocols.unit_of_work import UnitOfWorkProtocol
from src.adapters.uow import SQLiteUnitOfWork
from src.adapters.repositories import PostRepository
from src.application.interactors.post_interactors import (
    CreatePostInteractor,
    GetPostsInteractor,
)


logger = getLogger(__name__)


class AppProvider(Provider):
    config = from_context(provides=AppConfig, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def apply_migrations(self, config: AppConfig) -> None:
        logger.info("Apply migrations.")
        with sqlite3.connect(config.db_schema, isolation_level=None) as conn, open(
            config.db_schema
        ) as sql_file:
            conn.executescript(sql_file.read())
            conn.commit()

    @provide(scope=Scope.REQUEST)
    def get_connection(self, config: AppConfig) -> Iterable[sqlite3.Connection]:
        with sqlite3.connect(config.db_url, isolation_level=None) as conn:
            yield conn

    @provide(scope=Scope.REQUEST)
    def get_id_generator(
        self, conn: sqlite3.Connection
    ) -> AnyOf[SQLiteIdGenerator, IdGeneratorProtocol]:
        return SQLiteIdGenerator(conn)

    @provide(scope=Scope.REQUEST)
    def get_comment_mapper(self, conn: sqlite3.Connection) -> CommentMapper:
        return CommentMapper(conn)

    @provide(scope=Scope.REQUEST)
    def get_post_mapper(self, conn: sqlite3.Connection) -> PostMapper:
        return PostMapper(conn)

    @provide(scope=Scope.REQUEST)
    def get_mapper_registry(
        self,
        conn: sqlite3.Connection,
        comment_mapper: CommentMapper,
        post_mapper: PostMapper,
    ) -> MapperRegistry:
        mapper_registry = MapperRegistry()
        mapper_registry.register(Post, post_mapper)
        mapper_registry.register(Comment, comment_mapper)
        return mapper_registry

    @provide(scope=Scope.REQUEST)
    def get_uow(
        self,
        conn: sqlite3.Connection,
        mapper_registry: MapperRegistry,
    ) -> AnyOf[SQLiteUnitOfWork, UnitOfWorkProtocol]:
        return SQLiteUnitOfWork(conn, mapper_registry)

    @provide(scope=Scope.REQUEST)
    def get_post_repository(
        self,
        uow: UnitOfWorkProtocol,
        post_mapper: PostMapper,
        comment_mapper: CommentMapper,
    ) -> PostRepository:
        return PostRepository(uow, post_mapper, comment_mapper)

    @provide(scope=Scope.REQUEST)
    def get_create_post_interactor(
        self,
        uow: UnitOfWorkProtocol,
        post_repository: PostRepository,
        id_generator: IdGeneratorProtocol,
    ) -> CreatePostInteractor:
        return CreatePostInteractor(uow, post_repository, id_generator)

    @provide(scope=Scope.REQUEST)
    def get_get_posts_interactor(
        self, post_repository: PostRepository
    ) -> GetPostsInteractor:
        return GetPostsInteractor(post_repository)
