## File class with utility functions for the app
import os
import subprocess
import shlex
import tempfile
import json
import pathlib
from faster_whisper import WhisperModel


# Youtube-dl template
# CHANGE THIS TO USE youtube-dl in unix
_RETRIEVE_AUDIO_CMD_TEMPLATE = '''youtube-dl -k -f "bestaudio/best" -ciw -x --extractor-retries 4 -v --audio-quality 0 --audio-format wav -o "{audio_name}.wav" {url}'''
# Spleeter deezer template
_SPLIT_AUDIO_CMD_TEMPLATE = '''spleeter separate -p spleeter:2stems -o output {audio_file_path}'''

# Download video from url using youtube-dl
#python -m pip install --no-cache-dir git+https://github.com/yt-dlp/yt-dlp.git@2023.07.06
#ln -s $(which yt-dlp) /usr/local/bin/youtube-dl
# apt-get install -y software-properties-common && sudo apt-get update && apt-get install -y ffmpeg

def download_audio_of_video(url: str, audio_name: str = 'output') -> str:
    """F
    Download a video from a url and return the path
    """

    # Remove audio file if it exists
    audio_file_path = f'{audio_name}.wav'
    if os.path.exists(audio_file_path):
        os.remove(audio_file_path)
    else:
        print("The file does not exist")

    try:
        process = subprocess.run(_RETRIEVE_AUDIO_CMD_TEMPLATE.format(url=url.strip(),audio_name=audio_name), shell=True, check=True, text=True)
        print(process.stdout)  # Imprime la salida estándar
        print(process.stderr)  # Imprime el error estándar

    except subprocess.CalledProcessError as e:
        print(f'Error downloading video: {e.stderr}')
        pass

    print(f"Comand:{_RETRIEVE_AUDIO_CMD_TEMPLATE.format(url=url.strip(),audio_name=audio_name)}")

    """
    if status != 0:
        raise Exception(f'Error downloading video: {stderr}')
    
    """

    print('Downloaded video Filepath: ', f'{audio_name}.wav')
    # return the path to the video

    return f'{audio_name}.wav'


# Function to split audio into vocal and accompaniment
# pip install spleeter
def split_audio(audio_file_path):

    # Get the output directory
    output_dir = os.path.dirname(audio_file_path)

    # Extract file name with extension
    audio_filename_ext = os.path.basename(audio_file_path)
    audio_filename = os.path.splitext(audio_filename_ext)[0]

    try:
        # Execute the command
        print(_SPLIT_AUDIO_CMD_TEMPLATE.format(audio_file_path=audio_file_path))
        process = subprocess.run(_SPLIT_AUDIO_CMD_TEMPLATE.format(audio_file_path=audio_file_path), shell=True, check=True, text=True)
        print(process.stdout)  # Imprime la salida estándar
        print(process.stderr)  # Imprime el error estándar  
    except subprocess.CalledProcessError as e:
        print(f'Error splitting audio: {e.stdout}')
        print(f'Error splitting audio: {e.stderr}')
        pass
    
    # return the paths of the vocal and accompaniment files
    return f'output/{audio_filename}/vocals.wav', f'output/{audio_filename}/accompaniment.wav'


# Function to transcribe the vocals and return the lyrics
def transcribe_vocals(audio_vocals_path):
    # Devolver el resultado
    model_size = "large-v3"

    # Run on GPU with FP16
    #model = WhisperModel(model_size, device="cuda", compute_type="float16")

    # or run on GPU with INT8
    # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    # or run on CPU with INT8
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(audio_vocals_path, beam_size=5)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

    return list(segments), info


def run_cmd_sync(cmd, cwd=None, interactive=False, timeout=None):
    """Runs a console command synchronously and returns the results.

    Parameters
    ----------
    cmd : str
       The command to execute.
    cwd : :class:`pathlib.Path`, optional
       The working directory in which to execute the command.
    interactive : bool, optional
       If set, run command interactively and pipe all output to console.
    timeout : float, optional
       If specified, kills process and throws error after this many seconds.

    Returns
    -------
    int
       Process exit status code.
    str, optional
       Standard output (if not in interactive mode).
    str, optional
       Standard error (if not in interactive mode).

    Raises
    ------
    :class:`FileNotFoundError`
       Unknown command.
    :class:`NotADirectoryError`
       Specified working directory is not a directory.
    :class:`subprocess.TimeoutExpired`
       Specified timeout expired.
    """
    if cmd is None or len(cmd.strip()) == 0:
        raise FileNotFoundError()

    kwargs = {}
    if not interactive:
        kwargs["stdout"] = subprocess.PIPE
        kwargs["stderr"] = subprocess.PIPE

    err = None
    with subprocess.Popen(shlex.split(cmd), cwd=cwd, **kwargs) as p:
        try:
            p_res = p.communicate(timeout=timeout)
        except subprocess.TimeoutExpired as e:
            err = e
        p.kill()

    if err is not None:
        raise err

    result = p.returncode

    if not interactive:
        stdout, stderr = [s.decode("utf-8").strip() for s in p_res]
        result = (result, stdout, stderr)

    return result


# vimeo url to embed url
def convert_vimeo_url_to_embed(url: str) -> str:
    """
    Convert a vimeo url to an embed url
    """
    # Split the url by '/'
    url_split = url.split('/')
    # Get the video id
    video_id = url_split[-1]
    # Return the embed url
    return f'https://player.vimeo.com/video/{video_id}'


# youtube video url to embed url
def convert_youtube_url_to_embed(url: str) -> str:
    """
    Convert a youtube url to an embed url
    """
    # Split the url by '/'
    url_split = url.split('/')
    # Get the video id
    video_id = url_split[-1]
    # Return the embed url
    return f'https://www.youtube.com/embed/{video_id}'


# function to split audio into vocal and accompaniment
# returns the paths of the vocal and accompaniment files
# with the following format: output/audio_filename/vocals.wav
# and output/audio_filename/accompaniment.wav
# This function uses the spleeter library
def split(audio_file_path, output_dir='output'):
    """
    Split an audio file into vocals and accompaniment
    """
    # Extract file name with extension
    audio_filename_ext = os.path.basename(audio_file_path)
    print(audio_filename_ext)
    audio_filename = os.path.splitext(audio_filename_ext)[0]
    print(audio_filename)

    # Execute the command sincronously with os.system
    command = f'spleeter separate -p spleeter:2stems -o {output_dir}/ {audio_file_path}'
    os.system(command)
    return f'{output_dir}/{audio_filename}/vocals.wav', f'{output_dir}/{audio_filename}/accompaniment.wav'




