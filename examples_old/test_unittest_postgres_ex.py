import data_mock.psycopg2 as mock_psycopg2
from unittest import mock

class GoodUser(mock_psycopg2.Connect):

    def cursor(self, cursor_factory = None):
        mock_data1 = [
        [('email', 'some_user@domain.com'), ('password', 'hash_pwd')],
            ]
        o = mock_psycopg2.extras.RealDictCursor()
        o.register_mock_data(key = 'default', mock_data = mock_data1)
        return  o

@mock.patch('psycopg2.connect', side_effect =GoodUser)
def test_read_main4(m):
    url = '/token'
    payload = {'username':'some_user@somedomain.com','password':'unhashed'}
    response = client.post(url, data = payload)
    assert response.status_code == 200
