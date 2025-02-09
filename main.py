from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM, getaddrinfo, timeout, error
from textual.app import App
from textual.widgets import Header, Footer, Input, Button, Log
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive
from portsDict import well_known_ports
from colorama import Fore, Style
from threading import Thread, Event
import ipaddress
import re

class PortScannerApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    Container {
        width: 80%;
        height: 80%;
        border: solid green;
        padding: 1;
    }
    #results {
        width: 100%;
        height: 60%;
        border: solid blue;
        padding: 1;
    }
    """

    def __init__(self):
        super().__init__()
        self.scan_thread = None
        self.stop_event = Event()

    def compose(self):
        yield Header()
        yield Vertical(
            Input(placeholder="Enter IP/Hostname or CIDR", id="ip_input"),
            Input(placeholder="Enter port range", id="port_input"),
            Horizontal(
                Button("Scan TCP", id="tcp_button"),
                Button("Scan UDP", id="udp_button"),
                Button("Stop", id="stop_button", disabled=True),
            ),
            Log(id="results"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "stop_button":
            self.stop_scan()
            return

        ip_or_cidr = self.query_one("#ip_input", Input).value
        port_range = self.query_one("#port_input", Input).value

        if not ip_or_cidr or not port_range:
            self.query_one("#results", Log).write("Please enter both IP/Hostname/CIDR and port range.")
            return

        if "-" in port_range:
            start, end = map(int, port_range.split("-"))
            portas = range(start, end + 1)
        else:
            portas = [int(port_range)]

        self.query_one("#results", Log).clear()

        self.query_one("#stop_button", Button).disabled = False
        self.query_one("#tcp_button", Button).disabled = True
        self.query_one("#udp_button", Button).disabled = True

        self.stop_event.clear()

        if event.button.id == "tcp_button":
            self.query_one("#results", Log).write("Scanning TCP ports...\n")
            self.scan_thread = Thread(target=self.scan_network, args=(ip_or_cidr, portas, "TCP"))
        elif event.button.id == "udp_button":
            self.query_one("#results", Log).write("Scanning UDP ports...\n")
            self.scan_thread = Thread(target=self.scan_network, args=(ip_or_cidr, portas, "UDP"))

        self.scan_thread.start()

    def stop_scan(self):
        """Stop the ongoing scan."""
        if self.scan_thread and self.scan_thread.is_alive():
            self.stop_event.set()
            self.query_one("#results", Log).write(f"{Fore.YELLOW}Scan stopped by user.{Style.RESET_ALL}\n")

        self.query_one("#stop_button", Button).disabled = True
        self.query_one("#tcp_button", Button).disabled = False
        self.query_one("#udp_button", Button).disabled = False

    def scan_network(self, ip_or_cidr, portas, protocol):
        """Scan a network using CIDR notation or a single IP."""
        try:
            if "/" in ip_or_cidr:
                network = ipaddress.ip_network(ip_or_cidr, strict=False)
                ips = [str(ip) for ip in network.hosts()]
            else:
                ips = [ip_or_cidr]

            for ip in ips:
                if self.stop_event.is_set():
                    break

                self.query_one("#results", Log).write(f"{Fore.CYAN}Scanning IP: {ip}{Style.RESET_ALL}\n")
                self.scan_ports(ip, portas, protocol)

        except Exception as e:
            self.query_one("#results", Log).write(f"{Fore.RED}Erro: {e}{Style.RESET_ALL}\n")
        finally:
            self.call_later(self.enable_scan_buttons)

    def scan_ports(self, ip, portas, protocol):
        """Scan ports for a specific IP address."""
        try:
            info = getaddrinfo(ip, None)
            ip = info[0][4][0]
            family = info[0][0]
            resultado = False

            for porta in portas:
                if self.stop_event.is_set():
                    break

                if protocol == "TCP":
                    s = socket(family, SOCK_STREAM)
                elif protocol == "UDP":
                    s = socket(family, SOCK_DGRAM)

                s.settimeout(0.5)
                try:
                    if protocol == "TCP":
                        if s.connect_ex((ip, porta)) == 0:
                            if str(porta) in well_known_ports:
                                self.query_one("#results", Log).write(f"{Fore.GREEN}{ip}: Porta {porta} aberta ({well_known_ports[str(porta)]}){Style.RESET_ALL}\n")
                            else:
                                self.query_one("#results", Log).write(f"{Fore.GREEN}{ip}: Porta {porta} aberta{Style.RESET_ALL}\n")
                            resultado = True
                    elif protocol == "UDP":
                        s.sendto(b'', (ip, porta))
                        data, addr = s.recvfrom(1024)
                        if str(porta) in well_known_ports:
                            self.query_one("#results", Log).write(f"{Fore.GREEN}{ip}: Porta {porta} aberta ({well_known_ports[str(porta)]}){Style.RESET_ALL}\n")
                        else:
                            self.query_one("#results", Log).write(f"{Fore.GREEN}{ip}: Porta {porta} aberta{Style.RESET_ALL}\n")
                        resultado = True
                except timeout:
                    self.query_one("#results", Log).write(f"{Fore.YELLOW}{ip}: Porta {porta} filtrada{Style.RESET_ALL}\n")
                except error:
                    if protocol == "UDP":
                        self.query_one("#results", Log).write(f"{Fore.RED}{ip}: Porta {porta} fechada{Style.RESET_ALL}\n")
                finally:
                    s.close()

            if not resultado and not self.stop_event.is_set():
                self.query_one("#results", Log).write(f"{Fore.RED}{ip}: Nenhuma porta especificada está aberta :({Style.RESET_ALL}\n")
        except Exception as e:
            self.query_one("#results", Log).write(f"{Fore.RED}{ip}: Erro: {e}{Style.RESET_ALL}\n")

    def get_banner(self, sock):
        """Attempt to retrieve a banner from the socket."""
        try:
            sock.settimeout(2)
            banner = sock.recv(1024).decode().strip()
            return banner
        except:
            return None

    def detect_os_from_banner(self, banner):
        """Attempt to detect the OS from the banner."""
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

    def enable_scan_buttons(self):
        """Re-enable the Scan buttons and disable the Stop button."""
        self.query_one("#stop_button", Button).disabled = True
        self.query_one("#tcp_button", Button).disabled = False
        self.query_one("#udp_button", Button).disabled = False

if __name__ == "__main__":
    app = PortScannerApp()
    app.run()