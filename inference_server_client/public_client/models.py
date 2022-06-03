import json
import logging
import os
import tempfile
import zipfile
from abc import abstractmethod
from typing import BinaryIO

from pydantic import BaseModel


class ClientModel(BaseModel):
    zip_file_path : str = None
    def get_zip(self) -> BinaryIO:
        assert self.zip_file_path
        if self.zip_file_path.endswith("zip"):
            return open(self.zip_file_path, "br")
        elif os.path.isdir(self.zip_file_path):
            logging.info("Input is directory - zipping to ZipFile/directory name/...")
            input_zip = tempfile.TemporaryFile(suffix=".zip")
            with zipfile.ZipFile(input_zip, "w") as zip_file:
                for fol, subs, files in os.walk(self.zip_file_path):
                    for file in files:
                        path = os.path.join(fol, file)
                        zip_file.write(path, arcname=path.replace(path, ""))
            input_zip.seek(0)
            return input_zip
        else:
            raise Exception("Input_path must be either zip_file or directory")

    @abstractmethod
    def to_params(self):
        pass

class Model(ClientModel):
    human_readable_id: str
    container_tag: str
    use_gpu: bool = None
    model_available: bool = None
    input_mountpoint: str = None
    output_mountpoint: str = None
    model_mountpoint: str = None
    description: str = None
    relative_zip_file_path: str = None


    def to_params(self):
        d = self.dict()
        del d["zip_file_path"]
        return d


class Task(ClientModel):
    model_human_readable_id: str
    relative_zip_file_path: str = None
    uid: str = None

    def to_params(self):
        d = self.dict()
        del d["zip_file_path"]
        return d

def model_loader(json_path):
    with open(json_path) as r:
        model_json = json.loads(r.read())
    model = Model(**model_json)

    return model

def task_loader(json_path):
    with open(json_path) as r:
        task_json = json.loads(r.read())
    model = Task(**task_json)

    return model

if __name__ == "__main__":
    model = model_loader("/models/GTVs_uncertainty_slim/GTVs_uncertainty_slim.json")
    print(model.dict())
