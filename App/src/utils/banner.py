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