import datetime
import os.path
import unittest
from pprint import pprint

import dotenv

from inference_server_client.client_backend.client_backend_requests_impl import ClientBackendRequestsImpl
from inference_server_client.public_client import Model, Task
from inference_server_client.public_client.public_client_impl import PublicClient

dotenv.load_dotenv()


class TestEndToEnd(unittest.TestCase):
    def setUp(self) -> None:
        self.client_backend = ClientBackendRequestsImpl(base_url="https://localhost/", verify=False)
        self.client = PublicClient(self.client_backend)

        self.hello_world_model_zip_path = "tests/models/hello_world/hello_world.zip"
        self.model_no_zip = Model(container_tag="hello-world",
                                  human_readable_id=f"hello_world_{datetime.datetime.now()}",
                                  use_gpu=False,
                                  model_available=False,
                                  description="Run hello world",
                                  model_mountpoint="/model"
                                  )
        self.model_with_zip = Model(container_tag="hello-world",
                                    human_readable_id=f"hello_world_{datetime.datetime.now()}",
                                    use_gpu=False,
                                    model_available=True,
                                    description="Run hello world",
                                    input_path=os.path.dirname(self.hello_world_model_zip_path),
                                    model_mountpoint="/model"
                                    )

    def test_hello_world(self):
        echo = self.client.get_hello_world()
        self.assertIn(b"Hello world", echo.content)

    def test_post_task(self):
        model = self.test_post_model_with_zip()
        task = Task(model_human_readable_id=model.human_readable_id, input_path=self.hello_world_model_zip_path)
        echo = self.client.post_task(task)
        self.assertEqual(echo.model_human_readable_id, task.model_human_readable_id)
        return echo

    # def test_get_output_zip_by_uid(self):
    #     pass

    def test_post_model_with_zip(self):
        echo = self.client.post_model(self.model_with_zip)
        self.assertEqual(echo.to_params(), self.model_with_zip.to_params())
        return echo

    def test_post_model_no_zip(self):
        echo = self.client.post_model(self.model_with_zip)
        # # for k, v in echo.to_params().items():
        # #     if k == "human_readable_id":
        #         continue
        self.assertEqual(echo.to_params(), self.model_with_zip.to_params())
        return echo

    def test_get_models(self):
        models = self.client.get_models()
        pprint(models)
        l0 = len(models)
        model = self.test_post_model_with_zip()
        print(model)
        models = self.client.get_models()
        pprint(models)
        l1 = len(models)
        self.assertEqual(l1, l0 + 1)
