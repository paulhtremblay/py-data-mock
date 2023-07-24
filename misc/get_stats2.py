import os
import datetime
import argparse

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

class State:

    def __init__(self, line_info):
        self.current_state = None
        if line_info.commit:
            self.commit = True
        else:
            self.commit = False
        self.body = False
        self.date = None
        self.author = None
        self.merge = False
        self.branch = None

class LineInfo:


    def __init__(self, s):
        self.commit = False
        self.author = False
        self.date = False
        self.empty_line = False
        self.string = s
        self.unknown = False
        self.added_line = False
        self.subtracted_line = False
        self.parse_s(s)
        self.file_info = None
        self.null = None

    def parse_s(self, s):
        if s[0:6] == 'commit':
            self.commit = True
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
        else:
            self.unknown = True
            
def _get_date(s):
    pass

def get_line_info(s):
    return  LineInfo(s = s)

def _is_merge(s):
    words = s.split()
    words = [x.strip() for x in words]
    if len(words) >= 2 and words[-2] == 'to':
        return True

def _handle_line(line_info, list_, state):
    if line_info.commit:
        if state.commit and state.merge:
            list_.pop()
        state = State(line_info = line_info)
        list_.append({})
        return state
    if state.commit  and line_info.author:
        list_[-1]['author'] = line_info.author
        state.author = line_info.author
    elif state.commit  and line_info.date:
        list_[-1]['date'] = line_info.date
        state.date = line_info.date
    elif state.body  and line_info.added_line:
        if not list_[-1].get('lines_added'):
            list_[-1]['lines_added'] = 0
        list_[-1]['lines_added'] += 1
    elif state.body  and line_info.subtracted_line:
        if not list_[-1].get('lines_subtracted'):
            list_[-1]['lines_subtracted'] = 0
        list_[-1]['lines_subtracted'] += 1
    elif state.date and not line_info.empty_line:
        if _is_merge(s = line_info.string):
            state.merge = True
        else:
            state.body = True
            if not state.branch:
                list_[-1]['branch'] = line_info.string.strip()
                state.branch = True
    
    return state

def parse_file_log(s):
    list_ = []
    lines = s.split('\n')
    state = False
    for i in lines:
        line_info = get_line_info(i)
        if state == False:
            state = State(line_info = line_info)
        state = _handle_line(line_info, list_, state)
    
    return list_


def get_log_info_file(git_o, path):
    info = git_o.log('-p', '--follow', "--date=format:%Y-%m-%d %H:%M:%S",  path)
    return info

def _group_by_author(d):
    final = {}
    for path in d.keys():
        author_dict = {}
        for dict_ in d[path]:
            author = dict_['author']
            if not author_dict.get(author):
                author_dict[author] = {'lines_added': 0, 'lines_subtracted': 0}
            author_dict[author]['lines_added'] += dict_.get('lines_added',0)
            author_dict[author]['lines_subtracted'] += dict_.get('lines_subtracted',0)
        final[path] = author_dict

    return final

def get_stats(dirs, verbosity = 0, group_by_author = False):
    d = {}
    for dir_ in dirs:
        o = git.Git(dir_)
        for root, dirs, files in os.walk(dir_):
            for file in files:
                f = os.path.join(root, file)
                if verbosity > 2:
                    print(f'working on {f}')
                info = get_log_info_file(git_o = o, path = f)
                l = parse_file_log(info)
                d[f] = l
    if group_by_author:
        return _group_by_author(d)
    return d


if __name__ == '__main__':
    args = _get_args()
    get_stats(dirs = args.dirs, verbosity = args.verbosity)

