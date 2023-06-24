import sys
sys.path.append('.')

import json

import unittest

import data_mock.requests

import types

class TestRequests(unittest.TestCase):

    def setUp(self):
        pass

    def  tearDown(self):
        pass

    def test_requests_has_method(self):
        requests = data_mock.requests.Requests() 
        self.assertTrue(hasattr(requests, 'get'))
        self.assertTrue(hasattr(requests, 'post'))
        self.assertTrue(hasattr(requests, 'patch'))
        self.assertTrue(hasattr(requests, 'delete'))

    def test_generic_get_has_right_objects(self):
        requests = data_mock.requests.Requests() 
        resp = requests.get(url = 'https://catfact.ninja/fact')
        self.assertEqual(resp.text, '{}')
        self.assertEqual(resp.ok, True)
        self.assertEqual(resp.json(), {})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(isinstance(resp.iter_lines(), types.GeneratorType))

    def test_register201(self):
        requests = data_mock.requests.Requests() 
        end_point = 'https://mock-endpoint'
        requests.register_data(status_code = 201, url = end_point)
        resp = requests.get(end_point)
        self.assertEqual(resp.status_code, 201)

    def test_register200_with_json(self):
        requests = data_mock.requests.Requests() 
        end_point = 'https://mock-endpoint'
        json_data = {'fields':'value'}
        requests.register_data(status_code = 200, url = end_point,
                json_data = json_data)
        resp = requests.get(end_point)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json_data, resp.json())

    def test_register401(self):
        requests = data_mock.requests.Requests() 
        end_point = 'https://mock-endpoint'
        requests.register_data(status_code = 401, url = end_point,
                )
        resp = requests.get(end_point)
        self.assertEqual(resp.status_code, 401)
        self.assertRaises(json.decoder.JSONDecodeError, resp.json)
        self.assertEqual(resp.ok, False)

if __name__ == '__main__':
    unittest.main()
