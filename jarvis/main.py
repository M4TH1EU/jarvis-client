import os
import struct
import threading

import pvporcupine
import pyaudio
import simpleaudio as sa
import speech_recognition as sr

from jarvis.utils import server_utils, config_utils, flask_utils

wake_word_handler = pvporcupine.create(keywords=['jarvis'])


def wake_word_listening():
    pa = pyaudio.PyAudio()

    audio_stream = pa.open(
        rate=wake_word_handler.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=wake_word_handler.frame_length
    )

    while True:
        pcm = audio_stream.read(wake_word_handler.frame_length)
        pcm = struct.unpack_from("h" * wake_word_handler.frame_length, pcm)

        keyword_index = wake_word_handler.process(pcm)

        if keyword_index >= 0:
            threading.Thread(
                target=sa.WaveObject.from_wave_file(os.getcwd() + "/sounds/" + "listening.wav").play).start()
            record()


def record():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source=source, duration=0.7)
        audio = r.listen(source, timeout=2, phrase_time_limit=5)

    threading.Thread(target=sa.WaveObject.from_wave_file(os.getcwd() + "/sounds/" + "listened.wav").play).start()
    server_utils.send_record_to_server(audio.frame_data)


if __name__ == '__main__':
    if config_utils.get_in_config('SERVER_IP') is None:
        print("No server IP specified in config, looking trough the entire network... (might take a few seconds)")
        server_utils.find_server_on_network()

    thread = threading.Thread(target=wake_word_listening).start()

    flask_utils.start_server()
