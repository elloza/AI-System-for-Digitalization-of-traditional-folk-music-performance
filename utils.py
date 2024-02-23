## File class with utility functions for the app
import base64
import os
import subprocess
import shlex
import tempfile
import json
import pathlib
from faster_whisper import WhisperModel
from midi2audio import FluidSynth
import logging
import pathlib
from sheetsage.infer import sheetsage
from sheetsage.utils import engrave
from sheetsage.align import create_beat_to_time_fn
from tqdm import tqdm


logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)


# Youtube-dl template
# Examples: https://gist.github.com/tazihad/030f23a4970c7d1cf1382e69eb1c24ff
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

    # Extract file name with extension
    audio_filename_ext = os.path.basename(audio_file_path)
    audio_filename = os.path.splitext(audio_filename_ext)[0]

    # Remove files in the output directory if they exist
    if os.path.exists(f'output/{audio_filename}/vocals.wav'):
        os.system(f'rm -r output/{audio_filename}/vocals.wav')
        os.system(f'rm -r output/{audio_filename}/accompaniment.wav')
    else:
        print("The file does not exist")

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
# pip install faster-whisper
def transcribe_vocals(audio_vocals_path, st):
    
    # Devolver el resultado
    model_size = "large-v3"
    model = None

    # Check if model is available in st session state
    if 'whisper_model' not in st.session_state:
        # or run on CPU with INT8
        #model = WhisperModel(model_size, device="cpu", compute_type="int8")
        model = WhisperModel(model_size, device="cuda", compute_type="int8_float16",vad_filter=True)
        # Run on GPU with FP16
        #model = WhisperModel(model_size, device="cuda", compute_type="float16")
        
        st.session_state['whisper_model'] = model
    else:
        # Get the model from the session state
        model = st.session_state['whisper_model']

    segments, info = model.transcribe(audio_vocals_path, beam_size=5)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    segments_list = list(segments)

    for segment in segments_list:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

    return segments_list, info

def get_pdf_file_as_base64(pdf_file_path):
        with open(pdf_file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        return base64_pdf

# Function to generate the music score from the accompaniment
def generate_music_score(accompaniment_path):

    USE_JUKEBOX = True
    logging.basicConfig(level=logging.INFO)

    lead_sheet, segment_beats, segment_beats_times = sheetsage(
        accompaniment_path,
        use_jukebox=USE_JUKEBOX,
        measures_per_chunk=4,
        tqdm=tqdm)
    
    # Remove files if they exist
    if os.path.exists('/kaggle/working/output.ly'):
        os.remove('/kaggle/working/output.ly')
    if os.path.exists('/kaggle/working/output.pdf'):
        os.remove('/kaggle/working/output.pdf')
    if os.path.exists('/kaggle/working/output.midi'):
        os.remove('/kaggle/working/output.midi')
    if os.path.exists('/kaggle/working/output_midi.wav'):
        os.remove('/kaggle/working/output_midi.wav')

    # Write lead sheet
    lily = lead_sheet.as_lily(artist="A", title="Titulo")
    with open(pathlib.Path("/kaggle/working/", "output.ly"), "w") as f:
        f.write(lily)

    # Write PDF
    with open(pathlib.Path("/kaggle/working/", "output.pdf"), "wb") as f:
        f.write(
            engrave(
                lily, out_format="pdf", transparent=False, trim=False, hide_footer=False
            )
        )

    # Write MIDI
    with open(pathlib.Path("/kaggle/working/", "output.midi"), "wb") as f:
        f.write(
            lead_sheet.as_midi(
                pulse_to_time_fn=create_beat_to_time_fn(
                    segment_beats, segment_beats_times
                )
            )
        )

    fs = FluidSynth()

    midi_file = '/kaggle/working/output.midi'  # Reemplaza con la ruta de tu archivo MIDI
    wav_file = '/kaggle/working/output_midi.wav'       # Ruta del archivo WAV resultante

    fs.midi_to_audio(midi_file, wav_file)

    path_to_score = "/kaggle/working/output.ly"
    path_to_midi = "/kaggle/working/output.midi"
    path_to_pdf = "/kaggle/working/output.pdf"
    path_to_midi_wav = "/kaggle/working/output_midi.wav"

    return path_to_pdf, path_to_midi, path_to_score, path_to_midi_wav

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
# pip install spleeter
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




