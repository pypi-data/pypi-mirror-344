from .base.base_service import ZBLBase
from .auth import APIAuth
from .base.base_service import ServiceSpawnBase
from .plan import Plan
from .namespace import Namespace
from .utils.errors import api_error
from .utils.error_message import NO_INFERENCES, NO_INFERENCE_ID, NO_SPAWNED_INFERENCE, NO_SPAWNED_INFERENCE_ID, \
    NO_SPAWNED_INFERENCE_POD_NAME
from . import PLAN_TYPE_INFERENCE_HUB
import requests
from typing import List, Union, Dict
import json
from datetime import datetime
from .utils.validations import validate_inference_name, validate_inference_replicas, validate_resource_threshold, \
    validate_model_tag_info, validate_model_type


class InferenceHub(ServiceSpawnBase):
    def __init__(self, api_auth: APIAuth):
        super().__init__(api_auth)
        self.__plan = Plan(api_auth=api_auth)
        self.__namespace = Namespace(api_auth=api_auth)

    @staticmethod
    def convert_iso_datetime_to_local_time(iso_datetime: str) -> str:
        return datetime.strptime(iso_datetime, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone().strftime("%b %d %Y %H:%M:%S.%f")[
               :-3]

    @staticmethod
    def __print_info(inferences: List[Dict], error_message: str = None, processing_for_spawned_inference: bool = False):
        print("Inferences:")
        if len(inferences) > 0:
            for idx, data in enumerate(inferences):
                print(f"\t{idx + 1}. {data['name']}")

                if processing_for_spawned_inference:
                    print(f"\t\tSTATUS: {data['status']}")
                    print(f"\t\tLast Updated: {data['updated_at']}")

                print(
                    f"\t\tid: {data['id']} | description: {data['description']} | added by: {data['added_by']} | organisation: {data['organisation']} | is_public: {data['is_public']}"
                )

                print(f"\t\tVolume Path: {data['volume_path']}")

                if 'modelTags' in data:
                    print(f"\t\tModel Tags:")
                    for model_tag_idx, model_tag_info in enumerate(data['modelTags']):
                        print(
                            f"\t\t\t{model_tag_idx + 1}. _id: {model_tag_info['_id']} | displayName: {model_tag_info['displayName']} | modelImage: {model_tag_info['modelImage']}"
                        )

                if 'ports' in data:
                    print(f"\t\tPorts:")
                    for port_idx, port_info in enumerate(data['ports']):
                        print(
                            f"\t\t\t{port_idx + 1}. Protocol: {port_info['protocol']} | Port Identifier: {port_info['portIdentifier']} | Port Number: {port_info['number']}")

                if 'envs' in data:
                    print(f"\t\tEnvs:")
                    for env_idx, env_info in enumerate(data['envs']):
                        print(f"\t\t\t{env_idx + 1}. key: {env_info['key']} | value: {env_info['value']}")

                if 'args' in data:
                    print(f"\t\tArgs:")
                    for arg_idx, arg_info in enumerate(data['args']):
                        print(
                            f"\t\t\t{arg_idx + 1}. key: {arg_info['key']} {'| value: ' + str(arg_info['value']) if arg_info.get('value', None) is not None else ''}"
                        )

                print()
        else:
            print("No resources available" if error_message is None else error_message)

    @classmethod
    def __process_single_element(cls, element: Dict, processing_for_spawned_inference: bool = False) -> Dict:
        e = {
            'id': element.get('_id', None), 'name': element.get('name', None),
            'model_type': element.get('modelType', None),
            'is_public': element.get('isPublic', None),
            'added_by': None if element.get('addedBy', None) is None else element['addedBy'].get('name', None),
            'organisation': None if element.get('organisationId', None) is None else element['organisationId'].get(
                'name', None),
            'volume_path': element['parameters']['volumePath'],
        }

        if len(element['parameters']['ports']) > 0:
            e['ports'] = element['parameters']['ports']

        if len(element['parameters']['envs']) > 0:
            e['envs'] = element['parameters']['envs']

        if len(element['parameters']['args']) > 0:
            e['args'] = element['parameters']['args']

        if processing_for_spawned_inference:
            e['status'] = element.get('status', None)
            e['description'] = None if element.get('inferenceId', None) is None else element['inferenceId'][
                'description']
            if element.get('updatedAt', None) is not None:
                e['updated_at'] = cls.convert_iso_datetime_to_local_time(element['updatedAt'])
        else:
            e['description'] = element.get('description', None)
            e['modelTags'] = element.get('modelTag', [])
        return e

    def __process_response(
            self,
            response: requests.Response, return_data: bool = True,
            raise_exception: bool = True, error_message: str = None,
            processing_for_spawned_inference: bool = False
    ) -> Union[List[Dict], Dict, bool, None]:
        inference_data = None
        data_retrieval_success = response.status_code == 200 and response.json()['success']

        if not return_data:
            if not raise_exception:
                return True if data_retrieval_success else False

            if data_retrieval_success and raise_exception:
                return True

        if not data_retrieval_success and raise_exception:
            api_error(
                status_code=response.status_code,
                message=response.text if error_message is None else error_message
            )

        __resp_data = response.json()['data']
        if isinstance(__resp_data, dict):
            inference_data = self.__process_single_element(
                __resp_data) if not processing_for_spawned_inference else self.__process_single_element(
                __resp_data, True
            )
        elif isinstance(__resp_data, list):
            inference_data = list(map(
                lambda data: self.__process_single_element(
                    data) if not processing_for_spawned_inference else self.__process_single_element(data, True),
                __resp_data
            ))

        return inference_data

    @staticmethod
    def __basic_id_validation(resource_id: str):
        if not isinstance(resource_id, str):
            raise TypeError(f'inference_hub_id can only be of type String')
        if resource_id.strip() == '':
            raise ValueError(f'inference_hub_id cannot empty')

    def __get(
            self, resource_id: str = None, return_data: bool = True,
            raise_exception: bool = True, error_message: str = None,
    ) -> Union[List[Dict], Dict, bool, None]:
        __base_url = f"{self._api_auth.app_url}/api/v1/inferences"

        if resource_id is None:
            response = requests.get(
                __base_url, headers={'Content-Type': 'application/json'},
                auth=self._api_auth.get_api_creds()
            )
        else:
            self.__basic_id_validation(resource_id=resource_id)
            response = requests.get(
                f"{__base_url}/{resource_id.strip()}", headers={'Content-Type': 'application/json'},
                auth=self._api_auth.get_api_creds()
            )

        return self.__process_response(
            response=response, return_data=return_data, raise_exception=raise_exception, error_message=error_message
        )

    def __get_spawned_inference(
            self, resource_id: str = None, return_data: bool = True,
            raise_exception: bool = True, error_message: str = None,
    ) -> Union[List[Dict], Dict, bool, None]:
        __base_url = f"{self._api_auth.app_url}/api/v1/spawnedInferences"

        if resource_id is None:
            response = requests.get(
                __base_url, headers={'Content-Type': 'application/json'},
                auth=self._api_auth.get_api_creds()
            )
        else:
            self.__basic_id_validation(resource_id=resource_id)
            response = requests.get(
                f"{__base_url}/{resource_id.strip()}", headers={'Content-Type': 'application/json'},
                auth=self._api_auth.get_api_creds()
            )

        return self.__process_response(
            response=response, return_data=return_data, raise_exception=raise_exception, error_message=error_message,
            processing_for_spawned_inference=True
        )

    def validate_id(self, inference_id: str, raise_exception: bool = False):
        if inference_id is None:
            if raise_exception:
                raise ValueError("inference_id cannot be None")
            return False

        return self.__get(
            resource_id=inference_id, return_data=False, raise_exception=raise_exception,
            error_message=NO_INFERENCE_ID.format(inference_id=str(inference_id).strip())
        )

    def get_by_id(self, inference_id: str, print_stdout: bool = True) -> Dict:
        if inference_id is None or inference_id == "":
            raise ValueError("inference_id cannot be empty or None")

        err_msg = NO_INFERENCE_ID.format(inference_id=str(inference_id).strip())

        inference_data = self.__get(
            resource_id=inference_id, return_data=True,
            raise_exception=True, error_message=err_msg
        )

        if print_stdout:
            self.__print_info(inferences=[inference_data], error_message=err_msg)

        return inference_data

    def get_all(self, print_stdout: bool = True) -> List[Dict]:
        inference_hub_data = self.__get(
            resource_id=None, return_data=True,
            raise_exception=True, error_message=NO_INFERENCES
        )

        if print_stdout:
            self.__print_info(inferences=inference_hub_data, error_message=NO_INFERENCES)

        return inference_hub_data

    def spawn(
            self, inference_name: str, inference_id: str, plan_id: str, namespace_id: str, inference_display_name: str,
            inference_model_image_name: str, inference_model_tag_id: str, resource_threshold: int = 80,
            envs: List[Dict] = (), ports: List[Dict] = (), args: List[Dict] = (), command: str = None,
            model_type: str = 'VLLM', num_replicas: int = 1, min_num_replicas: int = 1, max_num_replicas: int = 2,
            volume_path: str = '/data/model-storage',
    ) -> (str, str):

        inference_data = self.get_by_id(inference_id=inference_id, print_stdout=False)
        validate_inference_name(inference_name)
        self.__namespace.validate_id(namespace_id=namespace_id, raise_exception=True)
        datacenter_id = self._validate_plan_and_get_datacenter(plan_id, PLAN_TYPE_INFERENCE_HUB)
        validate_inference_replicas(num_replicas, min_num_replicas, max_num_replicas, raise_exception=True)
        validate_resource_threshold(resource_threshold, raise_exception=True)
        validate_model_type(model_type, raise_exception=True)

        validate_model_tag_info(
            model_tag_id=inference_model_tag_id, display_name=inference_display_name,
            model_image_name=inference_model_image_name, inference_model_tags=inference_data['modelTags'],
            exception_message=f"Model Tag information (inference_model_tag_id, inference_display_name, inference_model_image_name) doesn't match with any of the Model Tags in the provided inference_id({inference_id}).",
            raise_exception=True
        )

        response = requests.post(
            f"{self._api_auth.app_url}/api/v1/spawnedInferences",
            headers={'Content-Type': 'application/json', 'source': 'sdk'},
            auth=self._api_auth.get_api_creds(),
            data=json.dumps({
                "dataCenterId": datacenter_id,
                "inferenceId": inference_id,
                "kioskArray": None,
                "replicas": num_replicas,
                "maxReplicas": max_num_replicas,
                "minReplicas": min_num_replicas,
                "modelType": model_type,
                "name": inference_name,
                "namespaceId": namespace_id,
                "nodePreference": "NO PREFERENCE",
                "dockerImageVersion": {
                    "displayName": inference_display_name,
                    "modelImage": inference_model_image_name,
                    "_id": inference_model_tag_id
                },
                "parameters": {
                    "ports": ports,
                    "envs": envs,
                    "args": args,
                    "command": command,
                    "volumePath": volume_path
                },
                "planId": plan_id,
                "threshold": resource_threshold
            })
        )

        if response.status_code == 201 and response.json()['success']:
            if response.json().get('data', None) is not None and response.json()['data'].get('k8sName',
                                                                                             None) is not None:
                print(
                    f"Successfully spawned `{inference_name}` with pod: `{response.json()['data']['k8sName']}`. Wait a minute, check the logs in the Web UI, then use `get_spawned_inference_id_by_pod_name({response.json()['data']['k8sName']})` to retrieve the inference ID."
                )
            else:
                print(
                    f"Successfully spawned `{inference_name}` but unable to fetch inference-pod-name. PLEASE CONTACT THE ADMIN to get the inference-pod-name."
                )
        else:
            api_error(status_code=response.status_code, message=response.text)

    def validate_spawned_inference_id(self, spawned_inference_id: str, raise_exception: bool = False) -> bool:
        if spawned_inference_id is None or spawned_inference_id == "":
            if raise_exception:
                raise ValueError("spawned_inference_id cannot be None or empty")
            return False

        return self.__get_spawned_inference(
            resource_id=spawned_inference_id, return_data=False, raise_exception=raise_exception,
            error_message=NO_SPAWNED_INFERENCE_ID.format(spawned_inference_id=str(spawned_inference_id).strip())
        )

    def get_spawned_inference_by_id(self, spawned_inference_id: str, print_stdout: bool = True) -> Dict:
        if spawned_inference_id is None or spawned_inference_id == "":
            raise ValueError("spawned_inference_id cannot be empty or None")

        err_msg = NO_SPAWNED_INFERENCE_ID.format(spawned_inference_id=str(spawned_inference_id).strip())

        inference_data = self.__get_spawned_inference(
            resource_id=spawned_inference_id, return_data=True,
            raise_exception=True, error_message=err_msg
        )

        if print_stdout:
            self.__print_info(inferences=[inference_data], error_message=err_msg, processing_for_spawned_inference=True)

        return inference_data

    def get_all_spawned_inferences(self, print_stdout: bool = True) -> List[Dict]:
        spawned_inferences_data = self.__get_spawned_inference(
            resource_id=None, return_data=True, raise_exception=True, error_message=NO_INFERENCES,
        )

        if print_stdout:
            self.__print_info(
                inferences=spawned_inferences_data, error_message=NO_SPAWNED_INFERENCE,
                processing_for_spawned_inference=True
            )

        return spawned_inferences_data

    def get_spawned_inference_id_by_pod_name(self, spawned_inference_pod_name: str) -> str:
        if not isinstance(spawned_inference_pod_name, str):
            raise TypeError('spawned_inference_pod_name can only be of type str')

        if spawned_inference_pod_name is None or spawned_inference_pod_name == "":
            raise ValueError("spawned_inference_pod_name cannot be empty or None")

        err_msg = NO_SPAWNED_INFERENCE_POD_NAME.format(
            spawned_inference_pod_name=str(spawned_inference_pod_name).strip())

        response = requests.get(
            url=f"{self._api_auth.app_url}/api/v1/spawnedInferences", headers={'Content-Type': 'application/json'},
            auth=self._api_auth.get_api_creds(), params={'k8sName': spawned_inference_pod_name}
        )

        if response.status_code == 200 and response.json()['success'] and response.json().get('data',
                                                                                              None) is not None and len(
            response.json()['data']) > 0:
            return response.json()['data'][0]['_id']

        api_error(status_code=response.status_code, message=err_msg)


class _Chat:
    def __init__(
            self, chat_id: str, response: str, inference_id: str, model_name: str, prompt: str,
            chat_epoch_time: int, chat_prompt_tokens: int, chat_total_tokens: int, chat_completion_tokens: int
    ):
        self.__chat_id = chat_id
        self.__prompt = prompt
        self.__response = response
        self.__inference_id = inference_id
        self.__model_name = model_name
        self.__chat_epoch_time = self.convert_epoch_to_datetime(chat_epoch_time)
        self.__chat_prompt_tokens = chat_prompt_tokens
        self.__chat_total_tokens = chat_total_tokens
        self.__chat_completion_tokens = chat_completion_tokens

    @staticmethod
    def convert_epoch_to_datetime(epoch_time) -> str:
        return datetime.fromtimestamp(epoch_time).strftime("%b %d %H:%M:%S %Y")

    def get_chat_info(self) -> dict:
        return {
            'chat_id': self.__chat_id, 'response': self.__response, 'inference_id': self.__inference_id,
            'model_name': self.__model_name, 'chat_epoch_time': self.__chat_epoch_time,
            'chat_prompt_tokens': self.__chat_prompt_tokens, 'chat_total_tokens': self.__chat_total_tokens,
            'chat_completion_tokens': self.__chat_completion_tokens, 'prompt': self.__prompt
        }

    def __str__(self) -> str:
        chat_string = f""" {self.__chat_epoch_time}
    Prompt: {self.__prompt}
    Response: {self.__response}
    Chat ID: {self.__chat_id} | Inference ID: {self.__inference_id} | Model Name: {self.__model_name}
    Prompt Info = Prompt Tokens: {self.__chat_prompt_tokens} | Total Tokens: {self.__chat_total_tokens} | Completion Tokens: {self.__chat_completion_tokens}
        """
        return chat_string


class InferenceChat(ZBLBase):
    def __init__(self, api_auth: APIAuth, spawned_inference_id: str):
        InferenceHub(api_auth=api_auth).validate_spawned_inference_id(
            spawned_inference_id=spawned_inference_id, raise_exception=True
        )
        super().__init__(api_auth)
        self.__spawned_inference_id = spawned_inference_id
        self.__chat_history = []

    def get_all(self, print_stdout: bool = True) -> List[dict]:
        res = []
        if print_stdout:
            print("Chat History:")
        for chat_idx, history in enumerate(self.__chat_history[::-1]):
            if print_stdout:
                print(f"{chat_idx + 1}. {str(history)}")
            res.append(history.get_chat_info())
        return res

    def chat(self, prompt: str) -> str:
        if not isinstance(prompt, str):
            raise TypeError('prompt can only be of type str')
        if prompt is None or prompt == "":
            raise ValueError("prompt cannot be empty or None")

        response = requests.post(
            url=f"{self._api_auth.app_url}/api/v1/spawnedInferences/chat/completion/{self.__spawned_inference_id}",
            headers={'Content-Type': 'application/json', 'source': 'sdk'},
            auth=self._api_auth.get_api_creds(), data=json.dumps({"message": prompt})
        )

        if response.status_code == 200 and response.json()['success']:
            chat_data = response.json()['data']
            self.__chat_history.append(
                _Chat(
                    chat_id=chat_data['id'], response=chat_data['choices'][0]['text'].strip(),
                    inference_id=self.__spawned_inference_id, model_name=chat_data['model'],
                    chat_epoch_time=chat_data['created'], prompt=prompt,
                    chat_prompt_tokens=chat_data['usage']['prompt_tokens'],
                    chat_total_tokens=chat_data['usage']['total_tokens'],
                    chat_completion_tokens=chat_data['usage']['completion_tokens']
                )
            )
            return chat_data['choices'][0]['text'].strip()
        else:
            api_error(status_code=response.status_code, message=response.text)
