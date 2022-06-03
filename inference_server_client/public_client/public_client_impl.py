import json
from urllib.parse import urljoin

from inference_server_client.client_backend.client_backend_interface import ClientBackendInterface
from inference_server_client.public_client.models import Model, Task
from inference_server_client.public_client.public_client_interface import PublicClientInterface


class PublicClient(PublicClientInterface):
    def __init__(self, client_backend: ClientBackendInterface):
        self.client = client_backend

    def get_hello_world(self):
        return self.client.get("/")

    def get_output_zip_by_uid(self, uid, dst):
        res = self.client.get(urljoin("/api/tasks/", uid),
                              stream=True)
        if res.ok:
            with open(dst, "wb") as f:
                for chunk in res.iter_content(chunk_size=1000000):
                    f.write(chunk)
            return True
        else:
            print(json.loads(res.content))
            return False

    def post_task(self, task: Task):
        with task.get_zip() as zip:
            res = self.client.post("/api/tasks",
                                   params=task.to_params(),
                                   files={"zip_file": zip}
                                   )

        if res.ok:
            return json.loads(res.content)
        else:
            return res

    def post_model(self, model: Model):
        if model.model_available:
            assert model.relative_zip_file_path, model.model_mountpoint
            with model.get_zip() as zip:
                res = self.client.post("/api/models",
                                       params=model.to_params(),
                                       files={"zip_file": zip})
        else:
            res = self.client.post("/api/models",
                                   params=model.to_params())
        if res.ok:
            print(res.content)
            return Model(**json.loads(res.content))
        else:
            return res

    def get_models(self):
        res = self.client.get("/api/models")
        models = [Model(**model) for model in json.loads(res.content)]
        return models