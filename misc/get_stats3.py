import os
import datetime
import argparse
import subprocess
import tempfile
import sqlite3

import csv

from git import Repo
import git

import pprint

pp = pprint.PrettyPrinter(indent = 4)

class BadStats(Exception):
    pass

def my_date(s):
    date = datetime.datetime.strptime(s, '%Y-%m-%d').date()
    return date

def _get_args_old():
    parser = argparse.ArgumentParser(description = 'get git status')
    parser.add_argument('--dirs', '-d', nargs="+", required = True)
    parser.add_argument('--verbosity', '-v', type = int, default = 0)
    args = parser.parse_args()
    return args

def _get_args():
    parser = argparse.ArgumentParser(description = 'get git status')
    subparsers = parser.add_subparsers(dest='action', required = True)
    summary = subparsers.add_parser('summary', help='summary')
    init = subparsers.add_parser('init', help='stats')
    add = subparsers.add_parser('add', help='stats')
    add.add_argument('--start-date', '-s', required=True, 
            type = my_date, help = 'date for start')
    add.add_argument('--end-date', '-e', required=True, 
            type = my_date, help = 'date for end')
    summary.add_argument('--target-dir', '-t', required=False, 
            type = str, help = 'dir for git')
    init.add_argument('--dirs', '-d', nargs="+", required = True)
    add.add_argument('--dirs', '-d', nargs="+", required = True)
    add.add_argument('--verbosity', '-v', type = int, default = 0)
    init.add_argument('--verbosity', '-v', type = int, default = 0)
    init.add_argument('--db_path', '-dp', type = str, default = 'git_change.db')
    init.add_argument('--table_name', '-tn', type = str, default = 'git')
    add.add_argument('--db_path', '-dp', type = str, default = 'git_change.db')
    add.add_argument('--table_name', '-tn', type = str, default = 'git')
    args = parser.parse_args()
    return args

class LineInfo:


    def __init__(self, s, state):
        self.commit = False
        self.author = False
        self.date = False
        self.empty_line = False
        self.string = s
        self.unknown = False
        self.file_info = None
        self.null = None
        self.body_line = False
        self.state = state
        self.file_name = None
        self.file_ext = None
        self.parse_s(s)

    def parse_s(self, s):
        if s[0:6] == 'commit':
            self.commit = True
        elif self.state == 'commit' and s[0:7] != 'Author:':
            self.unknown = True
        elif s[0:7] == 'Author:':
            self.author = s[8:]
        elif s[0:5] == 'Date:':
            self.date = datetime.datetime.strptime(s[5:].strip(), '%Y-%m-%d %H:%M:%S')
        elif s.strip() == '':
            self.empty_line = True
        elif s[0:2] == '++':
            assert False
            self.file_info = True
        elif s[0] == '+':
            assert False
            self.added_line = True
        elif s[0:2] == '--':
            assert False
            self.null = True
        elif s[0] == '-':
            assert False
            self.subtracted_line = True
        elif '|'  in s and (self.state == 'commit_comment' or self.state == 'body'):
            self.body_line = True
            fields = s.split('|')
            fields2 = fields[1].split()
            self.file_name = fields[0].strip()
            self.file_ext = os.path.splitext(fields[0])[1].strip()
            if len(fields2) == 2:
                n = int(fields2[0])
                if '-' in fields[1] and '+' in fields[1]:
                    self.line_added_and_subtracted = n
                elif '-' in fields2[1]:
                    self.line_subtracted = n
                elif '+' in fields2[1]:
                    self.line_added = n
                else:
                    assert False
        else:
            fields = s.split()
            self.unknown = True
            

def get_line_info(s):
    return  LineInfo(s = s)

def get_line_info_state(s, state):
    li=  LineInfo(s = s, state = state)
    if li.commit:
        state = 'commit'
    elif state == 'commit' and li.unknown:
        state = 'unknown'
    elif li.author:
        state = 'author'
    elif li.date:
        state = 'date'
    elif state == 'date' and not li.empty_line:
        state = 'commit_comment'
    elif state == 'commit_comment' and li.body_line:
        state = 'body'
    return li, state

def handle_line(list_, line_info, state):
    if state == 'commit':
        list_.append({'files':{}})
    elif line_info.author:
        list_[-1]['author'] = line_info.author
    elif line_info.date:
        list_[-1]['date'] = line_info.date
    elif line_info.body_line:
        file_dict = list_[-1].get('files')
        if not file_dict.get(line_info):
            file_dict[line_info.file_name] = {'ext': line_info.file_ext,'lines_added':0, 'lines_subtracted': 0, 'lines_added_and_subtracted': 0}
        if hasattr(line_info, 'line_added'):
            file_dict[line_info.file_name]['lines_added'] = line_info.line_added
        if hasattr(line_info, 'line_subtracted'):
            file_dict[line_info.file_name]['lines_subtracted'] = line_info.line_subtracted
        if hasattr(line_info, 'line_added_and_subtracted'):
            file_dict[line_info.file_name]['lines_added_and_subtracted'] = line_info.line_added_and_subtracted

def parse_file_log(s):
    list_ = []
    lines = s.split('\n')
    state = None
    for i in lines:
        line_info, state = get_line_info_state(s = i, state = state)
        handle_line(list_, line_info, state)
    
    return list_

