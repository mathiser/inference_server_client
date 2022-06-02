import logging
import os
import random
import secrets
from typing import Any, List, Optional, Union
from urllib.parse import urljoin

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from models import Model, Task

threads = []

LOG_FORMAT = ('%(levelname)s:%(asctime)s:%(message)s')
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


class OutModel(BaseModel):
    human_readable_id: str
    container_tag: str
    use_gpu: bool
    model_available: bool = True
    input_mountpoint: str = "/input"
    output_mountpoint: str = "/output"
    model_mountpoint: str = None
    description: str = None
    model_path: str = None


class OutTask(BaseModel):
    model_human_readable_id: str
    uid: str


class PublicFastAPI(FastAPI):
    def __init__(self, **extra: Any):
        super().__init__(**extra)
        self.models = []
        self.tasks = []

        @self.get("/")
        def public_hello_world():
            return {"message": "Hello world - Welcome to the public database API"}

        @self.post(os.environ['PUBLIC_POST_TASK'], response_model=OutTask)
        def public_post_task(model_human_readable_id: str,
                             zip_file: UploadFile,
                             ):
            uid = secrets.token_urlsafe(32)
            task = Task(model_human_readable_id=model_human_readable_id,
                        uid=uid)

            self.tasks.append(task)
            logging.info(f"task receive {task}")

            return task

        @self.get(urljoin(os.environ['PUBLIC_GET_OUTPUT_ZIP_BY_UID'], "{uid}"))
        def public_get_output_zip_by_uid(uid: str) -> StreamingResponse:
            def iterfile():
                yield from random.randbytes(128)

            return StreamingResponse(iterfile())

        @self.get(os.environ["PUBLIC_GET_MODELS"], response_model=List[OutModel])
        def public_get_models():
            return self.models

        @self.post(os.environ.get("PUBLIC_POST_MODEL"), response_model=OutModel)
        def public_post_model(container_tag: str,
                              human_readable_id: str,
                              input_mountpoint: Optional[str] = "/input",
                              output_mountpoint: Optional[str] = "/output",
                              model_mountpoint: Optional[str] = None,
                              description: Optional[str] = None,
                              zip_file: Optional[UploadFile] = File(None),
                              model_available: Optional[bool] = False,
                              use_gpu: Optional[bool] = False,
                              ):
            model = Model(container_tag=container_tag,
                          human_readable_id=human_readable_id,
                          input_mountpoint=input_mountpoint,
                          output_mountpoint=output_mountpoint,
                          model_mountpoint=model_mountpoint,
                          description=description,
                          model_available=model_available,
                          use_gpu=use_gpu)

            self.models.append(model)

            return model
