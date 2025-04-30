import contextlib
import logging
import typing

import fastapi
from gadfastrouter import const
from gadfastrouter import enums
from gadutils import binaries
from gadutils import dates
from gadutils import json

logger = logging.getLogger("fastapi.route")


class Logging:
    def __init__(self, request: fastapi.Request) -> None:
        self.context = self.init_context(request)

    @classmethod
    def init_context(cls, request: fastapi.Request) -> dict:
        headers = dict(request.headers.items())

        for key in enums.HTTPHeader.secure():
            if headers.get(key, None):
                headers[key] = const.SYMBOL_ASTERISK

        return {
            enums.LoggingField.debug: request.app.debug,
            enums.LoggingField.service: request.app.title,
            enums.LoggingField.version: request.app.version,
            enums.LoggingField.http_version: request.scope.get("http_version", None),
            enums.LoggingField.ip: f"{request.client.host}:{request.client.port}",
            enums.LoggingField.method: request.method.upper(),
            enums.LoggingField.url: str(request.url),
            enums.LoggingField.headers: headers,
            enums.LoggingField.query: dict(request.query_params),
            enums.LoggingField.body: {},
            enums.LoggingField.response: {},
            enums.LoggingField.code: None,
            enums.LoggingField.started: dates.now(),
            enums.LoggingField.ended: None,
            enums.LoggingField.elapsed: None,
        }

    @property
    def endpoint(self) -> str:
        return f"{self.context[enums.LoggingField.method]} {self.context[enums.LoggingField.url]}"

    def timing(self) -> None:
        self.context[enums.LoggingField.ended] = dates.now()
        self.context[enums.LoggingField.elapsed] = (
            self.context[enums.LoggingField.ended] - self.context[enums.LoggingField.started]
        ).total_seconds()

    def accepted(self) -> None:
        _logger = logger.warning if self.context.get(enums.LoggingField.body) == const.SYMBOL_DASH else logger.info
        _logger(f"Request accepted - {self.endpoint}", extra=self.context)

    def processed(self) -> None:
        _logger = logger.warning if self.context.get(enums.LoggingField.response) == const.SYMBOL_DASH else logger.info
        _logger(f"Request processed - {self.endpoint}", extra=self.context)

    def error(self) -> None:
        logger.error(f"Request error - {self.endpoint}", extra=self.context, exc_info=True)


class Json:
    @classmethod
    def parse(cls, raw: bytes) -> typing.Any | str:
        with contextlib.suppress(Exception):
            return json.fromjson(binaries.tostring(raw))
        return const.SYMBOL_DASH

    @classmethod
    def parseresponse(cls, response: fastapi.Response) -> typing.Any | str:
        return cls.parse(response.body)

    @classmethod
    async def parsebody(cls, request: fastapi.Request) -> typing.Any | str:
        return cls.parse(await request.body())


class APIRoute(fastapi.routing.APIRoute):
    def get_route_handler(self) -> typing.Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: fastapi.Request) -> fastapi.Response:
            if route := request.scope.get("route", None):  # noqa:SIM102
                if exclude_paths := getattr(request.app, "exclude_paths", None):  # noqa:SIM102
                    if route.path_format in exclude_paths:
                        return await original_route_handler(request)

            log = Logging(request)

            if request.headers.get("Content-Type") == "application/json":
                with contextlib.suppress(ValueError):
                    log.context[enums.LoggingField.body] = (
                        await Json.parsebody(request)
                        if int(request.headers.get("Content-Length", 0)) < const.SIZE_64KB
                        else const.SYMBOL_DASH
                    )

            log.accepted()

            try:
                response = await original_route_handler(request)
                log.context[enums.LoggingField.code] = response.status_code
            except fastapi.exceptions.HTTPException as e:
                log.context[enums.LoggingField.code] = e.status_code
                log.context[enums.LoggingField.response] = e.detail
                log.timing()
                log.processed()
                raise e
            except fastapi.exceptions.ValidationException as e:
                log.context[enums.LoggingField.code] = fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY
                log.context[enums.LoggingField.response] = str(e)
                log.timing()
                log.processed()
                raise e
            except Exception as e:
                log.context[enums.LoggingField.code] = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
                log.timing()
                log.error()
                raise e

            if response.headers.get("Content-Type") == "application/json":
                log.context[enums.LoggingField.response] = (
                    Json.parseresponse(response) if len(response.body) < const.SIZE_128KB else const.SYMBOL_DASH
                )

            log.timing()
            log.processed()

            return response

        return custom_route_handler
