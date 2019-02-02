import logging
import sys

import requests

API_URL = 'https://cdn.fht.im/'


def export2file(service, out, start=0, limit=100):
    req = requests.get("https://chis-cat.fht.im/api?q=%s&start=%d&limit=%d" % (service, start, limit))
    rtn_value = req.json()
    if not rtn_value['success']:
        logging.error("ERROR.")
    else:
        if (out != sys.stdout):
            f = open(out, 'wb')
        for host in rtn_value['results']:
            out.writelines("%s:%s\n" % (host['ip'], host['port']))


if __name__ == '__main__':
    export2file("redis", out=sys.stdout)
