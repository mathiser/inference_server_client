import json
import os.path
import unittest

import dotenv

from models import Model, Task
from public_client.public_client_impl import PublicClient
from tests.mock_component.mock_fast_api_testclient import MockClientBackend
from tests.mock_component.mock_public_api_fast_api_impl import PublicFastAPI


dotenv.load_dotenv()
class TestPublicClientRequestsImpl(unittest.TestCase):
    def setUp(self) -> None:
        self.client_backend = MockClientBackend(PublicFastAPI())
        self.client = PublicClient(self.client_backend)
        self.hello_world_model_path = "tests/models/hello_world/hello_world.json"
        with open(self.hello_world_model_path) as r:
            self.hello_world_model = Model(**json.loads(r.read()))

        self.task = Task(model_human_readable_id=self.hello_world_model.human_readable_id,
                         input_path=os.path.dirname(self.hello_world_model_path),
                         )

    def test_post_task(self):
        echo = self.client.post_task(self.task)
        self.assertEqual(echo.model_human_readable_id, self.task.model_human_readable_id)
        return echo

    def test_get_output_zip_by_uid(self):
        pass

    def test_post_model(self):
        echo = self.client.post_model(self.hello_world_model)
        self.assertEqual(echo.to_params(), self.hello_world_model.to_params())
        return echo

    def test_get_models(self):
        models = self.client.get_models()
        self.assertEqual(len(models), 0)
        model = self.test_post_model()
        models = self.client.get_models()
        self.assertEqual(len(models), 1)
        self.assertEqual(model.to_params(), models[0].to_params())
