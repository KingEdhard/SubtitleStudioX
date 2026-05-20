# 🎙️ SubtitleStudio – Transcripción profesional y subtitulado de muy alta precisión

**SubtitleStudio** transforma tus vídeos en inglés en experiencias accesibles en español latino con una **muy alta precisión**. El proceso es completamente automático, 100% local y optimizado para CPUs convencionales:

1. 🎚️ **Extrae y realza la voz** – Aísla y amplifica las frecuencias clave del diálogo para una claridad excepcional.
2. 📝 **Genera subtítulos en inglés** – Usa IA de última generación (`faster-whisper`) con marcas de tiempo milimétricas.
3. 🌎 **Traduce al español latino** – Modelo especializado (`Helsinki-NLP/opus-mt-en-es`) para resultados naturales y coherentes.
4. 💾 **Incrusta ambos subtítulos** – Crea un nuevo archivo de vídeo sin pérdida de calidad original.

Todo el proceso se ejecuta **100 % en local, sin GPU ni conexión a internet** (salvo la primera descarga de modelos).  
Diseñado para funcionar de forma eficiente en **procesadores Intel básicos** (Intel Inside, Celeron, Pentium) usando precisión `float32`.

## ⚙️ Instalación automática (recomendada)

Después de clonar o descargar el proyecto, ejecuta un solo comando según tu sistema:

- **Windows (PowerShell):** `.\setup.ps1`
- **Windows (Git Bash), Linux o macOS:** `chmod +x setup.sh && ./setup.sh`

Estos scripts crearán el entorno virtual, instalarán las dependencias y descargarán automáticamente `ffmpeg.exe` y `ffprobe.exe` en la carpeta `bin/`.

🔽 Para obtener el proyecto haz clic en el botón verde **Code** en GitHub y selecciona **Download ZIP** o copia la URL para clonarlo con `git clone`.

## 🔧 Instalación manual

1. Crea un entorno virtual: `python -m venv venv`
2. Actívalo:
   - Windows (PowerShell): `venv\Scripts\Activate.ps1`
   - Windows (Git Bash): `source venv/Scripts/activate`
   - Linux/macOS: `source venv/bin/activate`
3. Instala las dependencias: `pip install -r requirements.txt`
4. Descarga `ffmpeg.exe` y `ffprobe.exe` de gyan.dev (versión _release essentials_) y colócalos en la carpeta `bin/`.

## 🔄 Flujo de trabajo

1. **Selección de archivos** – Diálogo gráfico que permite elegir múltiples vídeos.
2. **Extracción y mejora de audio** – Detecta la pista en inglés, aplica el filtro de realce vocal y la convierte a WAV mono 16 kHz.
3. **Transcripción en inglés** – `faster-whisper` (modelo `medium` o `large-v3`) genera un archivo `.srt` con marcas de tiempo.
4. **Traducción al español** – `Helsinki-NLP/opus-mt-en-es` traduce cada segmento, conservando las marcas de tiempo.
5. **Incrustación** – `FFmpeg` multiplexa los subtítulos en un nuevo vídeo (MKV o MP4 elegible desde la interfaz gráfica).
6. **Limpieza** – Se eliminan los archivos temporales (WAV) y se pregunta si se desea borrar el vídeo original.

## 🔊 Mejoras en el audio

- Normalización dinámica (`dynaudnorm=f=150:g=31:p=0.95`)
- Realce de voces (+2 dB entre 400-4000 Hz con `firequalizer`)
- Conversión a mono 16 kHz para máxima compatibilidad con Whisper

## 📦 Conservación de datos originales

- Vídeo copiado sin recodificar (`-c:v copy`)
- Pistas de audio y subtítulos originales conservados con su códec original
- Subtítulos originales copiados (MKV) u omitidos si son incompatibles (MP4)
- Metadatos globales y capítulos heredados del archivo fuente

## 🛡️ Manejo de errores

- Si el formato elegido falla (códecs incompatibles con MP4), se reintenta automáticamente en MKV.
- Subtítulos gráficos (PGS/DVD) detectados y omitidos si causan conflictos.
- Fallo en la multiplexación → se reintenta automáticamente omitiendo subtítulos originales y cambiando a MKV si era MP4.
- En procesamiento por lotes, un error en un vídeo no detiene el resto de la cola.

## 🎛️ Personalización

- **Ganancia de diálogos:** Editar el valor `gain=2` en `extraccion.py` (línea del filtro `firequalizer`). Subir a `3` o `4` para voces más marcadas.
- **Modelo de transcripción:** Cambiar la variable `modelo` en `transcripcion.py` a `"large-v3"` para máxima precisión (el doble de tiempo).
- **Post‑edición de la traducción:** Añadir un diccionario de localización en `traduccion.py` para adaptar modismos ibéricos a latinos.
- **Precisión numérica:** Para CPUs Intel básicas sin AVX-512 VNNI se usa `float32` por defecto, evitando la sobrecarga del modo `int8`.

## 🔧 Requisitos

- **FFmpeg y FFprobe** (se descargan automáticamente con el script de instalación)
- **Python 3.8+** con `faster-whisper`, `transformers`, `sentencepiece`, `torch`, `tqdm`, `numpy`
- **Windows** (Linux/macOS adaptable)

## ▶️ Cómo ejecutar

```bash
# Activar entorno virtual
source venv/Scripts/activate

# Lanzar la interfaz gráfica
python src/components/interfaz.py
```

También puedes usar el modo texto con `python main.py`.

---

Repositorio creado por [KingEdhard](https://github.com/KingEdhard)  
*"Los subtítulos que tus series y películas favoritas merecen"*

🚀 **Próximas mejoras**
- Selector de modelo Whisper en GUI – Elige entre velocidad (tiny/base) o precisión (large-v3).
- Soporte para más idiomas – Transcripción desde inglés a español, francés, alemán, portugués.
- Ajuste manual de sincronización – Corrige pequeños desfases de subtítulos (± segundos).
- Exportar subtítulos sueltos – Genera solo los archivos .srt sin incrustar en el video.
- Detección automática del idioma del audio – No asumir siempre inglés.
- Modo oscuro en la interfaz – Para trabajar de noche.
- Archivo de correcciones comunitarias – Mejora colaborativa de traducciones.

¿Quieres contribuir? ¡Los pull requests son bienvenidos!

## 📝 Licencia

MIT License (ver archivo LICENSE)

**Español:** Este software es libre y de código abierto. Puedes usarlo, modificarlo y distribuirlo libremente, siempre que mantengas el aviso de copyright original. No hay garantía de ningún tipo.

**English:** This software is free and open source. You may use, modify, and distribute it freely, as long as you retain the original copyright notice. No warranty of any kind.
