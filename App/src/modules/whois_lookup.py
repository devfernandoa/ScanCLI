import whois
from colorama import Fore, Style

def perform_whois_lookup(domain):
    """Executa uma consulta WHOIS para um domínio."""
    try:
        print(f"Consultando informações WHOIS para {domain}...")
        w = whois.whois(domain)
        print(f"{Fore.GREEN}=== Informações WHOIS para {domain} ==={Style.RESET_ALL}\n")
        
        # Formatar os resultados
        for key, value in w.items():
            # Ignorar campos vazios ou None
            if value:
                # Formatar listas (como name_servers)
                if isinstance(value, list):
                    print(f"{Fore.CYAN}{key.capitalize()}{Style.RESET_ALL}: {', '.join(str(v) for v in value)}")
                else:
                    print(f"{Fore.CYAN}{key.capitalize()}{Style.RESET_ALL}: {value}")
        
        return True
    except Exception as e:
        print(f"{Fore.RED}Erro ao consultar WHOIS: {e}{Style.RESET_ALL}")
        return False