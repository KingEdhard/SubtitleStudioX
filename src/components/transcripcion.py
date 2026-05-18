import os
from tqdm import tqdm
from faster_whisper import WhisperModel

def transcribir_audio(wav_path, modelo="medium", device="cpu", compute_type="float32"):
    """
    Transcribe el WAV a inglés con faster-whisper.
    Optimizado para CPUs Intel básicas sin aceleración int8 (AVX-512 VNNI).
    """
    if not os.path.exists(wav_path):
        print(f"✖ Archivo de audio no encontrado: {wav_path}")
        return None

    print(f"\n📝 Iniciando transcripción (modelo: {modelo}, precisión: {compute_type})...")
    model = WhisperModel(modelo, device=device, compute_type=compute_type)

    with tqdm(desc="Transcribiendo audio", unit=" segmentos") as pbar:
        segments, info = model.transcribe(wav_path, beam_size=5, language="en")
        print(f"   Idioma detectado: {info.language} (probabilidad: {info.language_probability:.2f})")

        base = os.path.splitext(wav_path)[0]
        srt_path = base + "_en.srt"

        total_segmentos = 0
        with open(srt_path, "w", encoding="utf-8") as f:
            for segment in segments:
                start = segment.start
                end = segment.end
                text = segment.text.strip()
                if not text:
                    continue

                def to_hmsm(t):
                    h = int(t // 3600)
                    m = int((t % 3600) // 60)
                    s = int(t % 60)
                    ms = int((t % 1) * 1000)
                    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

                f.write(f"{total_segmentos+1}\n{to_hmsm(start)} --> {to_hmsm(end)}\n{text}\n\n")
                total_segmentos += 1
                pbar.update(1)

        pbar.total = total_segmentos
        pbar.refresh()

    print(f"✔ Subtítulos en inglés generados: {srt_path} ({total_segmentos} segmentos)")
    return srt_path
