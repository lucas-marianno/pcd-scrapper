# PCD Scrapper

A Python-based web scraper designed to extract and download CVs (resumes) of People with Disabilities (PCD) from the Brazilian job portal **empregos.com**.

## Overview

**PCD Scrapper** automates the process of searching and downloading curriculum vitae (CV) documents from empregos.com, specifically targeting job candidates with various types of disabilities. The tool uses the platform's API combined with browser automation to reliably download PDF files organized by location, job role, and disability type.

> **Important Legal Notice**: This tool is designed for legitimate data collection purposes. Users must comply with empregos.com's terms of service and applicable Brazilian laws regarding data scraping and privacy.

## Features

- **API-Based Search**: Uses empregos.com's REST API for efficient candidate searches
- **Browser Automation**: Leverages Playwright for reliable PDF downloads with formatting preservation
- **Request Caching**: Implements intelligent caching to reduce API calls and improve performance
- **Flexible Filtering**: Search by multiple job roles, locations, and disability types simultaneously
- **Configurable Parameters**: YAML-based configuration with environment variable support
- **Retry Logic**: Automatic retry mechanism for failed downloads with configurable limits
- **Debug Mode**: Lightweight testing mode to validate configurations before full execution
- **Organized Output**: Automatically structures downloads by location → job role → disability type

## Technology Stack

- **Python 3.14+** (requires-python >=3.14)
- **Playwright**: Cross-browser automation (1.58.0+)
- **Requests & Requests-Cache**: HTTP requests with SQLite-based caching (2.32.5+, 1.3.1+)
- **PyYAML**: Configuration file parsing (6.0.3+)
- **Python-dotenv**: Environment variable management (0.9.9+)
- **pytest**: Unit testing framework (9.0.2+)

## Project Structure

```
pcd-scrapper/
├── run.py                          # Entry point - executes scraping
├── pyproject.toml                  # Project metadata and dependencies
├── CONFIG.yaml                     # User configuration (auto-generated from default)
├── INSTALADOR.bat                  # Windows installation script
├── EXECUTAR.bat                    # Windows execution script
│
├── src/
│   ├── pcd_scrapper.py            # Main orchestrator class
│   ├── config/
│   │   ├── api_config.py          # API endpoint constants
│   │   ├── script_config.py       # Configuration loader (YAML + env vars)
│   │   └── default_config.yaml    # Default configuration template
│   ├── service/
│   │   └── api_service.py         # Business logic (auth, search, download)
│   ├── repository/
│   │   └── api_repository.py      # API communication layer
│   └── dto/
│       └── candidate_response.py  # Data transfer object for API responses
│
├── scripts/
│   └── clear-cache.sh             # Utility to clear local cache
│
├── test/                          # Unit tests (placeholder)
│
└── .requests_cache/               # SQLite cache database (auto-created)
```

## Quick Start

### Windows Setup (installer):

1. **Run the Installation Script**:
   ```batch
   INSTALADOR.bat
   ```
   This will automatically:
   - Install Scoop (if not present)
   - Install UV package manager
   - Sync Python dependencies
   - Install Playwright browsers
   - Create desktop shortcuts and configuration file

2. **Configure Your Settings**:
   - Open `CONFIG.yaml` with Notepad
   - Follow the detailed instructions in the file for account setup
   - Update search parameters (job roles, locations, disabilities)

3. **Execute the Scraper**:
   ```batch
   EXECUTAR.bat
   ```
   Downloaded PDFs will appear in the `output/` folder

