from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM, getaddrinfo, timeout, error
from colorama import Fore, Style
import ipaddress
import re
import threading
import sys
import os

# Importar dicionário de portas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from portsDict import well_known_ports
except ImportError:
    well_known_ports = {}  # Fallback caso não consiga importar o dicionário

def get_banner(sock):
    """Tenta obter um banner da conexão."""
    try:
        sock.settimeout(2)
        banner = sock.recv(1024).decode().strip()
        return banner
    except:
        return None

def detect_os_from_banner(banner):
    """Tenta detectar o sistema operacional a partir do banner."""
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

def scan_ports(ip, portas, protocol):
    """Escaneia portas para um endereço IP específico."""
    try:
        # Verificar se as portas são inteiras
        portas = [int(p) for p in portas]
        
        info = getaddrinfo(ip, None)
        ip = info[0][4][0]
        family = info[0][0]
        resultado = False

        for porta in portas:
            if protocol == "TCP":
                s = socket(family, SOCK_STREAM)
            elif protocol == "UDP":
                s = socket(family, SOCK_DGRAM)

            s.settimeout(0.5)
            try:
                if protocol == "TCP":
                    if s.connect_ex((ip, porta)) == 0:
                        banner = get_banner(s)
                        os_info = detect_os_from_banner(banner)
                        os_text = f" (Sistema provável: {os_info})" if os_info else ""
                        banner_text = f" [Banner: {banner}]" if banner else ""
                        
                        port_service = well_known_ports.get(str(porta), "desconhecido")
                        print(f"{Fore.GREEN}{ip}: Porta {porta} aberta ({port_service}){os_text}{banner_text}{Style.RESET_ALL}")
                        resultado = True
                elif protocol == "UDP":
                    s.sendto(b'', (ip, porta))
                    try:
                        data, addr = s.recvfrom(1024)
                        port_service = well_known_ports.get(str(porta), "desconhecido")
                        print(f"{Fore.GREEN}{ip}: Porta {porta} aberta ({port_service}){Style.RESET_ALL}")
                        resultado = True
                    except timeout:
                        print(f"{Fore.YELLOW}{ip}: Porta {porta} filtrada{Style.RESET_ALL}")
            except timeout:
                if protocol == "TCP":
                    print(f"{Fore.YELLOW}{ip}: Porta {porta} filtrada{Style.RESET_ALL}")
            except error:
                if protocol == "UDP":
                    print(f"{Fore.RED}{ip}: Porta {porta} fechada{Style.RESET_ALL}")
            finally:
                s.close()

        if not resultado:
            print(f"{Fore.RED}{ip}: Nenhuma porta especificada está aberta :({Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}{ip}: Erro: {e}{Style.RESET_ALL}")

def scan_network(ip_or_cidr, portas, protocol):
    """Escaneia uma rede usando notação CIDR ou um único IP."""
    try:
        if "/" in ip_or_cidr:
            network = ipaddress.ip_network(ip_or_cidr, strict=False)
            ips = [str(ip) for ip in network.hosts()]
        else:
            ips = [ip_or_cidr]

        threads = []
        for ip in ips:
            print(f"{Fore.CYAN}Escaneando IP: {ip}{Style.RESET_ALL}")
            t = threading.Thread(target=scan_ports, args=(ip, portas, protocol))
            threads.append(t)
            t.start()
            
            # Limitar o número de threads paralelas para não sobrecarregar
            if len(threads) >= 10:
                for thread in threads:
                    thread.join()
                threads = []
        
        # Aguardar as threads restantes
        for thread in threads:
            thread.join()

    except Exception as e:
        print(f"{Fore.RED}Erro: {e}{Style.RESET_ALL}")