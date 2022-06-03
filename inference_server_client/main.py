import argparse
import os

import dotenv

from inference_server_client.client_backend.client_backend_requests_impl import ClientBackendRequestsImpl
from inference_server_client.public_client.models import task_loader, model_loader, Task
from inference_server_client.public_client.public_client_impl import PublicClient

def main():
    dotenv.load_dotenv()
    CERT = os.path.join(os.path.dirname(__file__), os.environ.get("CERT"))
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--method', required=True, help='')
    parser.add_argument("-i", '--input_json', required=False, help="")
    parser.add_argument('-o', "--output_zip_path", required=False, help="")
    parser.add_argument("-b", "--base_url", required=False, default=os.environ.get("BASE_URL"))
    parser.add_argument("-c", "--cert_file", required=False, default=CERT, help="Set a custom certificate")
    parser.add_argument("-zip", "--zip_file_path", required=False, help="Zip file path - use with -hid")
    parser.add_argument("-hid", "--model_human_readable_id", required=False, help="Human readable id of a model")
    parser.add_argument('-uid', "--task_uid", required=False, help="Uid of a task. Is returned when a task is posted")


    args = parser.parse_args()
    method = args.method
    input_json = args.input_json
    output_folder = args.output_folder
    base_url = args.base_url
    cert_file = args.cert_file
    model_human_readable_id = args.model_human_readable_id
    task_uid = args.task_uid
    zip_file_path = args.zip_file_path

    client_backend = ClientBackendRequestsImpl(base_url=base_url, cert=cert_file)
    client = PublicClient(client_backend=client_backend)

    if method == "hello_world":
        print(client.get_hello_world())

    elif method == "post_task":
        if input_json:
            task = task_loader(json_path=input_json)
            print(client.post_task(task))
        else:
            assert model_human_readable_id, zip_file_path
            task = Task(model_human_readable_id=model_human_readable_id,
                        zip_file_path=zip_file_path)
            print(client.post_task(task)["uid"])

    elif method == "post_model":
        assert input_json
        model = model_loader(json_path=input_json)
        print(client.post_model(model))

    elif method == "get_models":
        print(client.get_models())

    elif method == "get_task":
        assert task_uid, output_folder
        print(client.get_output_zip_by_uid(task_uid, output_folder))

    else:
        print(f"Wrong method")

if __name__ == "__main__":
    main()