def get_log_info_file_append(git_o, start_date, end_date):
    info = git_o.log('--stat', "--date=format:%Y-%m-%d %H:%M:%S", 
                '--since={start_date}'.format(start_date = start_date.strftime('%Y-%m-%d')),
        '--until={end_date}'.format(end_date = end_date.strftime('%Y-%m-%d')),
                     )
    return info

def get_log_info_file(git_o):
    info = git_o.log('--stat', "--date=format:%Y-%m-%d %H:%M:%S")
    return info

def to_csv(l, file_path, verbosity = 0):
    counter = 0
    with open(file_path, 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        for dict_ in l:
            if not dict_.get('author'):
                continue
            author = dict_['author']
            date = dict_['date'].strftime('%Y-%m-%d %H:%M:%S')
            for path in dict_['files'].keys():
                counter += 1
                row = [author, date, path, dict_['files'][path]['ext'], 
                       dict_['files'][path]['lines_added'] + dict_['files'][path]['lines_subtracted'] + dict_['files'][path]['lines_added_and_subtracted']]
                csv_writer.writerow(row)
    if verbosity > 1:
        print(f'wrote {counter} lines to csv {file_path}')


def _print_args(args):
    print(f"executing {' '.join(args)}")

def to_sqlite(db_path, csv_path, table_name, verbosity = 0):
    #git log --author="_Your_Name_Here_" --pretty=tformat: --numstat | awk '{ add += $1; subs += $2; loc += $1 - $2 } END { printf "added lines: %s, removed lines: %s, total lines: %s\n", add, subs, loc }' -

    args = ['sqlite3', db_path, '-cmd', 
                '.mode csv',
            f'.import {csv_path} {table_name}'
            ]
    result = subprocess.run(args,
                            capture_output=True)
    if verbosity > 2:
        _print_args(args)
    if result.returncode != 0:
        print(result.stderr)
        print(result.stdout)

def init(dirs, db_path, table_name, verbosity = 0):
    if os.path.isfile(db_path):
        os.remove(db_path)
        if verbosity > 0:
            print(f'removed {db_path}')
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    sql = f"""
create table if not exists {table_name}
(name text not null,
	date datetime not null,
	path text not null,
	extention text,
	lines_changed int
    )
    """
    cur.execute(sql)
    if verbosity > 0:
        print(f'created table {table_name}')
    fh, temp_path = tempfile.mkstemp()
    list_ = []
    for dir_ in dirs:
        if verbosity > 0:
            print(f'working on {dir_}')
        o = git.Git(dir_)
        log_string = get_log_info_file(git_o = o)
        l = parse_file_log(log_string)
        list_.extend(l)
    if verbosity > 2:
        print(f'list hasfiles has {len(list_)} dicts')
    to_csv(list_, file_path = temp_path, verbosity = verbosity)
    to_sqlite(
        db_path = db_path,
        csv_path = temp_path,
        table_name = table_name,
        verbosity = verbosity
        )
    if verbosity > 0:
        print(f'wrote lines to {db_path}.{table_name}')
    os.close(fh)
    os.remove(temp_path)

def flatte_list(l, verbosity = 0):
    final = []
    counter = 0
    for dict_ in l:
        if not dict_.get('author'):
            continue
        author = dict_['author']
        date = dict_['date'].strftime('%Y-%m-%d %H:%M:%S')
        for path in dict_['files'].keys():
            counter += 1
            row = [author, date, path, dict_['files'][path]['ext'], 
                   dict_['files'][path]['lines_added'] + dict_['files'][path]['lines_subtracted'] + dict_['files'][path]['lines_added_and_subtracted']]
            final.append(row)
    if verbosity > 1:
        print(f'wrote {counter} lines ')
    return final

def make_delete_string(table_name, start_date, end_date):
    s = f'DELETE FROM {table_name} WHERE date BETWEEN {start_date} AND {end_date};\n'
    return s

def make_insert_from_list(l, table_name, start_date, end_date):
    s = f'INSERT INTO {table_name} VALUES\n'
    temp_l = []
    for i in l:
        temp_l.append(f"('{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}', {i[4]})")
    s += ',\n'.join(temp_l)
    return s

def add(dirs, start_date, end_date, table_name , db_path,  verbosity = 0):
    list_ = []
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    for dir_ in dirs:
        if verbosity > 0:
            print(f'working on {dir_}')
        o = git.Git(dir_)
        log_string = get_log_info_file_append(git_o = o,
                                              start_date = start_date,
                                              end_date = end_date)
        if verbosity > 3:
            print(f'log is {log_string}')
        l = parse_file_log(log_string)
        list_.extend(l)
    if verbosity > 2:
        print(f'list has {len(list_)} dicts')
    full_l = flatte_list(l = list_, verbosity = verbosity)
    insert_s = make_insert_from_list(full_l, table_name = table_name, 
                                     start_date = start_date,
                                     end_date = end_date)
    delete_string = make_delete_string(table_name = table_name,
                                       start_date = start_date,
                                       end_date = end_date)
    if verbosity > 3:
        print('delete string is {delete_string}')
    cur.execute(delete_string)
    if verbosity > 3:
        print(f'insert string is {insert_s})')
    cur.execute(insert_s)


if __name__ == '__main__':
    args = _get_args()
    if args.action == 'init':
        init(dirs = args.dirs, verbosity = args.verbosity,
             db_path = args.db_path,
             table_name = args.table_name)
    else:
        add(dirs = args.dirs, verbosity = args.verbosity,
            start_date = args.start_date,
            end_date = args.end_date,
            db_path = args.db_path,
            table_name = args.table_name
            )

