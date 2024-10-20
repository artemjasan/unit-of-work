from src.application.interactors.post_interactors import (
    CreatePostInteractor,
    GetPostInteractor,
    GetPostsInteractor,
)
from typing import Annotated

from dishka.integrations.base import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, post, get
from litestar.params import Body


class HTTPPostController(Controller):
    path = "/post"

    @post()
    @inject
    async def create_post(
        self,
        post_title: Annotated[str, Body(description="Post title", title="Post Title")],
        interactor: Depends[CreatePostInteractor],
    ) -> dict:
        post_dm = interactor.execute(post_title)
        return post_dm

    @get()
    @inject
    async def get_posts(self, interactor: Depends[GetPostsInteractor]) -> list:
        posts = interactor.execute(None)
        return posts
