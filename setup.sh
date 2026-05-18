#!/bin/bash
set -e

echo "===== Instalando VocesClaras-STT ====="

# 1. Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python -m venv venv
fi

# 2. Activar entorno virtual
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate   # Windows Git Bash
else
    source venv/bin/activate       # Linux/macOS
fi

# 3. Instalar dependencias
echo "Instalando dependencias Python..."
pip install -r requirements.txt

# 4. Descargar FFmpeg si no está en bin/
if [ ! -f "bin/ffmpeg.exe" ] || [ ! -f "bin/ffprobe.exe" ]; then
    echo "Descargando FFmpeg..."
    FFMPEG_URL="https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    curl -L "$FFMPEG_URL" -o ffmpeg.zip
    unzip -o ffmpeg.zip
    # Buscar la carpeta extraída (contiene bin/)
    FFMPEG_DIR=$(find . -maxdepth 1 -type d -name "ffmpeg-*" | head -1)
    cp "$FFMPEG_DIR/bin/ffmpeg.exe" bin/
    cp "$FFMPEG_DIR/bin/ffprobe.exe" bin/
    rm -rf "$FFMPEG_DIR" ffmpeg.zip
    echo "FFmpeg instalado en bin/"
else
    echo "FFmpeg ya está presente en bin/"
fi

echo ""
echo "===== Instalación completada ====="
echo "Para ejecutar la interfaz gráfica:"
echo "  source venv/Scripts/activate   # (o venv/bin/activate)"
echo "  python src/components/interfaz.py"
