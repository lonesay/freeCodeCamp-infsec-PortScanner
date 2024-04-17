import socket
from common_ports import ports_and_services


def port_scanner(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    r = s.connect_ex((host, port))
    s.close()
    if r:
        return False
    else:
        return True


def check_target(target):
    parts = target.split('.')
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for part in parts:
        for i in range(len(part)):
            if part[i] not in numbers:
                return False
    return True


def get_open_ports(target, port_range, verbose = False):
    t = check_target(target)

    try:
        if t:
            host = target
            hostname = socket.gethostbyaddr(host)[0]
        else:
            hostname = target.replace("www.", "")
            host = socket.gethostbyname(hostname)
    except:
        return "Error: Invalid IP address" if t else "Error: Invalid hostname"
    
    open_ports = []
    if verbose:
        if host == hostname:
            open_ports = f'Open ports for {host}\n'
        else:
            open_ports = f'Open ports for {hostname} ({host})\n'
        open_ports += 'PORT     SERVICE\n'
    
    flag = False
    for port in range((port_range[1] - port_range[0]) + 1):
        port += port_range[0]
        service = ports_and_services[port] if port in ports_and_services.keys() else ""
        if port_scanner(host, port):
            if verbose:
                if flag:
                    open_ports += "\n"
                else:
                    flag = True
                open_ports += f"{str(port).ljust(9)}{service}"
            else:
                open_ports.append(port)

    return(open_ports)

