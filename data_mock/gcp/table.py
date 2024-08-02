class RowIterator:

    def __init__(self, data, m):
        if data == None:
            def none_generator():
                return
                yield
            self.__data = none_generator()
            self.total_rows = 0
        else:
            def my_generator():
                for i in data:
                    yield i
            self.__data = my_generator()
            self.total_rows = m.get('total_rows')
            self.schema = m.get('schema')

    def __iter__(self):
        return self

    def __next__(self):
        v = next(self.__data)
        if not v:
            raise StopIteration
        else:
            return Row(row = v)

    def result(self):
        return self

class Row():

    def __init__(self, row):
        self.__info = {}
        l = []
        for i in row:
            self.__info[i[0]] = i[1]
            l.append(i[1])
            self.__dict__[i[0]] = i[1]
        self.__values = tuple(l)
        self.row = row

    def get(self, *args, **kwargs):
        if args:
            return self.__info.get(args[0])
        return self.__info.get(kwargs['key'])

    def items(self, *args, **kwargs):
        for i in self.row:
            yield i[0], i[1]

    def values(self, *args, **kwargs):
        return self.__values

    def keys(self, *args, **kwargs):
        return self.__info.keys()

class Table:
    pass

class TableReference:
    pass

class TableListItem:
    pass

