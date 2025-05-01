import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class AuthRequests:

    def __init__(self, token, base_url):
        self.token = token
        self.base_url = base_url

    def add_auth_headers(self, **kargs):
        if not kargs.get("headers"):
            kargs["headers"] = {}
        kargs["headers"]["x-access-token"] = self.token
        return kargs
    
    def raise_for_status(self, response: requests.Response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise requests.exceptions.HTTPError(
                f"{e} - Response Text: {response.text}"
            ) from None

    def get(self, **kargs):
        r= requests.get(**self.add_auth_headers(**kargs), timeout=3)

        self.raise_for_status(r)
        return r.json()

    def post(self, **kargs):
        r= requests.post(**self.add_auth_headers(**kargs), timeout=3)
        self.raise_for_status(r)
        return r.json()

    def delete(self, **kargs):
        r= requests.delete(**self.add_auth_headers(**kargs), timeout=3)
        self.raise_for_status(r)
        return r.json()

    def patch(self, **kargs):
        r= requests.patch(**self.add_auth_headers(**kargs), timeout=3)
        self.raise_for_status(r)
        return r.json()

    def put(self, **kargs):
        r= requests.put(**self.add_auth_headers(**kargs), timeout=1)
        self.raise_for_status(r)
        return r.json()
