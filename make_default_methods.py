import argparse

def _get_args():
    parser = argparse.ArgumentParser(description = 'make default methods')
    parser.add_argument('path')
    return  parser.parse_args()

def make_method(name):
    s = ''
    s += f'def {name}(self, *args, **kwargs):\n'
    s += '     raise NotImplementedError()\n\n'
    return s

def make_default_methods(path):
    with open(path, 'r') as read_obj, open('temp_method.py', 'w') as write_obj:
        line = True
        while line:
            line = read_obj.readline()
            if len(line.strip()) == 0:
                continue
            new_func = make_method(line.strip())
            write_obj.write(new_func)

if __name__ == '__main__':
    args = _get_args()
    make_default_methods(args.path)
