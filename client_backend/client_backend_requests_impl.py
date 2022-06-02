from urllib.parse import urljoin

import requests

from client_backend.client_backend_interface import ClientBackendInterface


class ClientBackendRequestsImpl(ClientBackendInterface):
    def __init__(self, base_url, cert=None, verify=True):
        self.base_url = base_url
        self.cert = cert
        self.verify = verify

    def get(self, url, stream=False):
        return requests.get(urljoin(self.base_url, url), verify=self.verify, cert=self.cert)

    def post(self, url, params=None, files=None, cert_file=None):
        if files:
            return requests.post(urljoin(self.base_url, url), params=params, files=files, cert=self.cert,
                                 verify=self.verify)
        else:
            return requests.post(urljoin(self.base_url, url), params=params, cert=self.cert, verify=self.verify)
