import os
import datetime
import argparse

from git import Repo
import git

import pprint
pp = pprint.PrettyPrinter(indent = 4)

import bar_graph_time
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot
"""
python examples/get_stats.py stats -e 2023-06-22 -s 2023-05-22 -em "email1" "email2" "email3" \
	-d /Users/repo1 /Users/repo2

Note: repo must be checked out to branch where activity took place
"""


class BadStats(Exception):
    pass

def my_date(s):
    date = datetime.datetime.strptime(s, '%Y-%m-%d').date()
    return date

def _get_args():
    parser = argparse.ArgumentParser(description = 'get git status')
    subparsers = parser.add_subparsers(dest='action', required = True)
    summary = subparsers.add_parser('summary', help='summary')
    stats = subparsers.add_parser('stats', help='stats')
    stats.add_argument('--start-date', '-s', required=True, 
            type = my_date, help = 'date for start')
    stats.add_argument('--end-date', '-e', required=True, 
            type = my_date, help = 'date for end')
    summary.add_argument('--start-date', '-s', required=True, 
            type = my_date, help = 'date for start')
    summary.add_argument('--end-date', '-e', required=True, 
            type = my_date, help = 'date for end')
    summary.add_argument('--author', '-a', required=True, 
            type = str, help = 'email')
    summary.add_argument('--target-dir', '-t', required=False, 
            type = str, help = 'dir for git')
    stats.add_argument('--emails', '-em', nargs="+", required = True)
    stats.add_argument('--dirs', '-d', nargs="+", required = True)
    args = parser.parse_args()
    return args

def _parse_string(s):
    lines = s.split('\n')
    added = 0
    removed = 0
    for line in lines:
        if not line.strip():
            continue
        fields = line.split('\t')
        if len(fields) != 3:
            raise BadStats('len of line is not 3??')
        if fields[0] == '-':
            continue
        try:
            added += int(fields[0])
        except ValueError:
            raise BadStats('not sure')
        removed += int(fields[1])
    return added, removed


def get_added_removed(date, author, the_dir):
    end_date = date + datetime.timedelta(days = 1)
    o = git.Git(the_dir)
    loginfo = o.log('--since={date}'.format(date = date.strftime('%Y-%m-%d')),
        '--until={end_date}'.format(end_date = end_date.strftime('%Y-%m-%d')),
        '--author={author}'.format(author = author),
        '--pretty=tformat:','--numstat')
    added, removed = _parse_string(loginfo)
    return added, removed


def get_stats_by_user_date(d):
    dates = []
    y_values ={}
    for key in sorted(d.keys()):
        dates.append(key)
        for email in d[key]:
            if not y_values.get(email):
                y_values[email] = []
            y_values[email].append(d[key][email]['added'])
    return dates, y_values

def make_graph(dates, y_values):
    dates = [datetime.datetime(x.year, x.month, x.day) for x in dates]
    height = 3000
    graphs = []
    for email in y_values.keys():
        p = p_bide=bar_graph_time.bar_with_time_series(dates =  dates,
                                            y = y_values[email],
                                            title = email,
                                                   height = height
                                            )
        graphs.append(p)
    grid = gridplot(graphs, width=500, height=500, ncols = 3)
    show(grid)


def get_git_stats(start_date, end_date, emails, projects):
    d = {}
    while True:
        if start_date > end_date:
            break
        if datetime.datetime.today().weekday() > 5: #weekend
            continue

        for author in emails:
            for project in projects:
                added, removed = get_added_removed(start_date, 
                                           author = author,
                                           the_dir = project
                        )
                if not d.get(start_date):
                    d[start_date] = {}
                if not d[start_date].get(author):
                    d[start_date][author] = {'added':0, 'removed':0}
                d[start_date][author]['removed'] += removed
                d[start_date][author]['added'] += added

        start_date += datetime.timedelta(days = 1)
    dates, y_values = get_stats_by_user_date(d)
    return dates, y_values

def summary(start_date, end_date, author, the_dir = None):
    if not the_dir:
        the_dir = cwd = os.getcwd()
    total_add = 0
    total_removed = 0
    while True:
        if start_date > end_date:
            break
        added, removed = get_added_removed(date = start_date, 
                                           author = author,
                                           the_dir = the_dir
        )
        total_add += added
        total_removed += removed
        start_date += datetime.timedelta(days = 1)
    print(total_add, total_removed)

def main(args):
    if args.action == 'summary':
        summary(start_date = args.start_date, 
                end_date = args.end_date,
                author = args.author,
                the_dir = args.target_dir
                )
    elif args.action == 'stats':
        dates, y_values = get_git_stats(
                start_date = args.start_date,
                end_date = args.end_date,
                emails = args.emails,
                projects = args.dirs
                )

        make_graph(dates = dates, y_values = y_values)

if __name__ == '__main__':
    args = _get_args()
    main(args)
