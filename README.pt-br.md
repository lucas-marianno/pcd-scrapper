# PCD Scrapper

Um web scraper baseado em Python projetado para extrair e baixar currículos (CVs) de Pessoas com Deficiência (PCD) do portal de empregos **empregos.com**.

## Visão Geral

**PCD Scrapper** automatiza o processo de busca e download de documentos de currículo (CV) do empregos.com, visando especificamente candidatos com vários tipos de deficiência. A ferramenta utiliza a API da plataforma combinada com automação de navegador para baixar arquivos PDF de forma confiável, organizados por localização, cargo e tipo de deficiência.

> **Aviso Legal Importante**: Esta ferramenta foi projetada para fins legítimos de coleta de dados. Os usuários devem cumprir os termos de serviço do empregos.com e as leis brasileiras aplicáveis em relação à raspagem de dados e privacidade.

## Funcionalidades

* **Busca Baseada em API**: Utiliza a API REST do empregos.com para buscas eficientes de candidatos.
* **Automação de Navegador**: Aproveita o Playwright para downloads de PDF confiáveis com preservação de formatação.
* **Cache de Requisições**: Implementa cache inteligente para reduzir chamadas de API e melhorar o desempenho.
* **Filtragem Flexível**: Busca por múltiplos cargos, localizações e tipos de deficiência simultaneamente.
* **Parâmetros Configuráveis**: Configuração baseada em YAML com suporte a variáveis de ambiente.
* **Lógica de Retentativa**: Mecanismo de retentativa automática para downloads falhos com limites configuráveis.
* **Modo de Depuração (Debug)**: Modo de teste leve para validar configurações antes da execução completa.
* **Saída Organizada**: Estrutura automaticamente os downloads por localização → cargo → tipo de deficiência.

## Stack Tecnológica

* **Python 3.14+** (requires-python >=3.14)
* **Playwright**: Automação de navegador cross-browser (1.58.0+)
* **Requests & Requests-Cache**: Requisições HTTP com cache baseado em SQLite (2.32.5+, 1.3.1+)
* **PyYAML**: Parsing de arquivos de configuração (6.0.3+)
* **Python-dotenv**: Gerenciamento de variáveis de ambiente (0.9.9+)
* **pytest**: Framework de testes unitários (9.0.2+)

## Estrutura do Projeto

```
pcd-scrapper/
├── run.py                          # Ponto de entrada - executa a raspagem
├── pyproject.toml                  # Metadados do projeto e dependências
├── CONFIG.yaml                     # Configuração do usuário (gerado automaticamente a partir do padrão)
├── INSTALADOR.bat                  # Script de instalação para Windows
├── EXECUTAR.bat                    # Script de execução para Windows
│
├── src/
│   ├── pcd_scrapper.py            # Classe orquestradora principal
│   ├── config/
│   │   ├── api_config.py          # Constantes de endpoints da API
│   │   ├── script_config.py       # Carregador de configuração (YAML + variáveis de ambiente)
│   │   └── default_config.yaml    # Template de configuração padrão
│   ├── service/
│   │   └── api_service.py         # Lógica de negócio (autenticação, busca, download)
│   ├── repository/
│   │   └── api_repository.py      # Camada de comunicação com a API
│   └── dto/
│       └── candidate_response.py  # Objeto de transferência de dados para respostas da API
│
├── scripts/
│   └── clear-cache.sh             # Utilitário para limpar o cache local
│
├── test/                          # Testes unitários (espaço reservado)
│
└── .requests_cache/               # Banco de dados de cache SQLite (criado automaticamente)
```


## Início Rápido

### Configuração no Windows (instalador):

1.  **Execute o Script de Instalação**:
    ```batch
    INSTALADOR.bat
    ```
    Isso irá automaticamente:
    * Instalar o Scoop (se não estiver presente)
    * Instalar o gerenciador de pacotes UV
    * Sincronizar as dependências do Python
    * Instalar os navegadores do Playwright
    * Criar atalhos na área de trabalho e o arquivo de configuração

2.  **Defina suas Configurações**:
    * Abra o `CONFIG.yaml` com o Bloco de Notas.
    * Siga as instruções detalhadas no arquivo para configuração da conta.
    * Atualize os parâmetros de busca (cargos, localizações, deficiências).

3.  **Execute o Scraper**:
    ```batch
    EXECUTAR.bat
    ```
    Os PDFs baixados aparecerão na pasta `output/`.

### Configuração no Linux/macOS (instalação manual):

1.  **Clone o Repositório**:
    ```bash
    git clone https://github.com/lucas-marianno/pcd-scrapper.git
    cd pcd-scrapper
    ```
   

2.  **Instale o UV**:
    ```bash
    # Arch
    sudo pacman -S uv
    # Debian
    sudo apt-get install uv
    # Ubuntu / mint
    sudo apt install uv
    ```
   

3.  **Instale o Playwright**:
    ```
    uv sync
    uv run playwright install
    ```
   

4.  **Configure a Aplicação**:
    Copie a configuração padrão para a raiz e edite conforme necessário.
    ```bash
    cp src/config/default_config.yaml CONFIG.yaml
    nvim CONFIG.yaml  # Edite com seu editor preferido
    ```
   

