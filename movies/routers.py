from rest_framework.routers import SimpleRouter, Route


class CreateReviewRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={'post': 'create'},
            name='{basename}-create',
            detail=False,
            initkwargs={'suffix': 'Create'}
        ),

    ]


class CreateStarRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={'post': 'create'},
            name='{basename}-create',
            detail=False,
            initkwargs={'suffix': 'Create'}
        ),

    ]


class ListCreateRatingRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list-create',
            detail=False,
            initkwargs={'suffix': 'List-Create'}
        ),
    ]


class ListCreateActorRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list-create',
            detail=False,
            initkwargs={'suffix': 'List-Create'}
        ),
    ]


movie_router = SimpleRouter()
create_review_router = CreateReviewRouter()
create_star_router = CreateStarRouter()
list_create_rating_router = ListCreateRatingRouter()
list_create_actor_router = ListCreateActorRouter()
