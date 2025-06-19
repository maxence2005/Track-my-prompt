import threading
import numpy as np
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import io
import time
import tempfile
from pipeline.pipelineTranscription import PipelineTranscription
from PySide6.QtCore import Qt

SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_SIZE = 1024  # nombre d’échantillons par bloc audio

class AudioRecorder:
    def __init__(self, mode):
        self.recording = []
        self._running = False
        self._thread = None
        self._mode = mode
        self.transcription_pipeline = PipelineTranscription()
        self.transcription_result = None
        self.transcription_error = None
        self._transcription_callback = None
        self._transcription_error_callback = None
        self.transcription_pipeline.transcriptionComplete.connect(self._on_transcription_complete)
        self.transcription_pipeline.transcriptionError.connect(self._on_transcription_error)

    def _audio_stream_callback(self, indata, frames, time_info, status):
        if self._running:
            self.recording.append(indata.copy())

    def start(self):
        self.recording = []
        self._running = True
        self._stream = sd.InputStream(samplerate=SAMPLE_RATE,
                                      channels=CHANNELS,
                                      blocksize=BLOCK_SIZE,
                                      callback=self._audio_stream_callback)
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
        if not self.recording:
            if self._transcription_error_callback:
                self._transcription_error_callback("Aucun son détecté. Veuillez réessayer.")
            return False
        return True

    def get_audio_bytesio(self):
        if not self.recording:
            raise ValueError("Aucun bloc audio enregistré")
        audio_np = np.concatenate(self.recording, axis=0)
        buffer = io.BytesIO()
        sf.write(buffer, audio_np, SAMPLE_RATE, format='WAV')
        buffer.seek(0)
        return buffer

    def transcript(self, callback=None, error_callback=None):
        self._transcription_callback = callback
        self._transcription_error_callback = error_callback
        if self._mode == "api":
            try:
                audio_buffer = self.get_audio_bytesio()
            except Exception as e:
                if error_callback:
                    error_callback(str(e))
                return None
            r = sr.Recognizer()
            with sr.AudioFile(audio_buffer) as source:
                audio = r.record(source)
                try:
                    text = r.recognize_google(audio, language="fr-FR")
                    if callback:
                        callback(text)
                    return text
                except sr.UnknownValueError:
                    if callback:
                        callback("")
                    return ""
                except sr.RequestError as e:
                    if error_callback:
                        error_callback("api_error")
                    raise ConnectionError("API Error")
        elif self._mode == "local":
            if not self.recording:
                if error_callback:
                    error_callback("no_sound_detected")
                return None
            self.transcription_result = None
            self.transcription_error = None
            audio_buffer = self.get_audio_bytesio()
            self.transcription_pipeline = PipelineTranscription()
            self.transcription_pipeline.transcriptionComplete.connect(self._on_transcription_complete)
            self.transcription_pipeline.transcriptionError.connect(self._on_transcription_error)
            self.transcription_pipeline.start_transcription(audio_buffer.read())
            return None

    def _on_transcription_complete(self, text):
        self.transcription_result = text
        if self._transcription_callback:
            self._transcription_callback(text)
            self._transcription_callback = None
        self._transcription_error_callback = None

    def _on_transcription_error(self, error):
        self.transcription_error = error
        if self._transcription_error_callback:
            self._transcription_error_callback(error)
            self._transcription_error_callback = None
        self._transcription_callback = None
    
    def set_mode(self, mode):
        self._mode = mode
    
    def get_mode(self):
        return self._mode