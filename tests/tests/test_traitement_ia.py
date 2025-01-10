import unittest
import importer
import os
import glob
traitementPrompt = importer.load('traitementPrompt', 'models', 'traitement_ia.py')

class TestTraitementPrompt(unittest.TestCase):
    def test_video(self):
        a = traitementPrompt("https://static.vecteezy.com/system/resources/previews/007/423/086/mp4/4k-looks-at-camera-cutest-little-pomeranian-dog-walking-cute-pet-in-nature-close-up-round-animal-funny-face-in-park-on-sunny-summer-day-free-video.mp4", ["dog"], "video", None)
        self.assertTrue(os.path.exists(a))
        os.remove(a)
        os.chdir(os.path.dirname(__file__))
        for file in glob.glob("../*.mp4"):
            os.remove(file)
    
    def test_image(self):
        a = traitementPrompt("https://images.rawpixel.com/image_png_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIzLTA4L3Jhd3BpeGVsb2ZmaWNlNV9hX3N0dWRpb19zaG90X29mX2RvZ193YXZpbmdfaW1hZ2VzZnVsbF9ib2R5X2lzb185ZGZhMTMwMS0xZTJhLTQ2Y2UtOWM5Yy0yNzFkZDJlM2Y3ZmEucG5n.png", ["dog"], "image", None)
        self.assertTrue(os.path.exists(a))
        os.remove(a)
        os.chdir(os.path.dirname(__file__))
        for file in glob.glob("../*.png"):
            os.remove(file)
        
if __name__ == '__main__':
    unittest.main()