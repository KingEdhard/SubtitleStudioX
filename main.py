import sys
import os
from tqdm import tqdm

from src.components.selector import seleccionar_videos
from src.components.extraccion import extraer_audio_mejorado
from src.components.transcripcion import transcribir_audio
from src.components.traduccion import traducir_srt
from src.components.muxer import incrustar_subtitulos

def main():
    print("\n=== VOCESCLARAS-STT ===")
    print("Subtitulado automático inglés + español latino\n")
    
    # 1. Seleccionar vídeos
    archivos = seleccionar_videos()
    if not archivos:
        print("No se seleccionó ningún vídeo. El programa finalizará.")
        return
    
    total = len(archivos)
    print(f"\n📂 {total} vídeo(s) seleccionado(s). Procesando uno a uno...")
    
    # 2. Procesar cada vídeo
    for i, video in enumerate(archivos, 1):
        print(f"\n{'='*60}")
        print(f"🎬 Procesando vídeo {i} de {total}: {os.path.basename(video)}")
        print('='*60)
        
        try:
            # Extraer y mejorar audio
            wav = extraer_audio_mejorado(video)
            if not wav:
                print(f"⚠ No se pudo extraer el audio de {video}. Pasando al siguiente...")
                continue
            
            # Transcribir a inglés
            srt_ingles = transcribir_audio(wav)
            if not srt_ingles:
                print(f"⚠ Falló la transcripción de {video}. Pasando al siguiente...")
                # Limpiar temporal antes de continuar
                if os.path.exists(wav):
                    os.remove(wav)
                continue
            
            # Traducir a español latino
            srt_espanol = traducir_srt(srt_ingles)
            if not srt_espanol:
                print(f"⚠ Falló la traducción de {video}. El .srt en inglés está a salvo.")
                # No limpiamos wav todavía para debug, pero seguimos con muxer si se desea
            
            # Incrustar subtítulos en nuevo vídeo
            ruta_final = incrustar_subtitulos(video, srt_ingles, srt_espanol if srt_espanol else srt_ingles)
            if ruta_final:
                print(f"🏁 Vídeo {i} completado: {ruta_final}")
            else:
                print(f"⚠ Vídeo {i} sin empaquetar. Los subtítulos se encuentran en:")
                print(f"   - {srt_ingles}")
                if srt_espanol:
                    print(f"   - {srt_espanol}")
            
            # Limpiar el WAV temporal
            if os.path.exists(wav):
                os.remove(wav)
                print(f"🧹 Archivo temporal eliminado: {wav}")
                
        except KeyboardInterrupt:
            print("\n\n⏹ Proceso interrumpido por el usuario.")
            print("Los vídeos ya procesados se conservan.")
            return
        except Exception as e:
            print(f"\n❌ Error inesperado procesando {video}: {e}")
            print("Se continúa con el siguiente vídeo...")
            # Intentar limpiar el temporal si existe
            try:
                if 'wav' in locals() and os.path.exists(wav):
                    os.remove(wav)
            except:
                pass
            continue
    
    print("\n" + "="*60)
    print("✅ PROCESAMIENTO COMPLETADO")
    print("="*60)
    print("Los archivos de subtítulos y vídeos se encuentran en las carpetas de origen.\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n🔥 Error fatal: {e}")
        import traceback
        traceback.print_exc()
    input("\nPresiona Enter para salir...")
