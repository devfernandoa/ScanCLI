# Roteiro 2 - Relatório

---

## Perguntas

---

### 1. Cinco Ferramentas Úteis de Reconhecimento (Além de Port Scanning)

- Shodan (shodan.io)
  - Função: Motor de busca para dispositivos conectados à internet (IoT, ICS, servidores).
  - Justificativa: Encontra ativos expostos que não são sites comuns, como bancos de dados sem senha, sistemas industriais ou câmeras. Essencial para mapear a superfície de ataque além do óbvio.

- theHarvester
  - Função: Coleta e-mails, nomes, subdomínios de fontes públicas (Google, Bing, etc. - OSINT).
  - Justificativa: Útil para encontrar alvos para phishing, ataques de força bruta em logins (password spraying) e descobrir subdomínios esquecidos que podem ser menos seguros.

- Nmap Scripting Engine (NSE) & Version Detection (nmap -sV --script xxxxx)
  - Função: Identifica a versão exata dos serviços (-sV) e usa scripts (NSE) para tarefas avançadas como detecção de vulnerabilidades, enumeração de usuários, etc.
  - Justificativa: Saber a versão exata ajuda a encontrar exploits conhecidos (CVEs). Scripts podem encontrar falhas de configuração ou informações sensíveis.

- Sublist3r / Amass
  - Função: Especializados em encontrar subdomínios usando diversas fontes (motores de busca, DNS passivo, brute-force).
  - Justificativa: Descobrem alvos "escondidos" ou esquecidos (como dev.empresa.com ou admin.empresa.com) que podem ter segurança mais fraca.

- Dirb / Gobuster / Ffuf
  - Função: Encontram diretórios e arquivos escondidos em servidores web usando listas de palavras (wordlists).
  - Justificativa: Podem revelar painéis administrativos, arquivos de backup com senhas, APIs não documentadas ou outras informações sensíveis não linkadas diretamente no site.

---

### 2. Diferença entre SYN Scan e TCP Connect Scan

- TCP Connect Scan (-sT):
  - Como funciona: Tenta completar a conexão TCP padrão (handshake de 3 vias: SYN -> SYN/ACK -> ACK). Usa a chamada connect() do sistema operacional.
  - Características: Completa a conexão. Não precisa de privilégios de root/admin. É facilmente detectado e registrado (logado) pela aplicação no alvo. Mais lento.
  - Cenário ideal: Quando você não tem privilégios de root/admin, ou quando scans do tipo SYN estão sendo bloqueados.

- SYN Scan (-sS):
  - Como funciona: Envia um pacote SYN. Se recebe SYN/ACK (porta aberta), envia um RST para derrubar a conexão antes de completar o handshake. Se recebe RST (porta fechada), marca como fechada.
  - Características: Não completa a conexão ("half-open"). Precisa de privilégios de root/admin para criar pacotes customizados. Menos propenso a ser logado pela aplicação, mas facilmente detectado por firewalls/IPS modernos. Mais rápido. Considerado mais "furtivo" (stealth) em relação à aplicação.
  - Cenário ideal: Quando você tem privilégios de root/admin. É o scan padrão do Nmap para usuários privilegiados por ser rápido e evitar logs de aplicação.

---

### 3. Como Evitar Detecção por IPS Durante Reconhecimento

IPS (Intrusion Prevention Systems) detectam scans por padrões anormais (muitas conexões, scans em sequencia) e assinaturas. Técnicas para evitar:

- Diminuir a Velocidade (Timing/Rate Limiting):
  - Técnica: Reduzir drasticamente a velocidade do scan (Nmap: -T0, -T1, --scan-delay, --max-rate).
  - Impacto: Mais eficaz contra detecção baseada em taxa/volume. Torna o scan extremamente lento (horas/dias), afetando a eficiência.

- Limitar o Escopo do Scan:
  - Técnica: Escanear menos portas (ex: --top-ports 100 ou -p 80,443) ou apenas IPs específicos, em vez de redes inteiras.
  - Impacto: Gera menos tráfego, reduzindo a chance de ativar alertas. Diminui a abrangência do scan (pode perder serviços em portas não comuns).

- Ocultar a Origem (Proxy/VPN):
  - Técnica: Roteador o tráfego do scan através de proxies (ex: proxychains) ou VPNs.
  - Impacto: Esconde seu IP real. Se o IP do proxy/VPN for bloqueado, seu IP real fica protegido. Adiciona lentidão. A reputação do IP de saída é importante (alguns são bloqueados por padrão).

- Usar Decoys (-D no Nmap):
  - Técnica: Faz o scan parecer vir de múltiplos IPs falsos (decoy) além do seu IP real.
  - Impacto: Dificulta a identificação do atacante real nos logs do alvo. Não reduz o tráfego real e pode ser detectado por alguns IPS ou regras anti-spoofing.

## Ferramentas Implementadas

### 1. `port_scanner.py`

- **Função:** Realiza escaneamento de portas TCP para identificar serviços ativos em um host.
- **Tecnologias:** `socket`, `concurrent.futures.ThreadPoolExecutor`
- **Uso Típico:** Identificar serviços como HTTP (porta 80), SSH (porta 22), FTP (porta 21), etc.

---

### 2. `directory_scanner.py`

- **Função:** Força bruta em diretórios e arquivos de um servidor web.
- **Tecnologias:** `requests`
- **Uso Típico:** Identificar caminhos ocultos (e.g. `/admin`, `/login`, `/robots.txt`).

---

### 3. `whois_lookup.py`

- **Função:** Realiza consulta WHOIS para obter informações sobre o domínio.
- **Tecnologias:** `whois` (biblioteca Python)
- **Uso Típico:** Verificar registrante, datas de criação/expiração e contatos administrativos.

---

### 4. `dns_enumerator.py`

- **Função:** Enumera registros DNS (A, MX, NS, TXT) de um domínio.
- **Tecnologias:** `dnspython`
- **Uso Típico:** Coleta de inteligência sobre a infraestrutura de rede.

---

### 5. `subdomain_scanner.py`

- **Função:** Realiza brute-force de subdomínios usando uma wordlist.
- **Tecnologias:** `dns.resolver`
- **Uso Típico:** Encontrar subdomínios ativos como `api.exemplo.com`, `mail.exemplo.com`, etc.

---

## Decisões de Arquitetura

- **Modularidade:** Cada ferramenta está isolada em seu módulo Python.
- **Reuso de Código:** Há um diretório `utils` para funções auxiliares.
- **Integração Central:** O script `main.py` coordena a execução das ferramentas e interações com o usuário.
