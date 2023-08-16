from setuptools import setup

setup(
    name='py-data-mock',
    version='0.0.14',    
    description='Mock Data',
    url='https://github.com/paulhtremblay/py-data-mock',
    author='Henry Tremblay',
    author_email='paulhtremblay@gmail.com',
    license='GNU GENERAL PUBLIC LICENSE',
    packages=['data_mock/google/cloud/bigquery/job', 'data_mock/google/cloud/bigquery',
        'data_mock/google/cloud/storage','data_mock/mock_helpers', 'data_mock',
        'data_mock/psycopg2/', 'data_mock/requests_lib/',
        ],
     classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing :: Mocking'
    ],
)
