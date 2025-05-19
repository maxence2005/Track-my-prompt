import importer
import time

audioRecorder = importer.load('AudioRecorder', 'models', 'transcripteur_vocal.py')

audioRecorder = audioRecorder()
print("Start")
audioRecorder.start()
time.sleep(5)
audioRecorder.stop()
print("Stop")
print("Transcription")
print(audioRecorder.transcript())
