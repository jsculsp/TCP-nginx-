# gentrace.py
#
# Trace a generator by printing items received


def trace(source):
    for item in source:
        print(item)
        yield item

# Example use
if __name__ == '__main__':
    from sendto.nginx_log import nginx_log
    from sendto.python_tail_f import follow

    lines = follow('/var/log/nginx/3d.access.log')
    log = trace(nginx_log(lines))
    r404 = trace(r for r in log if r['status'] == 404)
