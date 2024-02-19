## File class with utility functions for the app
import os

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




