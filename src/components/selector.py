import tkinter as tk
from tkinter import filedialog

EXTENSIONES_VIDEO = (
    ".mkv", ".mp4", ".avi", ".mov", ".wmv", ".flv", ".webm",
    ".ts", ".m2ts", ".mts", ".m4v", ".mpg", ".mpeg", ".vob",
    ".evo", ".ogv", ".ogm", ".divx", ".xvid"
)

def seleccionar_videos():
    """Abre un diálogo para elegir uno o varios vídeos y devuelve una lista de rutas."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    filetypes = [
        ("Archivos de video", "*.mkv *.mp4 *.avi *.mov *.wmv *.flv *.webm *.ts *.m2ts *.mts *.m4v *.mpg *.mpeg *.vob"),
        ("Todos los archivos", "*.*")
    ]

    archivos = []
    try:
        archivos = list(
            filedialog.askopenfilenames(
                title="Selecciona uno o varios vídeos para subtitular",
                filetypes=filetypes
            )
        )
    finally:
        try:
            root.destroy()
        except:
            pass

    return archivos
