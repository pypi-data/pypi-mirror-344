import enum


class LoggingField(str, enum.Enum):
    debug = "debug"
    service = "service"
    version = "version"
    http_version = "http-version"
    ip = "ip"
    method = "method"
    url = "url"
    headers = "headers"
    query = "query"
    body = "body"
    response = "response"
    code = "code"
    started = "started"
    ended = "ended"
    elapsed = "elapsed"
