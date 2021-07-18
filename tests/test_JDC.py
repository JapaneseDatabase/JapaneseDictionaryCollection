import unittest
from os import mkdir
from shutil import rmtree

from src.JapaneseDownload.download import loadJMdict, loadKANJIDIC


class downloadTests(unittest.TestCase):
    '''Used to ensure that the datasets can be downloaded
    '''

    def setUp(self):
        mkdir('data')

    def tearDown(self):
        rmtree('data')

    def test_JMLoad(self):
        '''Tests that the JMdict dataset can be loaded properly
        '''
        try:
            loadJMdict()
            print("Successfully downloaded the JMdict dataset")
        except Exception as e:
            print("Was unsuccessful loading JMdict")
            raise e

    def test_KANJILoad(self):
        '''Tests that the KANJI dataset can be loaded properly
        '''
        try:
            loadKANJIDIC()
            print("Successfully downloaded the KANJI dataset")
        except Exception as e:
            print("Was unsuccessful loading KANJI")
            raise e


if __name__ == '__main__':
    unittest.main()
