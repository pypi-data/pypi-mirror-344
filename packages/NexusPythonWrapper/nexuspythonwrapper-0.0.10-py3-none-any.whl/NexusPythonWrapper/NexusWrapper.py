import base64
import logging
import requests

from .endpoints import NexusEndpoints
from .exceptions import AuthenticationError, CredentialsError
from .NexusFilter import NexusFilter
from .NexusSort import NexusSort
from .models import Result

class NexusWrapper:
    def __init__(self, uri: str, authentication_type, api_key: str = None, username: str = None, password: str = None,
                 logger : logging.Logger = None, ssl_verify: bool = True):
        """
        Constructor method for NexusWrapper
        :param uri:                 In the form - "https://database.nexusic.com/" + "test/" for the test instance of the database
        :param authentication_type: APIKEY or BASIC
        :param api_key:             NEXUS account apikey, to be used with authentication_type = APIKEY
        :param username:            NEXUS account username, to be used with authentication_type = BASIC, in the form username@nexusic.com
        :param password:            NEXUS account password, to be used with authentication_type = BASIC
        :param logger:
        :param ssl_verify:
        """

        self._uri = uri
        self._authentication_type = authentication_type.upper()
        self._api_key = api_key
        self._username = username
        self._password = password
        self._logger = logger or logging.getLogger(__name__)
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            requests.packages.urllib3.disable_warnings()

        self._validate_authentication()
        self._encoded_credentials = self._encode_credentials(self._api_key if self._authentication_type == 'APIKEY' else f'{self._username}:{self._password}')

        self._authentication_header = {'Authorization': f'{self._authentication_type} {self._encoded_credentials}'}

        self._endpoints = NexusEndpoints(self._uri)

        self._login()
        self._base_params = {'hash': self._hash}
        self._get_version()

    def _validate_authentication(self):
        """
        Validate the authentication_type is either APIKEY or BASIC
        Validate the NEXUS account related parameters are compatible with the authentication_type
        """

        authentication_types = {'APIKEY', 'BASIC'}
        if self._authentication_type not in authentication_types:
            raise AuthenticationError(f'Authentication Type: {self._authentication_type} is not valid. Use \'APIKEY\' or \'BASIC\'')
    
        if self._authentication_type == 'APIKEY':
            if not self._api_key:
                raise CredentialsError('Authentication Type: APIKEY requires an api_key')
        else:
            if not self._username:
                raise CredentialsError('Authentication Type: BASIC requires a username')
            if not self._password:
                raise CredentialsError('Authentication Type: BASIC requires an password')

    def _encode_credentials(self, s: str):
        """
        Base64 encode the authentication credentials for login
        :param s: if authentication type = APIKEY, s = apikey, else s = username:password
        """

        return base64.b64encode(s.encode('utf-8')).decode('utf-8')

    def _login(self):
        """
        POST request on the NEXUS login endpoint
        Set hash value for future requests and other misc items
        """

        full_url = self._endpoints.login_endpoint()

        response = self._request(http_method='POST', url=full_url, headers=self._authentication_header)

        self._hash = response.metadata.get('hash', None)
        self._userId = response.metadata.get('id', None)
        self._username = response.metadata.get('username', None)
        self._user = response.metadata.get('name', None)
        self._license = response.metadata.get('license', None)

    def _get_version(self) -> None:
        """
        GET request on the NEXUS version endpoint
        Set version and schema for information
        """

        full_url = self._endpoints.version_endpoint()

        response = self._request(http_method='GET', url=full_url)

        self._version = response.metadata.get('version', None)
        self._schema = response.metadata.get('schema', None)

    def _request(self, http_method: str, url: str, headers: dict = None, data: dict = None, field_name: str = None,
                 pre_delete_result: Result = None, ssl_verify = True) -> Result:
        """
        Log params and perform a request, send the response to the validate method
        :param http_method:       HTTP method as defined by the method which calls this method
        :param url:               full_url to the NEXUS endpoint
        :param headers:           header dict containing either or both X-NEXUS-Filter and X-NEXUS-Sort
        :param data:              dict containing request body
        :param field_name:        NEXUS database field name
        :param pre_delete_result: Result class instance containing the row of a table which is about to be deleted
        :param ssl_verify:
        """

        self._logger.debug(f'http_method={http_method}, url={url}, headers={headers}, json={data}, field_name={field_name}')
        response = requests.request(method=http_method, url=url, json=data, headers=headers, verify=self._ssl_verify)
        return self._validate_response(response, field_name=field_name, pre_delete_result=pre_delete_result)

    def _validate_response(self, response: requests.Response, field_name: str = None, pre_delete_result: Result = None) -> Result | None:
        """
        Validates the response from _request and returns a Result instance
        :param response:          Response from _request
        :param field_name:        NEXUS database field name
        :param pre_delete_result: Result class instance containing the row of a table which is about to be deleted
        """
        
        status_code = response.status_code
        content_type = response.headers.get('Content-Type', '')
        message = response.reason

        if status_code < 200 or status_code > 299:
            self._logger.error(msg=f'status_code:{status_code}, message: {message}')
            raise Exception(f'status_code:{status_code}, message: {message}')
        
        if not response.content:
            self._logger.debug(msg=f'status_code: {status_code}, message: {message}')
            return Result(status_code=status_code, message=message)

        if status_code == 204:
            self._logger.debug(msg=f'status_code: {status_code}, message: {message}')
            if pre_delete_result:
                pre_delete_result.status_code = status_code
                pre_delete_result.message = message
            return pre_delete_result

        if 'application/json' in content_type:
            try:
                data = response.json()
                self._logger.debug(msg=f'status_code: {status_code}, message: {message}, result: {data}')
                return Result(
                    status_code=status_code,
                    message=message,
                    result=data.get('rows', []),
                    metadata={k: v for k, v in data.items() if k != 'rows'}
                )
            except ValueError:
                self._logger.error(msg=f'status_code: {status_code}, message: Response was not a valid json')
                raise AuthenticationError('Response was not a valid json')

        if 'text/plain' in content_type:
            try:
                self._logger.debug(msg=f'status_code: {status_code}, message: {message}, result: {[{field_name: response.text}]}')
                return Result(status_code=status_code, message=message, result=[{field_name: response.text}])
            except ValueError:
                self._logger.error(msg=f'status_code: {status_code}, message: Response was not valid plain text')
                raise AuthenticationError('Response was not valid plain text')

        return None

    def connection_details(self) -> None:
        """
        Prints information about the connected NEXUS database and user
        """
        
        print(f'Database:         {self._uri}')
        print(f'Database Version: {self._version}')
        print(f'Database Schema:  {self._schema}')
        print(f'User:             {self._user}')
        print(f'License:          {self._license}')

    def create_request_headers(nexus_filter: NexusFilter, nexus_sort: NexusSort) -> dict | None:
        """
        Helper method to create a header dict from NexusFilter and NexusSort instances
        :param nexus_filter: NexusFilter instance
        :param nexus_sort:   NexusSort instance
        """

        if not nexus_filter or not nexus_sort:
            return None

        headers = {}
        if nexus_filter:
            headers['X-NEXUS-Filter'] = nexus_filter.build()
        if nexus_sort:
            headers['X-NEXUS-Sort'] = nexus_sort.build()

        return headers

    def logout(self) -> None:
        """
        Invalidates hash
        """

        full_url = self._endpoints.logout_endpoint(params=self._base_params)

        response = self._request(http_method='GET', url=full_url)

        self.logout_status_code = response.status_code

    def get(self, table_name: str, key_value: int = None, field_name: str = None,
        headers: dict = None, paginated: bool = True, page_size: int = None,
        start_row: int = None, calculated_values: bool = None) -> Result:
        """
        Precursor method to make a GET request
        Subsequent calls: _get_rows:      when table_name is passed into the method
                          _get_row:       when table_name, key_value, are passed into the method
                          _get_row_field: when table_name, key_value, field_name are passed into the method
        :param table_name:                                NEXUS database table
        :param key_value:         _get_row                specified row in the table which is to be returned
        :param field_name:        _get_row_field:         NEXUS database field which value is to be returned
        :param headers:           _get_rows:              dict containing either or both X-NEXUS-Filter and X-NEXUS-Sort
        :param paginated:         _get_rows:              if true, all rows are returned by pagination
        :param page_size:         _get_rows:              determines how many rows are returned per request
        :param start_row:         _get_rows:              truncates rows up to the defined start row
        :param calculated_values: _get_rows or _ get_row: determines if the calculated values in a row are retuned
        """

        params = dict(self._base_params)

        if not key_value and not field_name:
            return self._get_rows(table_name=table_name, params=params, headers=headers, paginated=paginated,
                                  page_size=page_size, start_row=start_row, calculated_values=calculated_values)

        if key_value and not field_name:
            return self._get_row(table_name=table_name, key_value=key_value, params=params, calculated_values=calculated_values)   

        return self._get_row_field(table_name=table_name, key_value=key_value, field_name=field_name, params=params)

    def _get_rows(self, table_name: str, params: dict, headers: dict = None, paginated: bool = True,
                  page_size: int = 100, start_row: int = None, calculated_values: bool =True) -> Result:
        """
        Setup method for GET request for multiple rows, handles pagination
        :param table_name:        NEXUS database table
        :param headers:           dict containing either or both X-NEXUS-Filter and X-NEXUS-Sort
        :param paginated:         if true, all rows are returned by pagination
        :param page_size:         determines how many rows are returned per request
        :param start_row:         truncates rows up to the defined start row
        :param calculated_values: determines if the calculated values in a row are retuned
        """

        result = None

        current_row = start_row if start_row is not None else 0
        page_size = page_size if page_size is not None else 100
        params['pageSize'] = page_size
        params['calculatedValues'] = calculated_values

        while True:
            params['startRow'] = current_row
            full_url = self._endpoints.row_endpoint(table_name=table_name, params=params)
            response = self._request(http_method='GET', url=full_url, headers=headers)

            if not result:
                result = response
            else:
                result.extend(response)

            if not paginated:
                break

            current_row += page_size
            if current_row > response.metadata.get('totalRows', 0):
                break

        return result

    def _get_row(self, table_name: str, key_value: int, params: dict, calculated_values: bool = True) -> Result:
        """
        Setup method for GET request for single rows
        :param table_name:        NEXUS database table
        :param key_value:         specified row in the table which is to be returned
        :param calculated_values: determines if the calculated values in a row are retuned
        """

        params['calculatedValues'] = calculated_values

        full_url = self._endpoints.row_endpoint(table_name=table_name, params=params, key_value=key_value)

        return self._request(http_method='GET', url=full_url)

    def _get_row_field(self, table_name: str, key_value: int, field_name: str, params: dict) -> Result:
        """
        Setup method for GET request for a field within a single rows
        :param table_name: NEXUS database table
        :param key_value:  specified row in the table which is to be returned
        :param field_name: NEXUS database field which value is to be returned
        """

        full_url = self._endpoints.row_endpoint(table_name=table_name, params=params, key_value=key_value, field_name=field_name)

        return self._request(http_method='GET', url=full_url, field_name=field_name)

    def put(self, table_name:str, request_body: dict, calculated_values: bool = True) -> Result:
        """
        Setup method for PUT request

        NEXUS PUT = Create new row

        :param table_name:       NEXUS database table
        :param request_body:     defines the fields and values in the table
        :param calculated_values: determines if the calculated values in a row are retuned
        """

        params = dict(self._base_params)
        params['calculatedValues'] = calculated_values

        full_url = self._endpoints.row_endpoint(table_name, params, key_value=0)

        return self._request(http_method='PUT', url=full_url, data=request_body)

    def post(self, table_name: str, key_value: int, request_body: dict, calculated_values: bool = True) -> Result:
        """
        Setup method for POST request

        NEXUS POST = Update existing row

        :param table_name:        NEXUS database table
        :param key_value:         specified row of the table which is to be updated
        :param request_body:      defines the fields and values in the table
        :param calculated_values: determines if the calculated values in a row are retuned
        """

        params = dict(self._base_params)
        params['calculatedValues'] = calculated_values

        full_url = self._endpoints.row_endpoint(table_name, params, key_value=key_value)

        return self._request(http_method='POST', url=full_url, data=request_body)

    def delete(self, table_name: str, key_value: int) -> Result:
        """
        Setup method for DELETE request

        :param table_name: NEXUS database table
        :param key_value:  specified row of the table which is to be deleted
        """

        full_url = self._endpoints.row_endpoint(table_name, self._base_params, key_value)

        pre_delete_result = self.get(table_name=table_name, key_value=key_value)
        return self._request(http_method='DELETE', url=full_url, pre_delete_result=pre_delete_result)
