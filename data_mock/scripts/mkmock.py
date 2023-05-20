#!/usr/bin/env python3

import os
import argparse
from pathlib import Path
import shutil



def file_path(string):
    if os.path.isfile(string):
        return string
    else:
        raise argparse.ArgumentTypeError(f"bigquery-path:{string} is not a valid path")

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise argparse.ArgumentTypeError(f"bigquery-path:{string} is not a valid dir")

def _get_bigquery_code():
    return """from data_mock.google.cloud.bigquery import Client as Mock_Client
from data_mock.google.cloud.bigquery import DatasetReference as Mock_DatasetReference
from data_mock.google.cloud.bigquery import Table as Mock_Table
from data_mock.google.cloud.bigquery import SchemaField as Mock_SchemaField


class Client(Mock_Client):
    pass

class DatasetReference(Mock_DatasetReference):
    pass

class Table(Mock_Table):
    pass

class SchemaField(Mock_SchemaField):
    pass


    """


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices = ['create', 'destroy'], 
                        help="either create or delete")
    parser.add_argument("--bigquery-path", '-bq', 
                        help="path to bigquery mock module", 
                required = False, type = file_path)
    parser.add_argument("--dir-path", '-d', 
                        help="where to make directory", 
                default = '.', type = dir_path)
    return  parser.parse_args()


def main(command, bigquery_path, dir_path):
    cloud_path = os.path.join(dir_path, 'google', 'cloud')
    if command == 'create':
        shutil.rmtree('google', ignore_errors = True)
        Path(cloud_path).mkdir(parents=True, exist_ok=True)
        if bigquery_path:
            shutil.copyfile(bigquery_path, os.path.join(cloud_path, 'bigquery.py'))
        else:
            with open(os.path.join(cloud_path, 'bigquery.py'), 'w') as write_obj:
                write_obj.write(_get_bigquery_code())
    elif command == 'destroy':
        shutil.rmtree('google', ignore_errors = True)

if __name__ == '__main__':
    args = _get_args()
    main(command = args.command, 
         bigquery_path = args.bigquery_path,
         dir_path = args.dir_path)
