from fastapi.testclient import TestClient

from client_backend.client_backend_interface import ClientBackendInterface


class MockClientBackend(ClientBackendInterface):
    def __init__(self, app):
        self.client = TestClient(app=app)

    def get(self, url, stream=False):
        return self.client.get(url=url)

    def post(self, url, params, files=None):
        if files:
            return self.client.post(url=url, params=params, files=files)
        else:
            return self.client.post(url=url, params=params)