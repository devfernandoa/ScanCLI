import os
import sys
from colorama import init, Fore, Style
from modules.port_scanner import scan_network
from modules.whois_lookup import perform_whois_lookup
from modules.dns_enumerator import perform_dns_query
from modules.subdomain_scanner import perform_subdomain_scan
from modules.directory_scanner import perform_directory_scan

# Inicializar colorama
init()

def clear_screen():
    """Limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Exibe o banner da aplicação."""
    banner = f"""
{Fore.GREEN}
████████╗███████╗ ██████╗██╗  ██╗ █████╗  ██████╗██╗  ██╗
╚══██╔══╝██╔════╝██╔════╝██║  ██║██╔══██╗██╔════╝██║ ██╔╝
   ██║   █████╗  ██║     ███████║███████║██║     █████╔╝ 
   ██║   ██╔══╝  ██║     ██╔══██║██╔══██║██║     ██╔═██╗ 
   ██║   ███████╗╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗
   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝  
{Style.RESET_ALL}
    Ferramenta de Reconhecimento - v1.0
    """
    print(banner)

def print_menu():
    """Exibe o menu principal."""
    print("\n=== Feito por Fernando Alzueta ===")
    print("1. Port Scanner")
    print("2. WHOIS Lookup")
    print("3. DNS Enumerator")
    print("4. Subdomain Scanner")
    print("5. Directory Scanner")
    print("6. Exit")
    return input("Escolha uma opção: ")

def port_scanner_menu():
    """Menu para o Port Scanner."""
    ip_or_cidr = input("Digite o IP/Hostname: ")
    if not ip_or_cidr:
        print("IP/Hostname é obrigatório!")
        return
    
    port_range = input("Digite o intervalo de portas (ex: 1-1000): ")
    if not port_range:
        print("Intervalo de portas é obrigatório!")
        return
    
    portas = []
    if "-" in port_range:
        try:
            start, end = map(int, port_range.split("-"))
            portas = list(range(start, end + 1))
        except ValueError:
            print("Formato de intervalo de portas inválido!")
            return
    else:
        try:
            portas = [int(p) for p in port_range.split(",")]
        except ValueError:
            print("Formato de portas inválido!")
            return
    
    protocol = input("Escolha o protocolo (TCP/UDP): ").upper()
    if protocol not in ["TCP", "UDP"]:
        print("Protocolo inválido! Use TCP ou UDP.")
        return
    
    scan_network(ip_or_cidr, portas, protocol)

def whois_lookup_menu():
    """Menu para o WHOIS Lookup."""
    domain = input("Digite o domínio: ")
    if not domain:
        print("Domínio é obrigatório!")
        return
    
    perform_whois_lookup(domain)

def dns_enumerator_menu():
    """Menu para o DNS Enumerator."""
    domain = input("Digite o domínio: ")
    if not domain:
        print("Domínio é obrigatório!")
        return
    
    record_type = input("Digite o tipo de registro (A, AAAA, MX, NS, TXT, CNAME, SOA): ").upper()
    valid_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]
    if record_type not in valid_types:
        print(f"Tipo de registro inválido! Tipos válidos: {', '.join(valid_types)}")
        return
    
    perform_dns_query(domain, record_type)

def subdomain_scanner_menu():
    """Menu para o Subdomain Scanner."""
    domain = input("Digite o domínio: ")
    if not domain:
        print("Domínio é obrigatório!")
        return
    
    perform_subdomain_scan(domain)

def directory_scanner_menu():
    """Menu para o Directory Scanner."""
    url = input("Digite a URL: ")
    if not url:
        print("URL é obrigatória!")
        return
    
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    
    wordlist_path = input("Digite o caminho da wordlist (ex: ./data/wordlists/commmon.txt): ")
    
    if wordlist_path and os.path.isfile(wordlist_path):
        with open(wordlist_path, 'r') as f:
            wordlist = [line.strip() for line in f if line.strip()]
        perform_directory_scan(url, wordlist)
    else:
        perform_directory_scan(url)

def main():
    """Função principal do programa."""
    while True:
        clear_screen()
        print_banner()
        choice = print_menu()
        
        if choice == "1":
            port_scanner_menu()
        elif choice == "2":
            whois_lookup_menu()
        elif choice == "3":
            dns_enumerator_menu()
        elif choice == "4":
            subdomain_scanner_menu()
        elif choice == "5":
            directory_scanner_menu()
        elif choice in ["6", "exit", "quit", "q"]:
            print("Saindo...")
            sys.exit(0)
        else:
            print("Opção inválida!")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperação interrompida pelo usuário.")
        sys.exit(0)