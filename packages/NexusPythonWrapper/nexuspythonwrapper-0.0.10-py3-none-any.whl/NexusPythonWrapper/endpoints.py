from urllib.parse import urlencode

class NexusEndpoints:
    def __init__(self, base_uri: str) -> None:
        self.base_uri = base_uri.rstrip('/')

    def login_endpoint(self) -> str:
        return f'{self.base_uri}/data/icweb.dll/security/login'

    def logout_endpoint(self, params: dict = None) -> str:
        uri = f'{self.base_uri}/data/icweb.dll/security/logout'

        if params:
            uri = f'{uri}?{urlencode(params)}'

        return uri

    def version_endpoint(self) -> str:
        return f'{self.base_uri}/data/icweb.dll/version'

    def row_endpoint(self, table_name: str, params: dict, key_value: int = None, field_name: str = None) -> str:
        uri = f'{self.base_uri}/data/icweb.dll/bo/{table_name}/'
        
        if key_value is not None:
            uri += f'{key_value}'
            if field_name is not None:
                uri += f'/{field_name}'
                
        query = urlencode(params)
        if params:
            uri = f'{uri}?{query}'

        return uri

    def business_object_endpoint(self, table_name: str, params: dict) -> str:
        uri = f'{self.base_uri}/data/icweb.dll/bo/{table_name}'
        
        query = urlencode(params)
        
        if params:
            uri = f'{uri}?{query}'

        return uri