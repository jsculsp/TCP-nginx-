import socket
from genpickle import gen_pickle, gen_unpickle


def sendto(source, addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    for pitem in gen_pickle(source):
        s.sendall(pitem)
    s.close()


if __name__ == '__main__':
    from nginx_log import nginx_log
    from python_tail_f import follow

    lines = follow('/var/log/nginx/3d.access.log')
    log = nginx_log(lines)
    sendto(log, ('192.168.4.248', 3333))
