import threading
import numpy as np
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import io
import time
import tempfile

SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_SIZE = 1024  # nombre d’échantillons par bloc audio

class AudioRecorder:
    def __init__(self, mode):
        self.recording = []
        self._running = False
        self._thread = None
        self._mode = mode

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
        if self._mode == "api":
            r = sr.Recognizer()
            with sr.AudioFile(audio_buffer) as source:
                audio = r.record(source)
                try:
                    text = r.recognize_google(audio, language="fr-FR")
                    return text
                except sr.UnknownValueError:
                    # On ignore l'exception car celle-ci est levée lorsque l'audio envoyé est vide ce qui esr un comportement normal
                    return ""
                except sr.RequestError as e:
                    raise ConnectionError("API Error")
        elif self._mode == "local":
            try:
                import whisper
                model = whisper.load_model("base", device="cpu") 
                with tempfile.NamedTemporaryFile(suffix=".wav") as tmpfile:
                    tmpfile.write(audio_buffer.read())
                    tmpfile.flush()
                    result = model.transcribe(tmpfile.name)
                return result['text']
            except ImportError:
                raise ImportError("Whisper library is not installed")
            except Exception as e:
                print(e)
                raise RuntimeError(f"An error occurred during transcription: {e}")
    
    def set_mode(self, mode):
        self._mode = mode
    
    def get_mode(self):
        return self._mode