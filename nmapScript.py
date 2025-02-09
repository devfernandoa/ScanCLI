import subprocess
from portsDict import well_known_ports
from colorama import Fore, Style

target = input("Digite o IP/Hostname ou rede (CIDR): ")
portas = input("Digite o range de portas (XXXX ou XXXX-XXXX): ")

def escaneia_ip(target, portas):
    if "-" in portas:
        portas = portas
    else:
        portas = f"{portas}-{portas}"
    
    comando = ["nmap", "-Pn", "-p", portas, target]
    resultado = subprocess.run(comando, capture_output=True, text=True)
    
    if resultado.returncode != 0:
        print(Fore.RED, "Erro ao executar o nmap")
        return
    
    saida = resultado.stdout.splitlines()
    for linha in saida:
        if "/" not in target:
            if "/tcp" in linha and "open" in linha:
                partes = linha.split()
                porta = partes[0].split("/")[0]
                servico = partes[2]
                print(Fore.GREEN + f"A porta {porta} (TCP) está aberta com o serviço {servico}" + Style.RESET_ALL)
            elif "/udp" in linha and "open" in linha:
                partes = linha.split()
                porta = partes[0].split("/")[0]
                servico = partes[2]
                print(Fore.GREEN + f"A porta {porta} (UDP) está aberta com o serviço {servico}" + Style.RESET_ALL)
            elif "/tcp" in linha and "filtered" in linha:
                partes = linha.split()
                porta = partes[0].split("/")[0]
                print(Fore.YELLOW + f"A porta {porta} (TCP) está filtrada" + Style.RESET_ALL)
            elif "/udp" in linha and "filtered" in linha:
                partes = linha.split()
                porta = partes[0].split("/")[0]
                print(Fore.YELLOW + f"A porta {porta} (UDP) está filtrada" + Style.RESET_ALL)
        else:  
            if "Nmap scan report for" in linha:
                ip = linha.split()[-1]

            if "/tcp" in linha and "open" in linha:
                partes = linha.split()
                porta = partes[0].split("/")[0]
                servico = partes[2]
                print(Fore.GREEN + f"O IP {ip} tem a porta {porta} (TCP) aberta com o serviço {servico}" + Style.RESET_ALL)
            elif "/udp" in linha and "open" in linha:
                partes = linha.split()
                porta = partes[0].split("/")[0]
                servico = partes[2]
                print(Fore.GREEN + f"O IP {ip} tem a porta {porta} (UDP) aberta com o serviço {servico}" + Style.RESET_ALL)
            elif "/tcp" in linha and "filtered" in linha:
                partes = linha.split()
                porta = partes[0].split("/")[0]
                print(Fore.YELLOW + f"O IP {ip} tem a porta {porta} (TCP) filtrada" + Style.RESET_ALL)
            elif "/udp" in linha and "filtered" in linha:
                partes = linha.split()
                porta = partes[0].split("/")[0]
                print(Fore.YELLOW + f"O IP {ip} tem a porta {porta} (UDP) filtrada" + Style.RESET_ALL)

escaneia_ip(target, portas)