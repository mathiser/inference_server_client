from abc import abstractmethod
from typing import List

from client_backend.client_backend_interface import ClientBackendInterface
from models import Model, Task


class PublicClientInterface:
    def __init__(self, client: ClientBackendInterface):
        self.client = client

    @abstractmethod
    def get_output_zip_by_uid(self, uid: str, dst) -> Task:
        pass

    @abstractmethod
    def post_task(self, task: Task) -> Task:
        pass

    def post_model(self, model: Model) -> Model:
        pass

    @abstractmethod
    def get_models(self) -> List[Model]:
        pass