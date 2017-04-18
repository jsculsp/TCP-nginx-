class storelast(object):
    def __init__(self, source):
        self.source = source

    def __next__(self):
        item = next(self.source)
        self.last = item
        return item

    def __iter__(self):
        return self


# Example use
if __name__ == '__main__':
    from sendto.python_tail_f import follow
    from sendto.nginx_log import nginx_log

    lines = storelast(follow('access.log'))
    log = nginx_log(lines)

    for r in log:
        print(r)
        print(lines.last)
