from flask import Response
import orjson


class JSONResponse(Response):
    default_mimetype: str = "application/json"
    json_module = orjson
