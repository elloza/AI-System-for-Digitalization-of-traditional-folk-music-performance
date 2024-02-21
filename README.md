# AI-System-for-Digitalization-of-traditional-folk-music-performance
Artificial Intelligence system for digitalization of traditional folk music performances

# Context

Traditional folk music is a cultural heritage that is being lost. The main reason for this is that the music is not being recorded and digitalized. 

Among the task in the digitalization of traditional folk music performances, we can find:

- Transcription of the music to sheet music
- Transcription of the lyrics of the song

This task is usually done by hand, which is a time-consuming and expensive process. The traditional music archives are full of recordings and this is a huge amount of data to be digitalized.

This project aims to create an AI system that can digitalize traditional folk music performances. The system will be able to transcribe the music to sheet music, separate the voice from the instruments, and transcribe the lyrics of the song.


## Description of the system

The system is composed of different parts in order to achieve the digitalization of traditional folk music performances. The system is composed of the following parts:

- Video and audio collection from online sources through an URL of the performance
- Audio separation (voice and instruments): The system will separate the voice from the instruments in the audio of the performance for further analysis and processing.
- Voice to lyrics: The system will transcribe the voice of the performance to lyrics.
- Audio to score transcription: The system will transcribe the audio of the performance to sheet music in xml, midi and pdf format.


<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Main diagram of the system" width="256" height="256">
  </a>
</div>

# Demo notebook

[![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/elloza/ai-tool-for-digitalization-of-traditional-folk-mus)


## Employed utils and models:

### Audio separation (voice and instruments)
<p align="center">
<img src="https://github.com/deezer/spleeter/raw/master/images/spleeter_logo.png" width="99%"/>
</p>
* Spleeter by deezer: https://github.com/deezer/spleeter
  
### Audio to score transcription
<p align="center">
<img src="https://raw.githubusercontent.com/chrisdonahue/sheetsage/main/static/banner.png" width="99%"/>
</p>
* SheetSage: https://github.com/chrisdonahue/sheetsage
  
### Audio (voice) to lyrics
<p align="center">
<img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fdubverse.ai%2Fwp-content%2Fuploads%2F2022%2F09%2FFrame-4-1.png&f=1&nofb=1&ipt=55c089a153af8da8f4daa7b43c7106372295e94f1603711fc307ca6e340a7ffa&ipo=images" height="100px"/>
</p>
* faster-whisper: https://github.com/SYSTRAN/faster-whisper

### Tool

<!-- CITATION -->
### Citation

[![DOI](https://zenodo.org/badge/700259318.svg)](https://zenodo.org/doi/10.5281/zenodo.10659379)

If you find this repo useful in your research, please consider citing:

```
@article{folk-digitalization-tool-2024,
  title={Artificial Intelligence system for digitalization of traditional folk music performances},
  author={Álvaro Lozano Murciego, Diego M. Jiménez Bravo, Daniel Hernández de la Iglesia and Héctor Sánchez San Blas
  journal={},
  volume={},
  number={},
  pages={},
  year={},
  publisher={}
}
```

# About The Project

This repository contains the results of the collaboration between the cultural assosiation [A música portuguesa a gostar dela própria](https://amusicaportuguesaagostardelapropria.org/) and researchers from University of Salamanca, as part of the European project "EA-Digifolk".

<br />
<div align="center">
  <a href="https://github.com/elloza/DIGIFOLK-USAL-ITMA">
    <img src="https://usal.es/files/logo_usal.png" alt="Logo" width="250" height="100" style="margin:10px;padding:20px;">
  </a>
  <a href="https://amusicaportuguesaagostardelapropria.org">
    <img src="https://amusicaportuguesaagostardelapropria.org/wp-content/themes/mpagdp-3/assets/images/header/logo-large.svg" alt="Logo" width="250" height="100" style="margin:10px;padding:20px;">
  </a>
  <a href="https://github.com/elloza/DIGIFOLK-USAL-ITMA">
    <img src="https://cordis.europa.eu/images/logo/logo-ec-es.svg" alt="Logo" width="250" height="100" style="margin:10px;padding:20px;">
  </a>
</div>

# Aknowledgements

We would like to thank the European project "EA-Digifolk" for the support and funding of this research.

We would also like to thank the association [A música portuguesa a gostar dela própria](https://amusicaportuguesaagostardelapropria.org/) for providing the data and the support for this research.
