import sys
import unittest
import pytest

sys.path.append('.')

import data_mock.gcp.client as client
from data_mock.gcp.client import DataValidationError

from google.cloud import bigquery

class ClassTest1(client.Client):
    pass

class ClassTest2(client.Client):

    def query(self, query):
        return self.run_query(data = [[('first-key', 1), ('second-key', 2)]], m = {})

class ClassTest3(client.Client):

    def query(self, query):
        return self.run_query(
                data = 1, m = {})

class ClassTest4(client.Client):

    def query(self, query):
        return self.run_query(
                data = [1], m = {})

class ClassTest5(client.Client):

    def query(self, query):
        return self.run_query(
                data = [[1]], m = {})

class ClassTest6(client.Client):

    def query(self, query):
        return self.run_query(
                data = [[(1)]], m = {})

class ClassTest7(client.Client):

    def query(self, query):
        return self.run_query(
                data = [[('first-key', 1), ('second-key', 2)]], 
                m = 1)


def test_class1():
    client = ClassTest1()
    query_job = client.query('')
    rows = query_job.result()  
    for i in rows:
        print(i)

def test_class2():
    client = ClassTest2()
    query_job = client.query('')
    rows = query_job.result()  
    for counter, i in enumerate(rows):
        assert i.get('first-key') == 1
        for j in i.items():
            assert j == ('first-key', 1)
            break
        assert list(i.keys()) == ['first-key', 'second-key']
        assert i.values() == (1, 2)
    assert counter == 0

def test_class_data_not_list_raises_error():
    client = ClassTest3()
    with pytest.raises(DataValidationError) as e_info:
        query_job = client.query('')

def test_class_data_inside_list_not_list_raises_error():
    client = ClassTest4()
    with pytest.raises(DataValidationError) as e_info:
        query_job = client.query('')

def test_class_data_inside_list_of_list_not_tuple_raises_error():
    client = ClassTest5()
    with pytest.raises(DataValidationError) as e_info:
        query_job = client.query('')

def test_class_data_tuple_not_right_len_raises_error():
    client = ClassTest6()
    with pytest.raises(DataValidationError) as e_info:
        query_job = client.query('')

def test_class_meta_not_dict_raises_error():
    client = ClassTest7()
    with pytest.raises(DataValidationError) as e_info:
        query_job = client.query('')



