# consumer.py
#
# consumer decorator and co-routine example


def consumer(func):
    def start(*args, **kwargs):
        c = func(*args, **kwargs)
        next(c)
        return c
    return start


# Example
if __name__ == '__main__':

    @consumer
    def recv_count():
        while True:
            n = yield
            print('T-minus {}'.format(n))

    r = recv_count()
    for i in range(10):
        r.send(i)
