from data_mock.psycopg2.cursor import Cursor
from data_mock.psycopg2.extras import RealDictCursor

import data_mock.mock_helpers.provider as provider

from typing import Union, Type

class Connect:

    def __init__(self, dsn:None=None, connection_factory:None=None, 
            mock_data:Union[list, None] = None,  **kwargs):
        self.data_provider = provider.ProvideData()
        if mock_data:
            self.data_provider.add_data(data = mock_data, tag = 'default')
        self.register_initial_mock_data()
        
    def register_initial_mock_data(self):
        pass

    def register_mock_data(self, key:str, mock_data:list):
        self.data_provider.add_data(data = mock_data, tag = key)

    def cursor(self, cursor_factory: Union[Type[Cursor], Type[RealDictCursor]] \
            = Cursor) -> Union[Cursor, RealDictCursor]:
        return cursor_factory(data_provider = self.data_provider)

    def commit(self, *args, **kwargs):
        pass

    def close(self, *args, **kwargs):
        pass

    def DataError(self, *args, **kwargs):
         raise NotImplementedError()

    def DatabaseError(self, *args, **kwargs):
         raise NotImplementedError()

    def Error(self, *args, **kwargs):
         raise NotImplementedError()

    def IntegrityError(self, *args, **kwargs):
         raise NotImplementedError()

    def InterfaceError(self, *args, **kwargs):
         raise NotImplementedError()

    def InternalError(self, *args, **kwargs):
         raise NotImplementedError()

    def NotSupportedError(self, *args, **kwargs):
         raise NotImplementedError()

    def OperationalError(self, *args, **kwargs):
         raise NotImplementedError()

    def ProgrammingError(self, *args, **kwargs):
         raise NotImplementedError()

    def Warning(self, *args, **kwargs):
         raise NotImplementedError()

    def async_(self, *args, **kwargs):
         raise NotImplementedError()

    def autocommit(self, *args, **kwargs):
         raise NotImplementedError()

    def binary_types(self, *args, **kwargs):
         raise NotImplementedError()

    def cancel(self, *args, **kwargs):
         raise NotImplementedError()


    def closed(self, *args, **kwargs):
         raise NotImplementedError()

    def cursor_factory(self, *args, **kwargs):
         raise NotImplementedError()

    def deferrable(self, *args, **kwargs):
         raise NotImplementedError()

    def dsn(self, *args, **kwargs):
         raise NotImplementedError()

    def encoding(self, *args, **kwargs):
         raise NotImplementedError()

    def fileno(self, *args, **kwargs):
         raise NotImplementedError()

    def get_backend_pid(self, *args, **kwargs):
         raise NotImplementedError()

    def get_dsn_parameters(self, *args, **kwargs):
         raise NotImplementedError()

    def get_native_connection(self, *args, **kwargs):
         raise NotImplementedError()

    def get_parameter_status(self, *args, **kwargs):
         raise NotImplementedError()

    def get_transaction_status(self, *args, **kwargs):
         raise NotImplementedError()

    def info(self, *args, **kwargs):
         raise NotImplementedError()

    def isexecuting(self, *args, **kwargs):
         raise NotImplementedError()

    def isolation_level(self, *args, **kwargs):
         raise NotImplementedError()

    def lobject(self, *args, **kwargs):
         raise NotImplementedError()

    def notices(self, *args, **kwargs):
         raise NotImplementedError()

    def notifies(self, *args, **kwargs):
         raise NotImplementedError()

    def pgconn_ptr(self, *args, **kwargs):
         raise NotImplementedError()

    def poll(self, *args, **kwargs):
         raise NotImplementedError()

    def protocol_version(self, *args, **kwargs):
         raise NotImplementedError()

    def readonly(self, *args, **kwargs):
         raise NotImplementedError()

    def reset(self, *args, **kwargs):
         raise NotImplementedError()

    def rollback(self, *args, **kwargs):
         raise NotImplementedError()

    def server_version(self, *args, **kwargs):
         raise NotImplementedError()

    def set_client_encoding(self, *args, **kwargs):
         raise NotImplementedError()

    def set_isolation_level(self, *args, **kwargs):
         raise NotImplementedError()

    def set_session(self, *args, **kwargs):
         raise NotImplementedError()

    def status(self, *args, **kwargs):
         raise NotImplementedError()

    def string_types(self, *args, **kwargs):
         raise NotImplementedError()

    def tpc_begin(self, *args, **kwargs):
         raise NotImplementedError()

    def tpc_commit(self, *args, **kwargs):
         raise NotImplementedError()

    def tpc_prepare(self, *args, **kwargs):
         raise NotImplementedError()

    def tpc_recover(self, *args, **kwargs):
         raise NotImplementedError()

    def tpc_rollback(self, *args, **kwargs):
         raise NotImplementedError()

    def xid(self, *args, **kwargs):
         raise NotImplementedError()

