FROM python:3.11

# Establece el directorio de trabajo
WORKDIR /app

COPY reproductor2.py .
COPY config.ini .
COPY add_to_playlist_dark.png .
COPY add_to_playlist.png .
COPY delete_from_playlist_dark.png .
COPY delete_from_playlist.png .
COPY icono.png .
COPY next_dark.png .
COPY next.png .
COPY play_dark.png .
COPY play.png .
COPY previous_dark.png .
COPY previous.png .
COPY stop_dark.png .
COPY stop.png .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV DISPLAY host.docker.internal:0

# Comando para ejecutar tu aplicación
CMD ["python", "reproductor2.py"]
