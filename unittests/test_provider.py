import sys
sys.path.append('.')

import unittest

import data_mock.mock_helpers.provider as provider


class TestProvider(unittest.TestCase):

    def test_default(self):
        provide = provider.ProvideData()
        data = [
            [('num', 1), ('field', 'foo')],
            [('num', 2)]
            ]
        provide.add_data(data = data, tag = 'default')
        x = provide.get_data('default')
        for i in x:
            for j in i:
                self.assertTrue(hasattr(j,'name'))

    def test_custom_provider(self):
        provide = provider.ProvideData()
        def my_func():
            for i in range(10):
                data_obj = provider.Data(name = 'num', value = i)
                yield [data_obj]
        #wrong here
        provide.add_data(data = my_func, tag = 'f')
        x = provide.get_data('f')
        for i in x:
            for j in i:
                self.assertTrue(hasattr(j,'name'))


    
if __name__ == '__main__':
    unittest.main()
