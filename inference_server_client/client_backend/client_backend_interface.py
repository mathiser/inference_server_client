from abc import abstractmethod


class ClientBackendInterface:
    @abstractmethod
    def get(self, url, stream=False):
        pass

    @abstractmethod
    def post(self, url, params, files=None):
        pass
