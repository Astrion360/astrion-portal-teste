@echo off
setlocal
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
  echo O Node.js nao esta disponivel. Abra index.html para navegar nos arquivos locais.
  pause
  exit /b 1
)
echo.
echo ASTRION - PREVIA LOCAL
echo Abra http://127.0.0.1:4173/ no navegador.
echo Mantenha esta janela aberta enquanto usa a previa.
echo Pressione Ctrl+C para encerrar.
echo.
node server.cjs
