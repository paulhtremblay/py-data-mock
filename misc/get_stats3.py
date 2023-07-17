import os
import datetime
import argparse
import subprocess

import csv

from git import Repo
import git

import pprint

pp = pprint.PrettyPrinter(indent = 4)

class BadStats(Exception):
    pass

def _get_args():
    parser = argparse.ArgumentParser(description = 'get git status')
    parser.add_argument('--dirs', '-d', nargs="+", required = True)
    parser.add_argument('--verbosity', '-v', type = int, default = 0)
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
            self.file_info = True
        elif s[0] == '+':
            self.added_line = True
        elif s[0:2] == '--':
            self.null = True
        elif s[0] == '-':
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

def get_log_info_file(git_o):
    info = git_o.log('--stat', "--date=format:%Y-%m-%d %H:%M:%S")
    return info

def to_csv(l, file_path):
    with open('temp.csv', 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        for dict_ in l:
            if not dict_.get('author'):
                continue
            author = dict_['author']
            date = dict_['date'].strftime('%Y-%m-%d %H:%M:%S')
            for path in dict_['files'].keys():
                row = [author, date, path, dict_['files'][path]['ext'], 
                       dict_['files'][path]['lines_added'] + dict_['files'][path]['lines_subtracted'] + dict_['files'][path]['lines_added_and_subtracted']]
                csv_writer.writerow(row)

def to_sqlite(db_name, csv_path, table_name ):
    #initial dump
    #C:\sqlite3.exe DBNAME.db ".read DBSCRIPT.sql"
    #git log --author="_Your_Name_Here_" --pretty=tformat: --numstat | awk '{ add += $1; subs += $2; loc += $1 - $2 } END { printf "added lines: %s, removed lines: %s, total lines: %s\n", add, subs, loc }' -

    args = ['sqlite3', db_name, '-cmd', 
                '.mode csv',
            f'.import {csv_path} {table_name}'
            ]
    result = subprocess.run(args,
                            capture_output=True)
    if result.returncode != 0:
        print(result.stderr)
        print(result.stdout)

def get_stats(dirs, verbosity = 0):
    csv_path = 'temp.csv'
    for dir_ in dirs:
        o = git.Git(dir_)
        log_string = get_log_info_file(git_o = o)
        l = parse_file_log(log_string)
    to_csv(l, file_path = csv_path)
    to_sqlite(
        db_name = 'git_change.db',
        csv_path = csv_path,
        table_name = 'git',
        )

if __name__ == '__main__':
    args = _get_args()
    get_stats(dirs = args.dirs, verbosity = args.verbosity)

