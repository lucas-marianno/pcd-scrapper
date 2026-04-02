@echo off

chcp 65001 > nul
set PYTHONUTF8=1

cls

echo ==========================================
echo Iniciando a Configuracao do Projeto...
echo ==========================================

echo [1/5] Verificando instalação do Scoop...
where scoop >nul 2>nul
if %errorlevel% neq 0 (
    echo Scoop não foi encontrado e será instalado agora.
    powershell -NoProfile -ExecutionPolicy Bypass -Command "iex (new-object net.webclient).downloadstring('https://get.scoop.sh')"
    set "PATH=%USERPROFILE%\scoop\shims;%PATH%"
) else (
    echo Scoop já está instalado. Pulando para o próximo passo.
)

echo [2/5] Instalando o uv...
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo UV não foi encontrado e será instalado agora.
    call scoop install uv
) else (
    echo UV já está instalado. Pulando para o próximo passo.
)

echo [3/5] Sincronizando dependencias com o uv...
call uv sync

echo [4/5] Instalando navegadores do Playwright...
:: uv run roda o comando diretamente dentro do .venv sem precisar ativar manualmente
call uv run playwright install

echo [5/5] Criando configuracao padrao e atalhos...
:: Usa copy normal ao inves de xcopy para evitar prompts de confirmacao no terminal
copy "src\config\default_config.yaml" "CONFIG.yaml" > nul

setlocal enabledelayedexpansion

set "destDir=%USERPROFILE%\Desktop\PCD Scrapper"

if not exist "%destDir%" mkdir "%destDir%"

set "items=CONFIG.yaml EXECUTAR.bat output"

for %%I in (%items%) do (
    set "filename=%%~I"
    set "shortcutPath=%destDir%\%%~nxI.lnk"
    set "targetPath=%~dp0%%~I"

    if exist "!shortcutPath!" del "!shortcutPath!"

    :: Adicionado -NoProfile para o powershell rodar um pouco mais rapido
    powershell -NoProfile -command "$s=(New-Object -COM WScript.Shell).CreateShortcut('!shortcutPath!');$s.TargetPath='!targetPath!';$s.Save()"
)

cls

echo ==========================================
echo Instalacao concluida com sucesso!!!
echo ==========================================
echo.
echo Foi criada uma pasta 'PCD Scrapper' na sua area de trabalho.
echo.
echo PASSO A PASSO:
echo 1. Leia atentamente o arquivo CONFIG.yaml (abra com o bloco de notas)
echo 2. Configure o arquivo CONFIG.yaml com as opcoes desejadas
echo 3. Clique duas vezes em EXECUTAR.bat
echo 4. Os arquivs .pdf baixados estarão na pasta output\
echo.

pause
