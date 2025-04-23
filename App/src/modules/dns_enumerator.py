import dns.resolver
from colorama import Fore, Style

def perform_dns_query(domain, record_type):
    """Executa uma consulta DNS para um domínio e tipo de registro."""
    try:
        print(f"Consultando registros DNS {record_type} para {domain}...")
        answers = dns.resolver.resolve(domain, record_type)
        print(f"{Fore.GREEN}=== Registros DNS {record_type} para {domain} ==={Style.RESET_ALL}\n")
        
        for rdata in answers:
            if record_type == "A":
                print(f"{Fore.CYAN}IP:{Style.RESET_ALL} {rdata.address}")
            elif record_type == "AAAA":
                print(f"{Fore.CYAN}IPv6:{Style.RESET_ALL} {rdata.address}")
            elif record_type == "MX":
                print(f"{Fore.CYAN}Mail Server:{Style.RESET_ALL} {rdata.exchange} (Prioridade: {rdata.preference})")
            elif record_type == "NS":
                print(f"{Fore.CYAN}Name Server:{Style.RESET_ALL} {rdata.target}")
            elif record_type == "TXT":
                print(f"{Fore.CYAN}TXT Record:{Style.RESET_ALL} {rdata.strings}")
            elif record_type == "CNAME":
                print(f"{Fore.CYAN}CNAME:{Style.RESET_ALL} {rdata.target}")
            elif record_type == "SOA":
                print(f"{Fore.CYAN}SOA:{Style.RESET_ALL} {rdata.mname} (Serial: {rdata.serial})")
            else:
                print(f"{rdata}")
        
        return True
    except dns.resolver.NXDOMAIN:
        print(f"{Fore.RED}Domínio não encontrado.{Style.RESET_ALL}")
    except dns.resolver.NoAnswer:
        print(f"{Fore.YELLOW}Não há registros {record_type} para {domain}.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Erro na consulta DNS: {e}{Style.RESET_ALL}")
    
    return False