import requests
import concurrent.futures
from colorama import Fore, Style

def check_url_exists(url):
    """Verifica se uma URL existe e retorna o código de status."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=3, allow_redirects=True)
        return response.status_code, len(response.content)
    except:
        return 404, 0

def perform_directory_scan(base_url, wordlist=None):
    """Executa o scan de diretórios."""
    try:
        # Usar wordlist padrão se não for especificada
        if not wordlist:
            wordlist = [
                "admin", "login", "wp-admin", "wp-login.php", "administrator",
                "backup", "backups", "database", "db", "log", "logs",
                "test", "demo", "dev", "development", "staging", "prod", "production",
                "api", "api/v1", "api/v2", "docs", "documentation", "swagger",
                "config", "configuration", "setup", "install", "uploads", "news",
                "images", "img", "css", "js", "javascript", "assets", "nba",
                "wp-content", "wp-includes", "dashboard", "admin/login", "201",
                "server-status", "phpinfo.php", "info.php", "robots.txt", "sitemap.xml"
            ]
        
        print(f"Escaneando diretórios em {base_url}...")
        
        found_dirs = []
        total = len(wordlist)
        
        # Remover barra no final da URL base se existir
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {}
            
            for i, path in enumerate(wordlist):
                url = f"{base_url}/{path}"
                futures[executor.submit(check_url_exists, url)] = url
                
                # Atualizar progresso
                if i % (10) == 0:
                    print(f"Progresso: {i}/{total} ({i/total:.0%})")
            
            for future in concurrent.futures.as_completed(futures):
                url = futures[future]
                try:
                    status_code, content_length = future.result()
                    if status_code < 400:  # Consideramos 2xx e 3xx como "encontrado"
                        found_dirs.append((url, status_code, content_length))
                        color = Fore.GREEN if status_code < 300 else Fore.YELLOW
                        print(f"{color}[{status_code}] {url} - {content_length} bytes{Style.RESET_ALL}")
                except Exception as e:
                    pass  # Ignoramos erros neste caso
        
        # Resumo final
        if found_dirs:
            print(f"\n{Fore.CYAN}=== {len(found_dirs)} caminhos encontrados ==={Style.RESET_ALL}")
            for url, status, size in found_dirs:
                color = Fore.GREEN if status < 300 else Fore.YELLOW
                print(f"{color}[{status}] {url} - {size} bytes{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}Nenhum caminho válido encontrado.{Style.RESET_ALL}")
        
        return True
    
    except Exception as e:
        print(f"{Fore.RED}Erro no scan de diretórios: {e}{Style.RESET_ALL}")
        return False