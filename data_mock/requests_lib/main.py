import json
class RequestsResponse():

    def __init__(self, status_code:int, reason:str, 
            json_data:dict = None, ok:bool= True, 
            text:str = None):
        self.status_code = status_code
        self.reason = reason
        self.json_data = json_data
        self.ok = ok
        if text == None:
            self.text = str(json_data)
        else:
            self.text = text

    def json(self) -> dict:
        if self.json_data == None:
            return json.loads('')
        return self.json_data

    def iter_lines(self):
        def my_gen():
            for i in range(0):
                yield self.json_data
        return my_gen()

class Requests:

    def __init__(self, json_data = None):
        self.json = json_data
        self.return_dict = {}
        self.default_dict = {'reason':'OK', 'status_code':200, 'json_data': {}, 
                'text' : str({}), 'ok':True}
        self.register_initial_mock_data()

    def register_initial_mock_data(self):
        pass

    def register_data(self, url:str, status_code:int, reason:str = None,
            json_data:dict = None, text:str = None, ok:bool = None):
        d = {'status_code':status_code, 'json_data' : json_data}
        if status_code > 299 and ok == None:
            d['ok'] = False
        elif ok == None:
            d['ok'] = True
        if reason == None and status_code < 299:
            d['reason'] = 'OK'
        elif reason == None and status_code == 401:
            d['reason'] = 'Unauthorized'
        else:
            d['reason'] = 'Notok'
        if status_code < 299 and json_data != None:
            d['text'] = str(json_data)
        elif status_code < 299:
            d['text'] = ''
        elif status_code == 401:
            d['text'] = 'Not Authorized'
        self.return_dict[url] = d

    def _make_resp(self, url):
        d = self.return_dict.get(url)
        if d == None :
            d = self.default_dict
        o = RequestsResponse(status_code = d['status_code'],
                reason = d['reason'],
                json_data = d['json_data'],
                text = d['text'],
                ok = d['ok'],

                )
        return o

    def get(self, url:str, params=None, **kwargs):
        return self._make_resp(url)

    def options(self, url:str, **kwargs):
        raise NotImplementedError('not implemented')

    def head(self, url:str, **kwargs):
        raise NotImplementedError('not implemented')

    def post(self, url:str, data=None, json=None, **kwargs):
        pass

    def put(self, url:str, data=None, **kwargs):
        pass

    def patch(self, url:str, data=None, **kwargs):
        pass

    def delete(self, url:str, **kwargs):
        pass
