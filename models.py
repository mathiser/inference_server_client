import logging
import os
import tempfile
import zipfile
from typing import BinaryIO, Optional
from pydantic import BaseModel

def load_input_path(input_path) -> BinaryIO:
    assert input_path
    if input_path.endswith("zip"):
        return open(input_path, "br")
    elif os.path.isdir(input_path):
        logging.info("Input is directory - zipping to ZipFile/directory name/...")
        input_zip = tempfile.TemporaryFile(suffix=".zip")
        with zipfile.ZipFile(input_zip, "w") as zip_file:
            for fol, subs, files in os.walk(input_path):
                for file in files:
                    path = os.path.join(fol, file)
                    zip_file.write(path, arcname=path.replace(input_path, ""))
        input_zip.seek(0)
        return input_zip
    else:
        raise Exception("Input_path must be either zip_file or directory")



class Model(BaseModel):
    human_readable_id: str
    container_tag: str
    use_gpu: bool = False
    model_available: bool = False
    input_mountpoint: str = None
    output_mountpoint: str = None
    model_mountpoint: str = None
    description: str = None
    model_path: str = None

    def to_params(self):
        d = self.dict()
        del d["model_path"]

        return d

    def get_zip(self):
        return load_input_path(self.model_path)

class Task(BaseModel):
    model_human_readable_id: str
    input_path: str = None
    uid: str = None

    def to_params(self):
        d = self.dict()
        del d["input_path"]
        return d

    def get_zip(self):
        return load_input_path(self.input_path)


