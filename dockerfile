# Base image docker pull nvidia/cuda:12.2.0-base-ubuntu20.04
FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04

# Set environment variable to avoid tzdata prompt
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Update system
# Instala dependencias básicas del sistema
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    git

# Instala dependencias de python
RUN pip3 install --upgrade pip
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install matplotlib
RUN pip3 install seaborn
RUN pip3 install scikit-learn

# APP LIBRARIES
RUN pip3 install streamlit -q
RUN pip3 install streamlit_player
RUN pip3 install streamlit-pdf-viewer
RUN pip3 install midi-player

# LIBRARIES FOR DOWNLOADING YOUTUBE VIMEO FILES

RUN apt-get install -y wget
RUN apt-get install -y curl
RUN apt-get install -y software-properties-common && apt-get update -y -q && apt-get install -y ffmpeg
RUN python3 -m pip install --no-cache-dir git+https://github.com/yt-dlp/yt-dlp.git@2024.05.27

RUN ln -s $(which yt-dlp) /usr/local/bin/youtube-dl

# INSTALL SPLEETER
RUN pip3 install spleeter

# INSTALL FASTER-WHISPER
RUN pip3 install git+https://github.com/trungkienbkhn/faster-whisper.git@improve-language-detection

# Instala Jukebox
RUN python3 -m pip install --no-cache-dir torch==1.12.0+cu113 --extra-index-url https://download.pytorch.org/whl/cu113 && \
    python3 -m pip install --no-cache-dir numba==0.58.1 && \
    python3 -m pip install --no-cache-dir resampy==0.2.2 && \
    python3 -m pip install --no-cache-dir librosa==0.10.1

RUN apt-get install -y libopenmpi-dev openssh-server git && \
    python3 -m pip install --no-cache-dir mpi4py==3.1.5 && \
    python3 -m pip install --no-cache-dir git+https://github.com/XaryLee/jukebox.git@ddc3577b50a4085be0ef65e17e9863686dadef40 && \
    python3 -m pip install --no-cache-dir requests==2.26.0

# Instala pretty_midi
RUN apt-get install -y fluidsynth && \
    python3 -m pip install --no-cache-dir pyFluidSynth==1.3.0 && \
    python3 -m pip install --no-cache-dir pretty_midi==0.2.9

# Instala madmom
RUN python3 -m pip install --no-cache-dir Cython==0.29.24 && \
    python3 -m pip install --no-cache-dir git+https://github.com/XaryLee/madmom.git

# Instala lilypond
RUN apt-get install -y lilypond

# Instala mir_eval
RUN python3 -m pip install --no-cache-dir mir_eval==0.7

# Instala validators
RUN python3 -m pip install --no-cache-dir validators==0.20.0

# Instala Flask
RUN python3 -m pip install --no-cache-dir requests==2.26.0 && \
    python3 -m pip install --no-cache-dir Flask==2.0.3 && \
    python3 -m pip install --no-cache-dir Flask-Cors==3.0.10

# Instalar 
RUN python3 -m pip install --upgrade requests
RUN pip3 install protobuf==3.20.3

# Actualiza requests
RUN python3 -m pip install --upgrade requests

# Instala protobuf versión 3.20.3
RUN pip install protobuf==3.20.3

# Instala FluidSynth
RUN apt-get install -y fluidsynth

# Instala midi2audio para usar FluidSynth en Python
RUN pip install midi2audio

# Establece el directorio de trabajo al home del usuario
WORKDIR /root

# Añadir instalación de npm para proporcionar npx
RUN apt-get install -y npm

# Crear una carpeta para el código
# Clona el repositorio sheetsage
RUN git clone https://github.com/elloza/sheetsage.git

# Establece el directorio de trabajo a sheetsage (ajustado al path correcto tras clonar)
WORKDIR /root/sheetsage

# Instala el paquete en el modo editable
RUN python3 -m pip install --no-cache-dir -e .

