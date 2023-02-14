# https://stackoverflow.com/questions/33046733/force-requests-to-use-ipv4-ipv6

import socket
import requests.packages.urllib3.util.connection as urllib3_cn


def allowed_gai_family():
    return socket.AF_INET6


urllib3_cn.allowed_gai_family = allowed_gai_family