### Linux/macOS setup (manual installation):

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/lucas-marianno/pcd-scrapper.git
   cd pcd-scrapper
   ```

2. **Install UV**:
   ```bash
   # Arch
   sudo pacman -S uv
   # Debian
   sudo apt-get install uv
   # Ubuntu / mint
   sudo apt install uv
   ```

3. **Install playwright**:
   ```
   uv sync
   uv run playwright install
   ```

4. **Configure the Application**:  
   Copy the default config to the root and edit as needed
   ```bash
   cp src/config/default_config.yaml CONFIG.yaml
   nvim CONFIG.yaml  # Edit with your preferred editor
   ```

6. **Run the Scraper**:
   ```bash
   uv run python run.py
   ```

## Configuration Guide

### Account Setup

The `CONFIG.yaml` file requires an empregos.com account. **Use a temporary account** to avoid sanctions:

1. **Get a Temporary Email**:  
   Visit https://temp-mail.org/
2. **Generate a Random CNPJ**:  
   Use https://www.4devs.com.br/gerador_de_cnpj
3. **Create an Account**:  
   Register at https://b2b.empregos.com.br/empresa/cadastro/comecar-cadastro
   - Role: "Gerente de recrutamento e seleção" (Recruitment Manager)
   - Account type: "Para minha empresa" (For my company)
4. **Save Credentials**:  
   You can save you credentials in one of the three different places:
   
   > **Note**: Order of precedence in parsing credentials  
   > ENV VARS > `.env` file > `CONFIG.yaml` file
   
   - in `CONFIG.yaml`:
   ```yaml
   login:
     username: "your-temp-email@example.com"
     password: "your-password"
   ```
   - in `.env`:  
   Create a file named `.env` in root of the project and write:
   ```bash
   EMPREGOS_USERNAME="your-email@example.com"
   EMPREGOS_PASSWORD="your-password"
   ```
   - in **Environment Variables**:  
   Run the following before running the scrapper:  
   ```bash
   # Linux:
   export EMPREGOS_USERNAME="your-email@example.com"
   export EMPREGOS_PASSWORD="your-password"

   # Windows (cmd):
   set EMPREGOS_USERNAME "your-email@example.com"
   set EMPREGOS_PASSWORD "your-password"
   ```
   > **Note**: Session only!  
   > If you want env vars to persist across sessions, add them to you `PATH`.  

### Search Parameters

```yaml
search:
  job_roles: 
    - "Administrativo"           # Exact match required
    - "Consultor Comercial"
  locations:
    - "Osasco, SP"               # City name, state code
    - "São Paulo, SP"
  disabilities:
    - "Pessoa com deficiência"
    - "Pessoa com deficiência auditiva"
    - "Pessoa com deficiência física"
    - "Pessoa com deficiência mental"
    - "Pessoa com deficiência múltipla"
    - "Pessoa com deficiência visual"
```

> **Note**: Filter terms must match exactly what appears on empregos.com (case-sensitive, accents matter)

### Download Settings

```yaml
download:
  timeout: 5000              # Max milliseconds per PDF download (default: 5000)
  retry_limit: 5             # Failed download retry attempts (default: 5)
  ask_confirmation: True     # Prompt before starting downloads (default: True)
  cache_duration: 24         # Cache duration in hours (default: 24)
  output_dir: "output/"      # Directory for downloaded PDFs
```

### Test your settings 

Enable debug mode to validate setup without downloading many files:

```yaml
debug_mode:
  enabled: True
  search_page_limit: 1       # Only fetch first page of results
  cv_download_limit: 5       # Only download first 5 CVs per search
```

## Execution Flow

```
PcdScrapper.start_scraping()
├── Load configuration (YAML + env vars)
├── Authenticate with empregos.com API
├── For each location:
│   ├── Get geolocation coordinates
│   └── For each job role:
│       └── For each disability type:
│           ├── Search for matching candidates (paginated)
│           ├── Collect candidate IDs
│           ├── Prompt user confirmation
│           └── Download each CV as PDF (with retry logic)
└── Organize files: output/{location}/{role}/{disability}/{id}.pdf
```

## API Architecture

### Three-Layer Pattern

1. **Repository Layer** (`api_repository.py`):
   - HTTP communication with caching
   - Request/response handling
   - Error management

2. **Service Layer** (`api_service.py`):
   - Business logic orchestration
   - Authentication flow
   - CV search and download coordination
   - Browser automation via Playwright

3. **Configuration Layer** (`script_config.py`):
   - YAML parsing
   - Environment variable override
   - Configuration validation

## Output Structure

Downloaded files are automatically organized:

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

