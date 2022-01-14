from masonite.views import View
from masonite.response import Response
from masonite.request import Request
from masonite.controllers import Controller
import json
from masonite.facades import Storage


class DebugController(Controller):
    def debug(self, response: Response):
        requests = []
        files = Storage.disk("debug").get_files()
        files = sorted(files, key=lambda x: x.name())
        for file in files:
            requests.append(
                {
                    "request_id": json.loads(file.content)["__meta"]["request_id"],
                    "request_url": json.loads(file.content)["__meta"]["request_url"],
                }
            )

        return response.json(
            {
                "data": json.loads(files[0].content)["data"],
                "collectors": list(json.loads(files[0].content)["data"].keys()),
                "requests": requests,
            }
        )

    def get_debug(self, response: Response, request: Request):
        requests = []
        files = Storage.disk("debug").get_files()
        files = sorted(files, key=lambda x: x.name())

        for file in files:
            requests.append(
                {
                    "request_id": json.loads(file.content)["__meta"]["request_id"],
                    "request_url": json.loads(file.content)["__meta"]["request_url"],
                }
            )

        file = Storage.disk("debug").get(f"{request.param('id')}.json")

        return response.json(
            {
                "data": json.loads(file)["data"],
                "collectors": list(json.loads(file)["data"].keys()),
                "requests": requests,
            }
        )
