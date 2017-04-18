import socket
import pickle


class NetConsumer(object):
    def __init__(self, addr):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(addr)

    def send(self, item):
        pitem = pickle.dumps(item)
        self.s.sendall(pitem)

    def close(self):
        self.s.close()

# Example use. This requires you to run receivefrom.py first.

if __name__ == '__main__':
    from broadcast import broadcast
    from python_tail_f import follow
    from nginx_log import nginx_log

    # A class that sends 404 requests to another host
    class Stat404(NetConsumer):
        def send(self, item):
            if item['status'] == 404:
                super(Stat404, self).send(item)

    stat404 = Stat404(("192.168.4.248", 3333))
    lines = follow('/var/log/nginx/3d.access.log')
    log = nginx_log(lines)
    broadcast(log, [stat404])
