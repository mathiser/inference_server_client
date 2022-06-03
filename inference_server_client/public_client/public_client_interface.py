from abc import abstractmethod
from typing import List

from inference_server_client.public_client.models import Model, Task


class PublicClientInterface:

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