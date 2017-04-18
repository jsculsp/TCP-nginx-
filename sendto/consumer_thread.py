import queue
import threading


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
