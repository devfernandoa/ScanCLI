# Scan CLI

Scan CLI é uma ferramenta de reconhecimento unificado que permite realizar diversas operações de segurança em redes e domínios. Este projeto é uma versão baseada em terminal do ReconApp, que oferece funcionalidades como escaneamento de portas, consultas WHOIS, enumeração DNS, escaneamento de subdomínios e escaneamento de diretórios.

## Estrutura do Projeto

O projeto é organizado da seguinte forma:

```
App/
├── src
│   ├── modules                     # Módulos com funcionalidades específicas
│   │   ├── __init__.py
│   │   ├── port_scanner.py        # Lógica de escaneamento de portas
│   │   ├── whois_lookup.py        # Consulta WHOIS
│   │   ├── dns_enumerator.py      # Enumeração de registros DNS
│   │   ├── subdomain_scanner.py   # Escaneamento de subdomínios
│   │   └── directory_scanner.py   # Escaneamento de diretórios
│   ├── utils                       # Funções utilitárias
│   │   ├── __init__.py
│   │   ├── banner.py              # Funções para obter banners de serviços
│   │   └── validators.py          # Funções de validação de entradas
│   └── main.py                    # Orquestração da execução do aplicativo
├── data
│   └── wordlists
│       └── common_directories.txt  # Lista de diretórios comuns
├── requirements.txt               # Dependências do projeto
```

## Instalação

Na pasta App para instalar as dependências do projeto, execute o seguinte comando:

```
pip install -r requirements.txt
```

## Uso

Para executar a aplicação, utilize o seguinte comando:

```
python src/main.py
```

Siga as instruções na interface de linha de comando para interagir com as diferentes funcionalidades do ReconApp.

## Funcionalidades

- **Escaneamento de Portas**: Verifique portas abertas em um endereço IP ou intervalo de endereços.
- **Consulta WHOIS**: Obtenha informações sobre um domínio específico.
- **Enumeração DNS**: Realize consultas DNS para obter diferentes tipos de registros.
- **Escaneamento de Subdomínios**: Verifique a existência de subdomínios comuns para um domínio fornecido.
- **Escaneamento de Diretórios**: Utilize uma wordlist para verificar a existência de diretórios em uma URL.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.
