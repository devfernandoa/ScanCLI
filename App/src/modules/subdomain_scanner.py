import dns.resolver
from colorama import Fore, Style
import concurrent.futures
import threading

def check_subdomain_exists(subdomain):
    """Verifica se um subdomínio existe utilizando DNS."""
    try:
        answers = dns.resolver.resolve(subdomain, 'A')
        return True, answers[0].address
    except:
        return False, None

def perform_subdomain_scan(domain):
    """Executa o scan de subdomínios."""
    try:
        # Lista de prefixos comuns para tentar
        common_subdomains = [
            "www", "mail", "ftp", "webmail", "admin", "blog", 
            "dev", "api", "test", "stage", "git", "gitlab", "github",
            "portal", "vpn", "cloud", "mobile", "app", "cdn", "media",
            "shop", "store", "secure", "support", "help", "docs",
            "wiki", "login", "m", "status", "beta"
        ]
        
        print(f"Buscando subdomínios para {domain}...")
        
        found_subdomains = []
        total = len(common_subdomains)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {}
            
            for i, sub in enumerate(common_subdomains):
                subdomain = f"{sub}.{domain}"
                futures[executor.submit(check_subdomain_exists, subdomain)] = subdomain
                
                # Atualizar progresso
                if i % 5 == 0:
                    print(f"Progresso: {i}/{total} ({i/total:.0%})")
            
            for future in concurrent.futures.as_completed(futures):
                subdomain = futures[future]
                try:
                    exists, ip = future.result()
                    if exists:
                        found_subdomains.append((subdomain, ip))
                        print(f"{Fore.GREEN}Encontrado: {subdomain} -> {ip}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Erro ao verificar {subdomain}: {e}{Style.RESET_ALL}")
        
        # Resumo final
        if found_subdomains:
            print(f"\n{Fore.CYAN}=== {len(found_subdomains)} subdomínios encontrados ==={Style.RESET_ALL}")
            for subdomain, ip in found_subdomains:
                print(f"{subdomain} -> {ip}")
        else:
            print(f"\n{Fore.YELLOW}Nenhum subdomínio encontrado.{Style.RESET_ALL}")
        
        return True
    
    except Exception as e:
        print(f"{Fore.RED}Erro no scan de subdomínios: {e}{Style.RESET_ALL}")
        return False