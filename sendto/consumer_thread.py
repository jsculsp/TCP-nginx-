import queue
import threading
from broadcast import broadcast


class ConsumerThread(threading.Thread):

    def __init__(self, target):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.in_queue = queue.Queue()
        self.target = target

    def send(self, item):
        self.in_queue.put(item)

    def generate(self):
        while True:
            item = self.in_queue.get()
            yield item

    def run(self):
        self.target(self.generate())


if __name__ == '__main__':
    from python_tail_f import follow
    from nginx_log import nginx_log

    def find_404(log):
        for r in (r for r in log if r['status'] == 404):
            print('[{}] [{}] {}'.format(r['status'], r['datetime'], r['request']))

    def bytes_transferred(log):
        total = 0
        for r in log:
            total += r['bytes']
            print('Total bytes: {}'.format(total))

    c1 = ConsumerThread(find_404)
    c1.start()
    c2 = ConsumerThread(bytes_transferred)
    c2.start()

    lines = follow('/var/log/nginx/3d.access.log')
    log = nginx_log(lines)
    broadcast(log, [c1, c2])
