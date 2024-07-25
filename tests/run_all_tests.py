import unittest
import os

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for root, dirs, files in os.walk(os.path.dirname(__file__)):
        for file in files:
            if file.endswith('_test.py'):
                module_name = os.path.splitext(file)[0]
                module = __import__(module_name)
                suite.addTests(loader.loadTestsFromModule(module))
    return suite

if __name__ == '__main__':
    unittest.main()
