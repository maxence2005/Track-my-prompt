import unittest
import os

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='*.py', top_level_dir='.')
    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite)
