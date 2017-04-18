# coding:utf-8

import time
import codecs


def follow(filename):
    with codecs.open(filename, encoding='utf-8') as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if (not line) or (line == '\n') or (line == '\r\n'):
                time.sleep(0.1)
                continue
            yield line


def start():
    f = follow('access.log')
    while True:
        a = next(f)
        print(a)
        print('type: ', type(a))
