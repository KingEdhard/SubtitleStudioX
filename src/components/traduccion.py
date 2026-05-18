import re
import os
from tqdm import tqdm
from transformers import MarianMTModel, MarianTokenizer

def traducir_srt(srt_ingles, progress_callback=None):
    """
    Traduce el archivo .srt de inglés a español latino.
    Si se proporciona progress_callback, se llamará con (current, total) en cada segmento.
    """
    if not srt_ingles or not os.path.exists(srt_ingles):
        print(f"✖ Archivo .srt no encontrado: {srt_ingles}")
        return None

    print("\n🌎 Cargando modelo de traducción inglés → español...")
    modelo = "Helsinki-NLP/opus-mt-en-es"
    tokenizer = MarianTokenizer.from_pretrained(modelo)
    model = MarianMTModel.from_pretrained(modelo)

    with open(srt_ingles, "r", encoding="utf-8") as f:
        contenido = f.read()

    bloques = re.split(r'\n\n+', contenido.strip())
    if not bloques:
        print("✖ No se encontraron bloques en el .srt.")
        return None

    print(f"   Traduciendo {len(bloques)} segmentos...")

    base = os.path.splitext(srt_ingles)[0]
    srt_espanol = base.replace('_en', '_es') + ".srt"

    with open(srt_espanol, "w", encoding="utf-8") as out:
        for i, bloque in enumerate(tqdm(bloques, desc="Traduciendo segmentos"), 1):
            lineas = bloque.strip().split('\n')
            if len(lineas) < 3:
                continue

            indice = lineas[0]
            tiempos = lineas[1]
            texto = '\n'.join(lineas[2:])

            try:
                translated = model.generate(
                    **tokenizer(texto, return_tensors="pt", padding=True)
                )
                texto_es = tokenizer.decode(translated[0], skip_special_tokens=True)
            except Exception as e:
                print(f"\n⚠ Error traduciendo bloque {indice}: {e}")
                texto_es = texto

            out.write(f"{indice}\n{tiempos}\n{texto_es}\n\n")
            if progress_callback:
                progress_callback(i, len(bloques))

    print(f"✔ Subtítulos en español generados: {srt_espanol}")
    return srt_espanol
