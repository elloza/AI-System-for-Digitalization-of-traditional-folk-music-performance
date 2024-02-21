import datetime
import streamlit as st
import json
from streamlit_player import st_player
from streamlit_pdf_viewer import pdf_viewer

# import util functions
from utils import download_audio_of_video, generate_music_score, split_audio, transcribe_vocals

# Application title
st.title('AI tool for digitalization of traditional folk music performances')

with st.sidebar:
    st.subheader('DIGIFOLK Project')
    st.subheader('About')
    st.markdown('This tools is made with **Streamlit**')

# Video url to process 
url = st.text_input('Enter video URL (vimeo/youtube):')

# Botón para cargar el video
if st.button('Load Video'):
    if url:
        with st.spinner('Cargando video...'):
            # Crear una variable en la sesión para almacenar el estado
            st.session_state['video_loaded'] = True
            st.session_state['video_url'] = url

    else:
        st.error('Por favor, introduce una URL válida.')


# Section to display the video loaded
if st.session_state.get('video_loaded', False):

    st.subheader('Video selected')
    # Get the html code from the session state
    video_url = st.session_state['video_url']
    st_player(video_url)

    st.subheader('Process Video Section')
    # Show a button to process the video
    if st.button('Process Video'):
        # Process the video

        # Display loading message while processing the video
        with st.spinner('Processing video...'):

            # 1 Download the audio of the video to a local folder and get the path
            # function to download the audio video from the url and return the path

            # generate the name of the file with current date and time dd-mm-yyyy-hh-mm-ss
            filename = 'audio'
            print(f'New filename for the audio: {filename}')

            audio_filepath = download_audio_of_video(url=video_url, audio_name=filename)
            print(f'Downloaded video Filepath: {audio_filepath}')

            # Save video path and metadata in the session state 
            st.session_state['video_audio_processed_filepath'] = audio_filepath

        with st.spinner('Splitting audio in vocals and accompaniment..'):

            # 2 Extract the audio from the video and get the path
            # function to extract the audio from the video and return the path
            
            audio_vocals_path, audio_accompaniment_path = split_audio(audio_filepath)
            print(f'Vocals audio Filepath: {audio_vocals_path}')
            print(f'Accompaniment audio Filepath: {audio_accompaniment_path}')

            st.session_state['video_audio_vocals_filepath'] = audio_vocals_path
            st.session_state['video_audio_accompaniment_filepath'] = audio_accompaniment_path
            
        with st.spinner('Transcribing vocals and getting the lyrics...'):
            # 4 Transcribe the vocals and get the lyrics
            # pip install faster_whisper
            # function to transcribe the vocals and return the lyrics
            # Check this for lyrics
            segments, info = transcribe_vocals(audio_vocals_path,st)

            # Segments to full text
            text = ''
            # Complete all the segments with initial and final time segment.start, segment.end
            for segment in segments:
                text += f"[{datetime.timedelta(seconds=segment.start)} -> {datetime.timedelta(seconds=segment.end)}] {segment.text}\n"
            
            st.session_state['video_lyrics'] = text
            st.session_state['video_lyrics_language'] = info.language
            st.session_state['video_lyrics_language_probability'] = info.language_probability
            

            # 5 Generate the music score from the accompaniment, return path to score, path to midi and path to pdf
            # TODO function to generate the music score from the accompaniment

        with st.spinner('Generating music score from accompaniment...This takes a lot of time...⏳ ☕☕ '):

            # Check this for MIDI player https://github.com/andfanilo/streamlit-midi-to-wav/blob/main/app.py

            pdf_path, midi_path, score_path, midi_wav_path = generate_music_score(audio_accompaniment_path)

            # Save the paths in the session state
            st.session_state['video_score_pdf_path'] = pdf_path
            st.session_state['video_score_midi_path'] = midi_path
            st.session_state['video_score_path'] = score_path
            st.session_state['video_score_midi_wav_path'] = midi_wav_path

            # 6 Show the lyrics and the music score
            # TODO show the lyrics and the music score
            st.success('Video procesado con éxito.')

        # Create a variable in the session to store the state
        st.session_state['video_processed'] = True



# Information about the video processed
if st.session_state.get('video_processed', False):

    st.subheader('Downloaded audio')
    # Get the video filepath from the session state
    filepath = st.session_state['video_audio_processed_filepath']
    audio_file = open(filepath, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/wav', start_time=0)

    # Vocals audio
    st.subheader('Vocals audio')
    # Get the video filepath from the session state
    filepath = st.session_state['video_audio_vocals_filepath']
    audio_file = open(filepath, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/wav', start_time=0)

    # Accompaniment audio
    st.subheader('Accompaniment audio')
    # Get the video filepath from the session state
    filepath = st.session_state['video_audio_accompaniment_filepath']
    audio_file = open(filepath, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/wav', start_time=0)

    # Section of lyrics
    st.subheader('Lyrics')
    # Show language and language probability
    st.write(f'Language: {st.session_state["video_lyrics_language"]}')
    st.write(f'Language probability: {st.session_state["video_lyrics_language_probability"]}')

    # Get the lyrics from the session state
    lyrics_text = st.session_state['video_lyrics']
    # Muestra la transcripción en el área de texto
    lyrics = st.text_area('Lyrics:', lyrics_text, height=200)

    # Section for the score PDF with a pdf viewer
    st.subheader('Music Score')
    st.markdown('This is the generate music score for the song')

    # PDF viewer
    # Get the pdf file from the session state
    pdf_file_path = st.session_state['video_score_pdf_path']
    pdf_viewer(pdf_file_path)

    score_path = st.session_state['video_score_path']
    midi_path = st.session_state['video_score_midi_path']

    # MIDI player
    st.subheader('MIDI Audio player')
    st.markdown('This is the audio of the sinthesized MIDI')

    filepath = st.session_state['video_score_midi_wav_path']
    audio_file = open(filepath, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/wav', start_time=0)

    # Section for the score player musicxml js
    st.subheader('Score Player')
    st.markdown('This is the score player for the song')

    # Show Wor in progress message
    st.text('Work in progress section...')

