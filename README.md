# jarvis-client

Jarvis is a simple voice assistant for home automation and simplifying your life with voice commands. Written in Python,
it uses a lot of open-source libraries like Adapt and Padatious from the Mycroft AI project.

**This is only the client-side of Jarvis, you can download the server [here](https://github.com/M4TH1EU/jarvis-server)
.**

## Languages

It only supports **french** entirely for now, english is actively developed and will soon be available as well as a lot
of others languages like german, spanish and more.

## Compatiblity

The client should work on any platforms from Windows to Linux on ARM devices (raspberry pi 3/4) or x86 computers.

The client handle TTS (Text to Speech) and Wake Word.  
It listens for the wake word (offline of course) and then send what you said after the wake word to the server that will
use Google Speech to Text API *(unfortunately no other API other than Google is good enough imo.)* to convert your
speech to text and then try to execute your request.

## Installation

If not already installed, you will need Python 3.9, you can install it with these commands.

```shell
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt install python3.9 python3.9-dev python3.9-distutils
sudo apt-get install -y python3-dev libasound2-dev # required even if python is already installed
```

### Install requirements

Run the command `python -m pip3 install -r requirements.txt` to install the basic requirements for the project.

### Larynx TTS

Pre-built Debian packages are [available for download](https://github.com/rhasspy/larynx/releases/tag/v0.4.0).

There are three different kinds of packages, so you can install exactly what you want and no more:

* `larynx-tts_<VERSION>_<ARCH>.deb`
    * Base Larynx code and dependencies (always required)
    * `ARCH` is one of `amd64` (most desktops, laptops), `armhf` (32-bit Raspberry Pi), `arm64` (64-bit Raspberry Pi)
* `larynx-tts-lang-<LANG>_<VERSION>_all.deb`
    * Language-specific data files (at least one required)
    * See [above](#docker-installation) for a list of languages
* `larynx-tts-voice-<VOICE>_<VERSION>_all.deb`
    * Voice-specific model files (at least one required)
    * See [samples](#samples) to decide which voice(s) to choose

As an example, let's say you want to use the "harvard-glow_tts" voice for English on an `amd64` laptop for Larynx
version 0.4.0. You would need to download these files:

1. [`larynx-tts_0.4.0_amd64.deb`](https://github.com/rhasspy/larynx/releases/download/v0.4.0/larynx-tts_0.4.0_amd64.deb)
2. [`larynx-tts-lang-en-us_0.4.0_all.deb`](https://github.com/rhasspy/larynx/releases/download/v0.4.0/larynx-tts-lang-en-us_0.4.0_all.deb)
3. [`larynx-tts-voice-en-us-harvard-glow-tts_0.4.0_all.deb`](https://github.com/rhasspy/larynx/releases/download/v0.4.0/larynx-tts-voice-en-us-harvard-glow-tts_0.4.0_all.deb)

Once downloaded, you can install the packages all at once with:

```sh
sudo apt install \
  ./larynx-tts_0.4.0_amd64.deb \
  ./larynx-tts-lang-en-us_0.4.0_all.deb \
  ./larynx-tts-voice-en-us-harvard-glow-tts_0.4.0_all.deb \
  sox
```

You will need to install gruut aswell, follow the instructions [here](https://github.com/rhasspy/gruut#installation)  
*(e.g to install french support do `pip install gruut[fr]`)*

# Errors

Common errors than I personally encoured during this project, hope this can help you.

### Error during installation of PyAudio:

Do the following command `sudo apt-get install portaudio19-dev python-pyaudio`  
*Note: if the package `python-pyaudio` is not found try `python3-pyaudio`*  
[Source](https://ourcodeworld.com/articles/read/974/how-to-solve-installation-error-of-pyaudio-in-ubuntu-18-04-fatal-error-portaudio-h-file-not-found)