5.  **Execute o Scraper**:
    ```bash
    uv run python run.py
    ```
   

## Guia de Configuração

### Configuração de Conta

O arquivo `CONFIG.yaml` requer uma conta no empregos.com. **Use uma conta temporária** para evitar sanções:

1.  **Obtenha um E-mail Temporário**: Visite [https://temp-mail.org/](https://temp-mail.org/)
2.  **Gere um CNPJ Aleatório**: Utilize [https://www.4devs.com.br/gerador_de_cnpj](https://www.4devs.com.br/gerador_de_cnpj)
3.  **Crie uma Conta**: Registre-se em [https://b2b.empregos.com.br/empresa/cadastro/comecar-cadastro](https://b2b.empregos.com.br/empresa/cadastro/comecar-cadastro)
    * Cargo: "Gerente de recrutamento e seleção"
    * Tipo de conta: "Para minha empresa"
4.  **Salve as Credenciais**: Você pode salvar suas credenciais em um destes três lugares:

    > **Nota**: Ordem de precedência na leitura das credenciais: Variáveis de Ambiente > arquivo `.env` > arquivo `CONFIG.yaml`.

    * No `CONFIG.yaml`:
    ```yaml
    login:
      username: "seu-email-temporario@example.com"
      password: "sua-senha"
    ```
    * No `.env`: Crie um arquivo chamado `.env` na raiz do projeto e escreva:
    ```bash
    EMPREGOS_USERNAME="seu-email@example.com"
    EMPREGOS_PASSWORD="sua-senha"
    ```
    * Em **Variáveis de Ambiente**: Execute o seguinte antes de rodar o scraper:
    ```bash
    # Linux:
    export EMPREGOS_USERNAME="seu-email@example.com"
    export EMPREGOS_PASSWORD="sua-senha"

    # Windows (cmd):
    set EMPREGOS_USERNAME "seu-email@example.com"
    set EMPREGOS_PASSWORD "sua-senha"
    ```
    > **Nota**: Apenas para a sessão! Se você quiser que as variáveis de ambiente persistam entre sessões, adicione-as ao seu `PATH`.

### Parâmetros de Busca

```yaml
search:
  job_roles: 
    - "Administrativo"           # Necessário correspondência exata
    - "Consultor Comercial"
  locations:
    - "Osasco, SP"               # Nome da cidade, código do estado
    - "São Paulo, SP"
  disabilities:
    - "Pessoa com deficiência"
    - "Pessoa com deficiência auditiva"
    - "Pessoa com deficiência física"
    - "Pessoa com deficiência mental"
    - "Pessoa com deficiência múltipla"
    - "Pessoa com deficiência visual"
```


> **Nota**: Os termos de filtragem devem corresponder exatamente ao que aparece no empregos.com (case-sensitive, acentos importam).

### Configurações de Download

```yaml
download:
  timeout: 5000              # Milissegundos máximos por download de PDF (padrão: 5000)
  retry_limit: 5             # Tentativas de redownload em caso de falha (padrão: 5)
  ask_confirmation: True     # Solicitar confirmação antes de iniciar downloads (padrão: True)
  cache_duration: 24         # Duração do cache em horas (padrão: 24)
  output_dir: "output/"      # Diretório para os PDFs baixados
```


### Teste suas configurações

Ative o modo de depuração para validar a configuração sem baixar muitos arquivos:

```yaml
debug_mode:
  enabled: True
  search_page_limit: 1       # Busca apenas a primeira página de resultados
  cv_download_limit: 5       # Baixa apenas os primeiros 5 currículos por busca
```


## Fluxo de Execução

```
PcdScrapper.start_scraping()
├── Carrega configuração (YAML + variáveis de ambiente)
├── Autentica com a API do empregos.com
├── Para cada localização:
│   ├── Obtém coordenadas de geolocalização
│   └── Para cada cargo:
│       └── Para cada tipo de deficiência:
│           ├── Busca candidatos correspondentes (paginado)
│           ├── Coleta os IDs dos candidatos
│           ├── Solicita confirmação do usuário
│           └── Baixa cada CV como PDF (com lógica de retentativa)
└── Organiza arquivos: output/{localização}/{cargo}/{deficiência}/{id}.pdf
```


## Arquitetura da API

### Padrão de Três Camadas

1.  **Camada de Repositório** (`api_repository.py`):
    * Comunicação HTTP com cache
    * Manipulação de requisição/resposta
    * Gerenciamento de erros

2.  **Camada de Serviço** (`api_service.py`):
    * Orquestração da lógica de negócio
    * Fluxo de autenticação
    * Coordenação de busca e download de CV
    * Automação de navegador via Playwright

3.  **Camada de Configuração** (`script_config.py`):
    * Parsing de YAML
    * Sobrescrita por variáveis de ambiente
    * Validação de configuração

## Estrutura de Saída

Os arquivos baixados são organizados automaticamente:

```
output/
├── Osasco, SP/
│   └── Administrativo/
│       ├── Pessoa com deficiência visual/
│       │   ├── 1.pdf
│       │   ├── 2.pdf
│       │   └── ...
│       └── Pessoa com deficiência física/
│           └── ...
└── São Paulo, SP/
    └── ...
```