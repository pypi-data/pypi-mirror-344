from starlette.responses import PlainTextResponse
from starlette.routing import Route

async def test_endpoint(request):
    return PlainTextResponse('test')

routes = [
    Route('/test', test_endpoint)
]
