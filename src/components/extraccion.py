import subprocess
import json
import os
import tempfile
from src.utils import FFMPEG_PATH, FFPROBE_PATH, DEBUG, input_validado

def obtener_pistas_audio(archivo):
    """Devuelve una lista de pistas de audio con (index, idioma, codec, canales)."""
    cmd = [
        FFPROBE_PATH, '-v', 'error',
        '-select_streams', 'a',
        '-show_entries', 'stream=index,codec_name,channels,channel_layout:stream_tags=language',
        '-of', 'json', archivo.replace('\\', '/')
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if res.returncode != 0 or not res.stdout.strip():
            return []
        datos = json.loads(res.stdout)
        streams = datos.get('streams', [])
        pistas = []
        for s in streams:
            idx = s.get('index')
            codec = s.get('codec_name', '???')
            canales = s.get('channels', 0)
            tags = s.get('tags', {})
            idioma = tags.get('language', 'und').lower()
            pistas.append({
                'index': idx,
                'idioma': idioma,
                'codec': codec,
                'canales': canales,
                'layout': s.get('channel_layout', '')
            })
        return pistas
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error obteniendo pistas: {e}")
        return []

def elegir_pista_ingles(pistas):
    """Selecciona la primera pista en inglés; si no hay, pregunta al usuario."""
    pistas_eng = [p for p in pistas if p['idioma'] in ('eng', 'en', 'english', 'en-us', 'en-gb')]
    if pistas_eng:
        elegida = pistas_eng[0]
        print(f"🔊 Pista de audio en inglés detectada: índice {elegida['index']} ({elegida['codec']}, {elegida['canales']}ch)")
        return elegida['index']
    else:
        print("\n⚠ No se detectó pista en inglés. Pistas disponibles:")
        for p in pistas:
            print(f"   [{p['index']}] Idioma: {p['idioma']}, {p['codec']}, {p['canales']}ch")
        opciones = [str(p['index']) for p in pistas]
        indice = input_validado(
            "👉 Elige el índice de la pista a usar: ",
            opciones_validas=opciones,
            defecto=opciones[0] if opciones else None
        )
        return int(indice)

def extraer_audio_mejorado(archivo_video):
    """
    Extrae la pista de audio en inglés, aplica realce de diálogos y devuelve
    la ruta del WAV temporal listo para Whisper.
    """
    if not os.path.exists(archivo_video):
        print(f"✖ Archivo no encontrado: {archivo_video}")
        return None

    print(f"\n🎬 Analizando audio de: {os.path.basename(archivo_video)}")
    pistas = obtener_pistas_audio(archivo_video)
    if not pistas:
        print("✖ No se encontraron pistas de audio. Proceso cancelado.")
        return None

    idx_audio = elegir_pista_ingles(pistas)

    # Definir archivo temporal de salida (WAV)
    base = os.path.splitext(archivo_video)[0]
    wav_temp = base + "_dialogos_mejorados.wav"
    # Si existe, lo sobrescribimos (ffmpeg -y)
    if os.path.exists(wav_temp):
        os.remove(wav_temp)

    # Filtro de ganancia en diálogos exactamente igual que en tu masterizador
    filtro = "dynaudnorm=f=150:g=31:p=0.95,firequalizer=gain=if(gte(f\\,400)\\,if(lte(f\\,4000)\\,2\\,0)\\,0)"
    
    cmd = [
        FFMPEG_PATH, '-y',
        '-i', archivo_video.replace('\\', '/'),
        '-map', f'0:{idx_audio}',
        '-af', filtro,
        '-ac', '1',          # mono
        '-ar', '16000',      # 16 kHz para Whisper
        '-c:a', 'pcm_s16le',
        wav_temp
    ]
    
    print("\n🔥 Aplicando filtro de ganancia de diálogos...")
    if DEBUG:
        print(f"[DEBUG] Comando: {' '.join(cmd)}")
    
    try:
        resultado = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if resultado.returncode == 0:
            print(f"✔ Audio extraído y mejorado: {wav_temp}")
            return wav_temp
        else:
            print(f"✖ Error al extraer audio. Código: {resultado.returncode}")
            if DEBUG:
                print(resultado.stderr[-1000:])
            return None
    except Exception as e:
        print(f"✖ Excepción ejecutando ffmpeg: {e}")
        return None