# Establece la variable de entorno SHEETSAGE_CACHE_DIR
ENV SHEETSAGE_CACHE_DIR /root/.cache

# Verifica la variable de entorno (opcional, para propósitos de debugging)
RUN echo $SHEETSAGE_CACHE_DIR

# Instala aria2 para descargar assets
RUN apt-get install -y -qq aria2

# Crea los directorios necesarios y descarga los archivos usando aria2
RUN mkdir -p /root/.cache/sheetsage/v0.2/0919_02_e0908_oafmelspecnorm && \
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M -d /root/.cache/sheetsage/v0.2/0919_02_e0908_oafmelspecnorm -o 5b739ce5efa2b6d4d70c5f1feac802684f0ee6f4.cfg.json https://sheetsage.s3.amazonaws.com/sheetsage/v0.2/0919_02_e0908_oafmelspecnorm/5b739ce5efa2b6d4d70c5f1feac802684f0ee6f4.cfg.json && \
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M -d /root/.cache/sheetsage/v0.2/0919_02_e0908_oafmelspecnorm -o model.pt https://sheetsage.s3.amazonaws.com/sheetsage/v0.2/0919_02_e0908_oafmelspecnorm/model.pt && \
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M -d /root/.cache/sheetsage/v0.2/0919_02_e0908_oafmelspecnorm -o step.pkl https://sheetsage.s3.amazonaws.com/sheetsage/v0.2/0919_02_e0908_oafmelspecnorm/step.pkl

RUN mkdir -p /root/.cache/sheetsage/v0.2/0919_00_e0830_oafmelspecnorm && \
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M -d /root/.cache/sheetsage/v0.2/0919_00_e0830_oafmelspecnorm -o 7d82e6839e582936ea428a823a0d868075a52dc5.cfg.json https://sheetsage.s3.amazonaws.com/sheetsage/v0.2/0919_00_e0830_oafmelspecnorm/7d82e6839e582936ea428a823a0d868075a52dc5.cfg.json && \
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M -d /root/.cache/sheetsage/v0.2/0919_00_e0830_oafmelspecnorm -o model.pt https://sheetsage.s3.amazonaws.com/sheetsage/v0.2/0919_00_e0830_oafmelspecnorm/model.pt && \
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M -d /root/.cache/sheetsage/v0.2/0919_00_e0830_oafmelspecnorm -o step.pkl https://sheetsage.s3.amazonaws.com/sheetsage/v0.2/0919_00_e0830_oafmelspecnorm/step.pkl

RUN mkdir -p /root/.cache/sheetsage/v0.2 && \
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M -d /root/.cache/sheetsage/v0.2 -o oafmelspec_moments.npy https://sheetsage.s3.amazonaws.com/sheetsage/v0.2/oafmelspec_moments.npy

RUN mkdir -p /root/.cache/jukebox/models/5b && \
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M -d /root/.cache/jukebox/models/5b -o prior_level_2.pth.tar https://openaipublic.azureedge.net/jukebox/models/5b/prior_level_2.pth.tar

# Verifica los assets de sheetsage
RUN python3 -m sheetsage.assets SHEETSAGE_V02_HANDCRAFTED && \
python3 -m sheetsage.assets JUKEBOX && \
python3 -m sheetsage.assets SHEETSAGE_V02_JUKEBOX

# Add a build argument for cache busting
ARG CACHEBUST=1

WORKDIR /root
RUN git clone https://github.com/elloza/AI-System-for-Digitalization-of-traditional-folk-music-performance.git
WORKDIR /root/AI-System-for-Digitalization-of-traditional-folk-music-performance

RUN npm cache clean --force

CMD ["streamlit", "run", "/root/AI-System-for-Digitalization-of-traditional-folk-music-performance/app.py", "--server.port", "8502"]

# Exponer el puerto 8502
EXPOSE 8502