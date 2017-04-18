# coding:utf-8
import re
import os
import fnmatch
import gzip, bz2


def gen_find(filepat, top):
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)


def gen_open(filenames):
    for name in filenames:
        if name.endswith('.gz'):
            yield gzip.open(name)
        elif name.endswith('.bz2'):
            yield bz2.BZ2File(name)
        else:
            yield open(name)


def gen_cat(sources):
    for s in sources:
        for line in s:
            yield line


def gen_grep(pat, lines):
    patc = re.compile(pat)
    for line in lines:
        if patc.search(line):
            yield line


def gen_bytestr(lines):
    pattern = re.compile(r'.*?HTTP/1.1"200 (\d+?) .*?', re.S)
    for line in lines:
        m = re.search(pattern, line)
        if m:
            bytestr = m.group(1)
            yield int(bytestr)


def field_map(dictseq, name, func):
    for d in dictseq:
        d[name] = func(d[name])
        yield d


def nginx_log(lines):
    logpats = r'(\S+) - (\S+) - - \[(\S+) \+0800\] \[\S+\] "(\S+) (\S+) (\S+)"(\S+) (\S+) "(\S+)" "(.*?)" ".*?"'
    patc = re.compile(logpats)
    colnames = ('host', 'user', 'datetime', 'method', 'request', 'proto', 'status', 'bytes', 'referrer', 'agent')

    groups = (patc.match(line) for line in lines)
    tuples = (g.groups() for g in groups if g)

    log = (dict(zip(colnames, t)) for t in tuples)
    log = field_map(log, 'status', int)
    log = field_map(log, 'bytes', lambda s: int(s) if s != '-' else 0)

    return log


def lines_from_dir(filepat, dirname):
    names = gen_find(filepat, dirname)
    files = gen_open(names)
    lines = gen_cat(files)
    return lines


if __name__ == '__main__':
    lines = lines_from_dir('3d.access.log*', 'nginx')
    log = nginx_log(lines)
    # pattern = r'.*?HTTP/1.1"200 (\d+?) .*?'
    # log_names = gen_find("3d.access.log*", 'nginx')
    # log_files = gen_open(log_names)
    # log_lines = gen_cat(log_files)
    # patlines = gen_grep(pattern, log_lines)
    # bytecolumn = gen_bytestr(patlines)
    # print('Total: {}'.format(sum(bytecolumn)))
