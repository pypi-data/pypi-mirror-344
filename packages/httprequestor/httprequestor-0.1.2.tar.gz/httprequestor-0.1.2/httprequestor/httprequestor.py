import urllib3
import json


class HttpRequestor:
    """ Requestor Making HTTP Requests Easier
    
    This class is created to help make easy and constant. Making the interchanging of different HTTP libraries easy and only changeable in one place.

    The base URL is created to be a constant, with the optiont to change all the other values as the class is used.
    """

    _url: str = None
    _path: str = None
    _headers: dict = None
    _body: dict  = None
    _fields: dict = None
    _params: dict = None
    _http = urllib3.PoolManager()

    def __init__(self, url: str):
        self._url = url

    def set_path(self, path: str):
        self._path = path
        return self

    def set_headers(self, headers: dict):
        self._headers = headers
        return self

    def set_body(self, body: dict):
        self._body = body
        return self
    
    def set_fields(self, fields):
        self._fields = fields
        return self
    
    def set_params(self, params: dict):
        self._params = params
        return self
    
    def send_get(self):

        return ResponseModel(self._http.request(
            'GET',  
            self._url + self._path,
            headers=self._headers,
            fields=self._params))

    def send_post(self):

        encoded_body = None
        if self._body is not None:
            encoded_body = json.dumps(self._body)
        
        return ResponseModel(self._http.request(
            'POST',
            self._url + self._path,
            headers=self._headers,
            body=encoded_body,
            fields=self._fields))
    
    def send_put(self):

        encoded_body = None
        if self._body is not None:
            encoded_body = json.dumps(self._body)
        
        return ResponseModel(self._http.request(
            'PUT',
            self._url + self._path,
            headers=self._headers,
            body=encoded_body,
            fields=self._fields))
    
    def send_patch(self):

        encoded_body = None
        if self._body is not None:
            encoded_body = json.dumps(self._body)
        
        return ResponseModel(self._http.request(
            'PATCH',
            self._url + self._path,
            headers=self._headers,
            body=encoded_body,
            fields=self._fields))
    
    def send_delete(self):

        return ResponseModel(self._http.request(
            'DELETE',
            self._url + self._path,
            headers=self._headers,
            fields=self._params))
    

class ResponseModel:
    
    status = 0
    is_success = False
    data = None
    headers = None

    def __init__(self, rsp):
        self.status = rsp.status
        self.is_success = self.set_success(rsp.status)
        self.headers = rsp.headers

        if rsp.data is not None and rsp.data != b'':

            if 'application/json' in rsp.headers.get('Content-Type'):
                self.data = json.loads(rsp.data)
            else:
                self.data = rsp.data

    def __str__(self):
        return f"HttpRequestor->ResponseModel(status={self.status},is_success={self.is_success},data={self.data})"
    
    def __repr__(self):
        return f"HttpRequestor->ResponseModel(status={self.status},is_success={self.is_success},data={self.data})"

    def set_success(self, status: int):
        if status >= 200 and status < 300:
            return True
        else:
            return False
