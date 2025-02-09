from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM, getaddrinfo, timeout, error
from portsDict import well_known_ports
from colorama import Fore, Style
import ipaddress
import re

def verifica_ip(ip):
    try:
        info = getaddrinfo(ip, None)
        ip = info[0][4][0]
        return ip
    except:
        return ip

def get_banner(sock):
    try:
        sock.settimeout(2)
        banner = sock.recv(1024).decode().strip()
        return banner
    except:
        return None

def detecta_os(banner):
    if not banner:
        return None

    patterns = {
        r"Linux": "Linux",
        r"Windows": "Windows",
        r"Ubuntu": "Ubuntu",
        r"Debian": "Debian",
        r"CentOS": "CentOS",
        r"FreeBSD": "FreeBSD",
        r"OpenBSD": "OpenBSD",
    }

    for pattern, os_name in patterns.items():
        if re.search(pattern, banner, re.IGNORECASE):
            return os_name

    return None

def escaneia_portas(ip, portas, protocolo):
    try:
        info = getaddrinfo(ip, None)
        ip = info[0][4][0]
        family = info[0][0]
        resultado = False

        for porta in portas:
            if protocolo == "TCP":
                s = socket(family, SOCK_STREAM)
            elif protocolo == "UDP":
                s = socket(family, SOCK_DGRAM)

            s.settimeout(0.5)
            try:
                if protocolo == "TCP":
                    if s.connect_ex((ip, porta)) == 0:
                        banner = get_banner(s)
                        os_name = detecta_os(banner)
                        if str(porta) in well_known_ports:
                            print(f"{Fore.GREEN}{ip}: Porta {porta} aberta ({well_known_ports[str(porta)]}){Style.RESET_ALL}")
                        else:
                            print(f"{Fore.GREEN}{ip}: Porta {porta} aberta{Style.RESET_ALL}")
                        if os_name:
                            print(f"{Fore.BLUE}Possível sistema operacional: {os_name}{Style.RESET_ALL}")
                        resultado = True
                elif protocolo == "UDP":
                    s.sendto(b'', (ip, porta))
                    data, addr = s.recvfrom(1024)
                    if str(porta) in well_known_ports:
                        print(f"{Fore.GREEN}{ip}: Porta {porta} aberta ({well_known_ports[str(porta)]}){Style.RESET_ALL}")
                    else:
                        print(f"{Fore.GREEN}{ip}: Porta {porta} aberta{Style.RESET_ALL}")
                    resultado = True
            except timeout:
                print(f"{Fore.YELLOW}{ip}: Porta {porta} filtrada{Style.RESET_ALL}")
            except error:
                if protocolo == "UDP":
                    print(f"{Fore.RED}{ip}: Porta {porta} fechada{Style.RESET_ALL}")
            finally:
                s.close()

        if not resultado:
            print(f"{Fore.RED}{ip}: Nenhuma porta especificada está aberta :({Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}{ip}: Erro: {e}{Style.RESET_ALL}")

def main():
    ip_or_cidr = input("Digite o IP/Hostname ou rede (CIDR): ")
    port_range = input("Digite o range de portas (XXXX ou XXXX-XXXX): ")
    protocolo = input("Digite o protocolo (TCP ou UDP): ").upper()

    if not ip_or_cidr or not port_range or protocolo not in ["TCP", "UDP"]:
        print("Por favor, insira IP/Hostname/CIDR, range de portas e protocolo válidos.")
        return

    if "-" in port_range:
        start, end = map(int, port_range.split("-"))
        portas = range(start, end + 1)
    else:
        portas = [int(port_range)]

    if "/" in ip_or_cidr:
        network = ipaddress.ip_network(ip_or_cidr, strict=False)
        ips = [str(ip) for ip in network.hosts()]
    else:
        ips = [ip_or_cidr]

    for ip in ips:
        print(f"{Fore.CYAN}Escaneando IP: {ip}{Style.RESET_ALL}")
        escaneia_portas(verifica_ip(ip), portas, protocolo)

if __name__ == "__main__":
    main()