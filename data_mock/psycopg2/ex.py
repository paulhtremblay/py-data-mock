import sqlparse
import re
sql_example = """--comment
/*
comment 2
*/
SELEct * from test;
INSERT INTO test VALUES ('
-- test
a
WHERE name = %s
');
 """

def find_vars_pattern(s):
    pattern = re.compile('(\s*|=)(%s)($|\n|\s)')
    r = pattern.findall(s)
    return len(r)


def find_vars(sql):
    no_com = sqlparse.format(sql_example, strip_comments=True, keyword_case = 'upper').strip()

find_vars(sql = sql_example)

examples = ['x', ' %sx', "'%s", ' %s\n', 'where name = %s and %s ',
            'where name =%s']
for i in examples:
    l = find_vars_pattern(i)
    print(f'for "{i}" length is {l}')
