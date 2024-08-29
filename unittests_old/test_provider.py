import sys
sys.path.append('.')
import types

import unittest

import data_mock.mock_helpers.provider as provider

class CustomProvider1:

    def __init__(self):
        self.__call_no = 0

    def gen_func1(self):
        for i in range(10):
            yield [provider.Data(name = 'field', value = i)]

    def gen_func2(self):
        return 
        yield

    def query_results(self):
        self.__call_no += 1
        if self.__call_no == 1:
            return self.gen_func2(), {'total_rows':0}
        else:
            return self.gen_func1(), {'total_rows':10}


class TestProvider(unittest.TestCase):

    def test_default(self):
        provide = provider.ProvideData()
        data = [
            [('num', 1), ('field', 'foo')],
            [('num', 2)]
            ]
        provide.add_data(data = data, tag = 'default')
        g, metadata = provide.get_data('default')
        for i in g:
            for j in i:
                self.assertTrue(hasattr(j,'name'))

    def test_custom_provider(self):
        provide = provider.ProvideData()
        provide.add_data(data = CustomProvider1(), tag = 'f')
        g, metadata = provide.get_data('f')
        self.assertTrue(isinstance(g,  types.GeneratorType))
        self.assertEqual(metadata['total_rows'], 0)
        g, metadata = provide.get_data('f')
        for i in g:
            for j in i:
                self.assertTrue(hasattr(j,'name'))

    def test_empty_list_returns_generator(self):
        provide = provider.ProvideData()
        data = []
        provide.add_data(data = data, tag = 'default')
        num_rows = 0
        g, metadata = provide.get_data('default')
        self.assertTrue(isinstance(g,  types.GeneratorType))
        for i in g:
            num_rows += 1
        self.assertEqual(num_rows, 0)

if __name__ == '__main__':
    unittest.main()
