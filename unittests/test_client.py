import sys
import unittest
import pytest

sys.path.append('.')

import data_mock.gcp.client as client
import data_mock.gcp.bigquery as bigquery
import data_mock.gcp.table as table
from data_mock.gcp.client import DataValidationError

#from google.cloud import bigquery

class ClassTest1(client.Client):
    pass

class ClassTest2(client.Client):

    def query(self, query):
        return self.run_query(
                data = [[('first-key', 1), ('second-key', 2)]], 
                meta = {})

class ClassTest3(client.Client):

    def query(self, query):
        return self.run_query(
                data = 1, meta = {})

class ClassTest4(client.Client):

    def query(self, query):
        return self.run_query(
                data = [1], meta = {})

class ClassTest5(client.Client):

    def query(self, query):
        return self.run_query(
                data = [[1]], meta = {})

class ClassTest6(client.Client):

    def query(self, query):
        return self.run_query(
                data = [[(1)]], meta = {})

class ClassTest7(client.Client):

    def query(self, query):
        return self.run_query(
                data = [[('first-key', 1), ('second-key', 2)]], 
                meta = 1)

class ClassTest8(client.Client):
    """For testing create table"""
    pass

class ClassTest9(client.Client):
    """test mock list of tables"""
    def initialize_table_list(self):
        self.create_table_list({'x':'y'})

class ClassTest10(client.Client):
    """test mock list of tables"""
    pass

class ClassTest11(client.Client):
    """test mock list of tables 2"""
    def initialize_table_list(self):
        self.create_table_list([{'table_ref':'mock1'}])

class ClassTest12(client.Client):
    """test mock list of tables"""
    def initialize_table_list(self):
        self.create_table_list([None])

class ClassTest13(client.Client):
    pass

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


def test_create_table_has_right_atts():
    client = ClassTest8()
    dataset_id = 'mock'
    dataset_ref = client.dataset(dataset_id)
    table_id = 'mock'
    table_ref = dataset_ref.table(table_id)
    table_ref = 'mock'
    schema = 'mock'
    table = bigquery.Table(table_ref, schema=schema)
    partition_field = 'mock'
    require_partition_filter = True
    table.time_partitioning = bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY, 
                field = partition_field, 
                require_partition_filter = require_partition_filter)
    clustering_fields = ['a', 'b']
    table.clustering_fields = clustering_fields
    description = ''
    table.description = description
    table = client.create_table(table)  
    assert hasattr(table, 'path')
    assert hasattr(table, 'table_id')
    assert table.table_id == 'mock'

def test_bad_list_of_tables_raises_error():
    with pytest.raises(DataValidationError) as e_info:
        client = ClassTest9()

def test_bad_list_of_tables_raises_error2():
    with pytest.raises(DataValidationError) as e_info:
        client = ClassTest12()

def test_list_of_tables_does_not_raise_error():
    client = ClassTest10()

def test_list_of_tables_has_right_table_id():
    client = ClassTest11()
    l = client.list_tables()
    assert l[0].table_id == 'mock1'

def test_create_table_creates_table_with_right_id():
    client = ClassTest13()
    t = client.create_table(table = 'mock1')
    assert isinstance(t, table.Table)
    l = client.list_tables()
    assert l[0].table_id == 'mock1'
    l_tables = client.list_tables()
    assert len(l_tables) == 1
    assert l_tables[0].table_id == 'mock1'

