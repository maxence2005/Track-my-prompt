import threading
import numpy as np
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import io
import time

SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_SIZE = 1024  # nombre d’échantillons par bloc audio

class AudioRecorder:
    def __init__(self):
        self.recording = []
        self._running = False
        self._thread = None

    def _callback(self, indata, frames, time_info, status):
        if self._running:
            self.recording.append(indata.copy())

    def start(self):
        self.recording = []
        self._running = True
        self._stream = sd.InputStream(samplerate=SAMPLE_RATE,
                                      channels=CHANNELS,
                                      blocksize=BLOCK_SIZE,
                                      callback=self._callback)
        self._stream.start()
        self._thread = threading.Thread(target=self._monitor)
        self._thread.start()

    def _monitor(self):
        while self._running:
            time.sleep(0.1)

    def stop(self):
        self._running = False
        self._stream.stop()
        self._stream.close()
        self._thread.join()

    def get_audio_bytesio(self):
        audio_np = np.concatenate(self.recording, axis=0)
        buffer = io.BytesIO()
        sf.write(buffer, audio_np, SAMPLE_RATE, format='WAV')
        buffer.seek(0)
        return buffer

    def transcript(self):
        audio_buffer = self.get_audio_bytesio()
        r = sr.Recognizer()
        with sr.AudioFile(audio_buffer) as source:
            audio = r.record(source)
            try:
                text = r.recognize_google(audio, language="fr-FR")
                return text
            except sr.UnknownValueError:
                raise ValueError("Audio Error")
            except sr.RequestError as e:
                raise ConnectionError("API Error")
            
