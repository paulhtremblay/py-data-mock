import os
import datetime
import argparse
import subprocess
import tempfile
import sqlite3
import re

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

class LineInfo2:

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
        self.insert_delete = False
        self.num_inserts = None
        self.num_deletes = None
        self.parse_s(s)

    def get_name(self, s):
        s = s[7:]
        pattern = re.compile(r'(.*?)<(.*?)>')
        search_obj = pattern.search(s)
        if search_obj:
            self.name = search_obj.group(1).strip()
            self.email = search_obj.group(2)
            fields = self.name.split()
            if len(fields) == 2:
                self.first_name = fields[0].strip()
                self.last_name = fields[1].strip()
            else:
                self.first_name = None
                self.last_name = None
        else:
            self.name = None
            self.email = None
            self.first_name = None
            self.last_name = None

    def parse_s(self, s):
        if s[0:6] == 'commit':
            self.commit = True
        elif self.state == 'commit' and s[0:7] != 'Author:':
            self.unknown = True
        elif s[0:7] == 'Author:':
            self.author = s[8:]
            self.get_name(s)
        elif s[0:5] == 'Date:':
            self.date = datetime.datetime.strptime(s[5:].strip(), '%Y-%m-%d %H:%M:%S')
        elif s.strip() == '':
            self.empty_line = True
        elif '1 file changed' in s:
            self.insert_delete = True
            self.num_inserts, self.num_deletes = self.get_insertions_deletions(s)
            self.state = 'insert_delete_line'
        elif '|'  in s and (self.state == 'commit_comment' or self.state == 'body'):
            #this is summary line
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

    def _get_reg_exp(self, pattern, string):
        result  = pattern.search(string)
        if result != None:
            return int(result.group(1))
        return 0

    def get_insertions_deletions(self, s):
        pattern_insert = re.compile('(\d+) insertions')
        pattern_delete = re.compile('(\d+) deletions')
        insertions = self._get_reg_exp(pattern_insert, s)
        deletions = self._get_reg_exp(pattern_delete, s)
        return insertions, deletions




def get_line_info_state2(s, state):
    li=  LineInfo2(s = s, state = state)
    if li.commit:
        state = 'commit'
    elif state == 'commit' and li.unknown:
        state = 'unknown'
    elif li.author:
        state = 'author'
    elif li.date:
        state = 'date'
    elif li.insert_delete:
        state = 'insert_delete'
    elif state == 'date' and not li.empty_line:
        state = 'commit_comment'
    elif state == 'commit_comment' and li.body_line:
        state = 'body'
    return li, state


def handle_line2(dict_,line_info, state):
    if state == 'commit':
        pass
    elif line_info.author:
        dict_['author'] = line_info.author
        dict_['email'] = line_info.email
        dict_['name'] = line_info.name
        dict_['first_name'] = line_info.first_name
        dict_['last_name'] = line_info.last_name
    elif line_info.date:
        dict_['date'] = line_info.date
    elif line_info.insert_delete:
        dict_['num_insertions'] = line_info.num_inserts
        dict_['num_deletes'] = line_info.num_deletes

def parse_file_log2(s):
    dict_ = {}
    lines = s.split('\n')
    state = None
    for i in lines:
        line_info, state = get_line_info_state2(s = i, state = state)
        handle_line2(dict_,line_info, state)
    return dict_




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

def get_log_info_file2(git_o, path):
    info = git_o.log('--stat',  "--date=format:%Y-%m-%d %H:%M:%S",  path)
    return info

def _get_rel_path(path, target_dir):
    last = os.path.split(target_dir)[1]
    ind = path.find(last)
    return path[27:]

def db_init(db_path, table_name, verbosity = 0):
    if os.path.isfile(db_path):
        os.remove(db_path)
        if verbosity > 0:
            print(f'removed {db_path}')
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    sql = f"""
create table if not exists {table_name}
(author text not null,
name text,
first_name text,
last_name text,
email text,
	date datetime not null,
	path text not null,
	extension text,
	lines_added int,
    lines_deleted int
    )
    """
    cur.execute(sql)
    if verbosity > 0:
        print(f'created table {table_name}')

def init(dirs, db_path, table_name, verbosity = 0):
    db_init(db_path = db_path, table_name = table_name,
            verbosity = verbosity)
    fh, temp_path  = tempfile.mkstemp()
    with open(temp_path, 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        for dir_ in dirs:
            o = git.Git(dir_)
            for root, dirs, files in os.walk(dir_):
                for file in files:
                    f = os.path.join(root, file)
                    if verbosity > 2:
                        print(f'working on {f}')
                    log_string = get_log_info_file2(git_o = o, path = f)
                    if verbosity > 3:
                        print(log_string)
                    info = parse_file_log2(log_string)
                    if not info.get('author'):
                        continue
                    rel_path = _get_rel_path(path = f, target_dir = dir_)
                    row = [info.get('author'), info.get('name'), info.get('first_name'),
                           info.get('last_name'), info.get('email'), info['date'].strftime('%Y-%m-%d %H:%M:%S'),
                           rel_path, os.path.splitext(f)[1], info['num_insertions'] , info['num_deletes']
                            ]
                    csv_writer.writerow(row)
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

if __name__ == '__main__':
    args = _get_args()
    if args.action == 'init':
        init(dirs = args.dirs, verbosity = args.verbosity,
             db_path = args.db_path,
             table_name = args.table_name)
    else:
        raise NotImplementedError()

