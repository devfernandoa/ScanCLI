def is_valid_ip(ip):
    """Verifica se um endereço IP é válido."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def is_valid_url(url):
    """Verifica se uma URL é válida."""
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// ou https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domínio
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # IPv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # IPv6
        r'(?::\d+)?'  # porta
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def is_valid_port(port):
    """Verifica se um número de porta é válido."""
    return isinstance(port, int) and 0 <= port <= 65535

def is_valid_cidr(cidr):
    """Verifica se uma notação CIDR é válida."""
    try:
        ipaddress.ip_network(cidr, strict=False)
        return True
    except ValueError:
        return False