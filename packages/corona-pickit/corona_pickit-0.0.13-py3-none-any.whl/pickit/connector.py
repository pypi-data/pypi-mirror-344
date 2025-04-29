import json
import logging
import requests
from json.decoder import JSONDecodeError

logger = logging.getLogger(__name__)

class ConnectorException(Exception):
    def __init__(self, message, description, code):
        self.code = code
        self.message = message
        self.description = description
        super().__init__(message)

class Connector:
    def __init__(self, headers=None, verify_ssl=True):
        # Si no se pasan headers, se pueden agregar los de autenticación por defecto aquí
        self.headers = headers if headers else {}
        self.verify_ssl = verify_ssl

    def _handle_response(self, response, object_name, url):
        if response.status_code == 400:
            raise ConnectorException(response.content, response.text, 400)
        if response.status_code == 422:
            raise ConnectorException(
                f'Error:  {response.json()}', response.text, 422)
        if response.status_code == 401:
            raise ConnectorException(
                f'Unauthorized operation over {object_name}', response.text, 401)
        if response.status_code == 404:
            raise ConnectorException(
                f'Not found error trying to access to {url}', response.text, 404)
        if response.status_code not in [200, 201]:
            raise ConnectorException(
                f'Fail operation to {url}', response.text, response.status_code,)
        if isinstance(response.json, dict):
            return response.json
        try:
            return json.loads(response.content)
        except JSONDecodeError:
            return response.content.decode('utf-8')

    def get(self, url, object_name='this objects', headers=None):
        logger.debug(f'Getting url {url}')
        # Si se pasan headers a la solicitud, se usan en lugar de los headers por defecto
        final_headers = headers if headers else self.headers
        response = requests.get(url, headers=final_headers, verify=self.verify_ssl)
        return self._handle_response(response, object_name, url)

    def post(self, url, data, object_name='this objects', headers=None):
        logger.debug(f'Creating {object_name} to {url}')
        # Si se pasan headers a la solicitud, se usan en lugar de los headers por defecto
        final_headers = headers if headers else self.headers
        response = requests.post(url, json=data, headers=final_headers, verify=self.verify_ssl)
        return self._handle_response(response, object_name, url)

    def put(self, url, data, object_name, headers=None):
        logger.debug(f'Updating {object_name} to {url}')
        final_headers = headers if headers else self.headers
        response = requests.put(url, json=data, headers=final_headers, verify=self.verify_ssl)
        return self._handle_response(response, object_name, url)

    def delete(self, url, object_name, headers=None):
        logger.debug(f'Deleting {object_name} from {url}')
        final_headers = headers if headers else self.headers
        response = requests.delete(url, headers=final_headers, verify=self.verify_ssl)
        return self._handle_response(response, object_name, url)
