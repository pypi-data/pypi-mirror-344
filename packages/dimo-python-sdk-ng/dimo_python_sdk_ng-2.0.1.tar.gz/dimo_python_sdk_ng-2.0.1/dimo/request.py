import json
from requests import Session


class Request:

    def __init__(self, http_method: str, url: str, session: Session):
        self.http_method = http_method
        self.url = url
        self.session = session

    def __call__(self, headers=None, data=None, params=None, **kwargs):
        headers = headers or {}
        headers.update(kwargs.pop("headers", {}))

        if (
            data
            and isinstance(data, dict)
            and headers.get("Content-Type") == "application/json"
        ):
            data = json.dumps(data)

        response = self.session.request(
            method=self.http_method,
            url=self.url,
            headers=headers,
            params=params,
            data=data,
            **kwargs,
        )

        # TODO: Better error responses
        response.raise_for_status()

        if response.content:
            return response.json()
        return None
