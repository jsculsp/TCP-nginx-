def broadcast(source, consumers):
    for item in source:
        for c in consumers:
            c.send(item)


# Example
if __name__ == '__main__':

    class Consumer(object):
        def __init__(self, name):
            self.name = name

        def send(self, item):
            print("{} got {}".format(self, item))

        def __repr__(self):
            return self.name

    c1 = Consumer('consumer1')
    c2 = Consumer('consumer2')
    c3 = Consumer('consumer3')

    from python_tail_f import follow
    lines = follow(open("access-log"))
    broadcast(lines, [c1, c2, c3])
