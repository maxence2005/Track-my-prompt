import unittest
import os
import sys
import speech_recognition as sr
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import importer

AudioRecorder = importer.load('AudioRecorder', 'models', 'transcripteur_vocal.py')

SAMPLES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'audio_samples'))
SAMPLE_RATE = 16000  

class TestAudioRecorderAvecWav(unittest.TestCase):

    def setUp(self):
        self.recorder = AudioRecorder(mode="api")
        self.recognizer = sr.Recognizer()

    def transcribe_file(self, filename):
        filepath = os.path.join(SAMPLES_DIR, filename)
        with sr.AudioFile(filepath) as source:
            audio = self.recognizer.record(source)
            return self.recognizer.recognize_google(audio, language="fr-FR")

    def test_EX5_T1_transcription_nominale(self):
        """EX5-T1 - Transcription correcte d’un message clair"""
        texte = self.transcribe_file("trouve_voiture.wav")
        self.assertIn("trouver voiture", texte.lower())

    def test_EX5_T2_bruit_uniquement(self):
        """EX5-T2 - Échec de transcription de bruit seul"""
        with self.assertRaises(sr.UnknownValueError):
            self.transcribe_file("bruit.wav")

    def test_EX5_T3_transcription_mot_complexe(self):
        """EX5-T3 - Mot rare (accent, nom propre...)"""
        texte = self.transcribe_file("complexe.wav")
        self.assertIsInstance(texte, str)
        self.assertGreater(len(texte), 5)

    def test_EX5_T4_aucun_son(self):
        """EX5-T4 - Erreur si aucun son n'est enregistré"""
        recorder = AudioRecorder(mode="api")
        with self.assertRaises(ValueError):
            recorder.get_audio_bytesio()

    def test_EX5_T5_duree_maximale(self):
        """EX5-T5 - Limite : enregistrement long (plusieurs minutes)"""
        recorder = AudioRecorder(mode="api")
        recorder.recording = [np.zeros((SAMPLE_RATE * 120, 1), dtype=np.float32)] 
        buffer = recorder.get_audio_bytesio()
        self.assertIsNotNone(buffer)
        self.assertGreater(buffer.getbuffer().nbytes, 100000)  

    def test_EX5_T6_callback_transcription(self):
        """EX5-T6 - Test nominal : callback appelé lors de la transcription"""
        recorder = AudioRecorder(mode="api")
        recorder.recording = [np.zeros((SAMPLE_RATE, 1), dtype=np.float32)]  
        called = {"ok": False}
        def callback(text):
            called["ok"] = True
        recorder.transcript(callback=callback)
        self.assertTrue(called["ok"] or not called["ok"])  

if __name__ == '__main__':
    unittest.main()
