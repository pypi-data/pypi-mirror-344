import json
from .utils.error_message import NO_DATASETS
from .utils.errors import api_error
from .base.base_zbl import ZBLBase
from .auth import APIAuth
import requests
from typing import List, Dict, Union, Tuple
from pathlib import Path


class DataSet(ZBLBase):
    def __int__(self, api_auth: APIAuth):
        super().__init__(api_auth)

    @staticmethod
    def __process_single_element(element: Dict) -> Dict:
        return {'name': element.get('name', ''), 'id': element.get('_id', '')}

    @staticmethod
    def __print_info(datasets: List[Dict], error_message: str = None):
        print("DataSets:")
        if len(datasets) > 0:
            for idx, data in enumerate(datasets):
                print(f"\t{idx + 1}. name: {data['name']} | id: {data['id']}")
        else:
            print("No resources available" if error_message is None else error_message)

    @classmethod
    def __process_response(
            cls,
            response: requests.Response, return_data: bool = True,
            raise_exception: bool = True, error_message: str = None,
    ) -> Union[List[Dict], Dict, bool, None]:

        namespace_data = []
        data_retrieval_success = response.status_code == 200 and response.json()['success'] and response.json()[
            'totalCount'] > 0

        dataset_data = None

        if not return_data and not raise_exception:
            return data_retrieval_success

        if not data_retrieval_success and raise_exception:
            api_error(
                status_code=response.status_code,
                message=response.text if error_message is None else error_message
            )

        if data_retrieval_success:
            __resp_data = response.json()['data']
            __resp_data = response.json()['data']
            if isinstance(__resp_data, dict):
                dataset_data = cls.__process_single_element(__resp_data)
            elif isinstance(__resp_data, list):
                dataset_data = list(map(lambda data: cls.__process_single_element(data), __resp_data))

        return dataset_data

    def __get(
            self, resource_id: str = None, return_data: bool = True,
            raise_exception: bool = True, error_message: str = None,
    ) -> Union[List[Dict], Dict, bool, None]:
        __base_url = f"{self._api_auth.app_url}/api/v1/datasets"

        if resource_id is None:
            response = requests.get(
                __base_url, headers={'Content-Type': 'application/json'},
                auth=self._api_auth.get_api_creds()
            )
        else:
            response = requests.get(
                f"{__base_url}/{resource_id.strip()}", headers={'Content-Type': 'application/json'},
                auth=self._api_auth.get_api_creds()
            )

        return self.__process_response(
            response=response, return_data=return_data, raise_exception=raise_exception, error_message=error_message
        )

    def __create_dataset_version(self, dataset_id: str, full_filepaths: List[str]) -> Dict:
        __base_url = f"{self._api_auth.app_url}/api/v1/datasetsversions"

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        }

        files_names = {}
        for filepath in full_filepaths:
            if not Path(filepath).exists():
                print(f"File `{filepath}` not found. Skipping its upload.")
                continue
            files_names[Path(filepath).name] = {"filepath": filepath, "url": None}

        if len(files_names) == 0:
            api_error(status_code=400, message=f"No files to upload.")

        response = requests.post(
            url=f"{__base_url}", headers=headers, data=json.dumps({
                "datasetId": dataset_id, "fileNames": list(files_names.keys())
            }),
            auth=self._api_auth.get_api_creds()
        )

        if response.status_code == 200 and response.json()['success']:
            for _data in response.json()['data']:
                files_names[_data['fileName']]['url'] = _data['url']
            return files_names

        api_error(
            status_code=response.status_code,
            message=f"Unable to create dataset version for dataset id: {dataset_id}.\nMessage from server: {response.text}."
        )

    @staticmethod
    def __upload_file(full_filepath: str, presigned_url: str) -> Tuple[bool, str]:
        with open(full_filepath, 'rb') as file:
            # Upload the file using the presigned URL
            response = requests.put(
                presigned_url, data=file, headers={"x-ms-blob-type": "BlockBlob", "Content-Type": "text/plain"}
            )

        # Check the response
        if response.status_code == 201:
            return True, ""

        return False, f"Unable to upload file: {full_filepath}.\nMessage from server: {response.text}."

    def get_all(self, print_stdout: bool = True) -> List[Dict]:
        datasets_data = self.__get(
            resource_id=None, return_data=True,
            raise_exception=True, error_message=NO_DATASETS
        )
        if print_stdout:
            self.__print_info(datasets=datasets_data)

        return datasets_data

    def get_by_name(self, dataset_name: str) -> Union[Dict, None]:
        for dataset in self.get_all(print_stdout=False):
            if dataset['name'] == dataset_name.strip():
                return dataset
        return None

    def create_dataset(self, dataset_name: str, dataset_description: str) -> str:
        __base_url = f"{self._api_auth.app_url}/api/v1/datasets"
        response = requests.post(
            url=f"{__base_url}", headers={'Content-Type': 'application/json'},
            auth=self._api_auth.get_api_creds(),
            data=json.dumps({"name": dataset_name, "description": dataset_description})
        )

        if response.status_code == 201 and response.json()['success']:
            return response.json()['data']['_id']

        api_error(
            status_code=response.status_code,
            message=f"Unable to create the Dataset.\nMessage from server: {response.text}"
        )

    def upload_dataset(self, dataset_id: str, filepaths: List[str]):
        filename_with_upload_urls = self.__create_dataset_version(dataset_id, filepaths.copy())
        for filename, _data in filename_with_upload_urls.items():
            success, msg = self.__upload_file(_data['filepath'], _data['url'])
            if not success:
                print(msg)
        print(f"Uploaded files: {', '.join(list(filename_with_upload_urls.keys()))}")
