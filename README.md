# ☁️ SubtitleStudioX – Subtitulado con IA en Google Colab

**SubtitleStudioX** es la versión cloud de [SubtitleStudio](https://github.com), optimizada para ejecutarse **gratis en Google Colab con GPU T4**. Sin instalar nada en tu PC.

🎬 Sube tus vídeos en inglés y obtén subtítulos en español latino con precisión milimétrica usando **WhisperX Large-v3 + alineación fonética Wav2Vec2**.

---

## 🚀 Cómo usar

### 1. Abre un notebook en [Google Colab](https://google.com)

### 2. Copia y pega las celdas del archivo **[`SubtitleStudioX_Colab.ipynb`](https://github.comX/blob/main/SubtitleStudioX_Colab.ipynb)** en tu notebook

### 3. Ejecuta la Celda 1 y espera a que termine

### 4. Ejecuta la Celda 2, sube tus videos y ¡listo!

La Celda 2 incluye un bucle continuo: procesa, pregunta si quieres subir más videos, y repite hasta que decidas salir.

---

## 🔄 Flujo de procesamiento

* 📹 **VIDEO ORIGINAL**
  * ↓
* 🎵 **Extracción de audio optimizada** (VocesClaras-STT)
  * ↓
* 🧠 **WhisperX Large-v3** (Transcripción en inglés)
  * ↓
* 🎯 **Alineación fonética milimétrica** (Wav2Vec2)
  * ↓
* 📝 **Generación de subtítulos SRT** en inglés
  * ↓
* 🌎 **Traducción a español latino** (Modelo personalizado)
  * ↓
* 🎬 **Incrustación de subtítulos** en el video

---

## ⚡ Ventajas


| Característica | Detalle |
|----------------|---------|
| 🆓 **Gratuito** | Cuenta Google + GPU T4 sin costo |
| 🚀 **Velocidad** | 5-10x más rápido que CPU local |
| 🎯 **Precisión** | WhisperX Large-v3 + Wav2Vec2 |
| 📦 **Sin instalación** | Todo en el navegador |
| 🔄 **Procesamiento en lote** | Múltiples videos sin re-ejecutar |

---

## ⚠️ Limitaciones de Colab gratuito


| Recurso | Límite |
|---------|--------|
| Tiempo por sesión | ~4-6 horas |
| GPU | T4 (16 GB VRAM) |
| Almacenamiento | ~100 GB temporal |
| Videos muy largos (>2h) | Usar Colab Pro |

---

## 💻 ¿Prefieres procesar en tu PC?

Usa el proyecto hermano **[SubtitleStudio](https://github.com)** — 100% local, optimizado para CPU, sin límites de tiempo y con interfaz gráfica.

---

## 🛡️ Manejo de errores

- Error de CUDA → La Celda 2 reinstala PyTorch automáticamente
- Video incompatible → Reintenta en MKV automáticamente
- Error en un video → No detiene el resto de la cola
- Sesión terminada → Vuelve a ejecutar ambas celdas

---

## 📝 Licencia

MIT License — Libre uso, modificación y distribución.

---

*"Los subtítulos que tus series y películas favoritas merecen, ahora en la nube"*

Creado por [KingEdhard](https://github.com)
