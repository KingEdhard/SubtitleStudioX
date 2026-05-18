Write-Host "===== Instalando VocesClaras-STT ====="

# 1. Crear entorno virtual si no existe
if (-Not (Test-Path "venv")) {
    Write-Host "Creando entorno virtual..."
    python -m venv venv
}

# 2. Activar entorno virtual
& venv\Scripts\Activate.ps1

# 3. Instalar dependencias
Write-Host "Instalando dependencias Python..."
pip install -r requirements.txt

# 4. Descargar FFmpeg si no está en bin\
if (-Not (Test-Path "bin\ffmpeg.exe") -or -Not (Test-Path "bin\ffprobe.exe")) {
    Write-Host "Descargando FFmpeg..."
    $url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    Invoke-WebRequest -Uri $url -OutFile ffmpeg.zip
    Expand-Archive -Path ffmpeg.zip -DestinationPath .
    $ffmpegDir = Get-ChildItem -Directory -Name "ffmpeg-*" | Select-Object -First 1
    Copy-Item "$ffmpegDir\bin\ffmpeg.exe" -Destination bin\
    Copy-Item "$ffmpegDir\bin\ffprobe.exe" -Destination bin\
    Remove-Item -Recurse -Force $ffmpegDir, ffmpeg.zip
    Write-Host "FFmpeg instalado en bin\"
} else {
    Write-Host "FFmpeg ya está presente en bin\"
}

Write-Host ""
Write-Host "===== Instalación completada ====="
Write-Host "Para ejecutar la interfaz gráfica:"
Write-Host "  venv\Scripts\Activate.ps1"
Write-Host "  python src/components/interfaz.py"
