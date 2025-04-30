import functools

import fastapi
from gadfastrouter.routing.route import APIRoute

APIRouter = functools.partial(fastapi.APIRouter, route_class=APIRoute)
