from typing import List

import psutil
from loguru import logger


def get_used_ports():
    used_ports = set()
    try:
        for conn in psutil.net_connections(kind="inet"):
            if not conn.laddr or not conn.laddr.port:
                continue
            if conn.status in (psutil.CONN_ESTABLISHED, psutil.CONN_LISTEN):
                used_ports.add(conn.laddr.port)
    except psutil.AccessDenied as e:
        logger.error("Access denied while checking used ports, please run with elevated privileges.")
    except Exception as e:
        logger.error(f"Error while checking used ports: {e}.")
    return sorted(used_ports)


def get_free_ports(port_num: int, start_port: int = 8000, end_port: int = 10000) -> List[int]:
    used_ports = get_used_ports()
    ports = []
    for port in range(start_port, end_port):
        if port not in used_ports:
            ports.append(port)
            if len(ports) == port_num:
                return ports
    raise RuntimeError("No free ports found.")


def get_free_port(start_port: int = 8000, end_port: int = 10000) -> int:
    return get_free_ports(1, start_port, end_port)[0]
