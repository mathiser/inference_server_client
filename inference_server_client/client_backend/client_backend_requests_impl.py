from urllib.parse import urljoin

import requests

from inference_server_client.client_backend.client_backend_interface import ClientBackendInterface


class ClientBackendRequestsImpl(ClientBackendInterface):
    def __init__(self, base_url, cert=True):
        self.base_url = base_url
        self.cert = cert

    def get(self, url, stream=False):
        url = urljoin(self.base_url, url)
        return requests.get(urljoin(self.base_url, url), verify=self.cert)

    def post(self, url, params=None, files=None):
        if files:
            return requests.post(urljoin(self.base_url, url), params=params, files=files, verify=self.cert)
        else:
            return requests.post(urljoin(self.base_url, url), params=params, verify=self.cert)
