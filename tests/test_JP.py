import unittest
from os import mkdir, path
from shutil import rmtree

from src.JapaneseDownload.download import loadJMdict, loadKANJIDIC
from src.JapaneseParsers.parseJMdict import parseEntries
from src.JapaneseParsers.parseKANJIDIC import parseCharacter


class testJMdict(unittest.TestCase):
    '''Used to ensure that the JMdict parser works
    '''

    def setUp(self):
        mkdir('data')
        loadJMdict()

    def tearDown(self):
        rmtree('data')

    def test_iterator(self):
        '''Creates the parser opbject, then checks that it can read the first 10 elements
        '''
        try:
            parseObject = parseEntries(path.join('data', 'JMdict_e_examp.xml'))
        except Exception as e:
            print("Unable to load parser")
            raise e
        count = 10
        for x in range(count):
            try:
                next(parseObject)
            except Exception as e:
                print(f"Was only able to load {x}/{count} elements from the parsing")
                raise e

        print("Parser is successful")

    def test_readFirst_nonKana(self):
        '''Reades the first element, which should be non Kana ヽ
        '''
        parseObject = parseEntries(path.join('data', 'JMdict_e_examp.xml'))
        kana, item = next(parseObject)

        print(item)
        print(kana)
        self.assertTrue(kana, "First entry in this dataset is a non-kana element")
        print("Successfully loaded non kana element")

    def test_readFifth_kana(self):
        '''Reads the fifth element, which should be kana 〃
        '''
        parseObject = parseEntries(path.join('data', 'JMdict_e_examp.xml'))
        for count in range(5):
            kana, item = next(parseObject)

        print(item)
        print(kana)
        self.assertFalse(kana, "Fifth entry in this dataset is a kana element")
        print("Successfully loaded kana element")

class testKANJI(unittest.TestCase):
    '''Used to ensure that the KANJI parser works
    '''

    def setUp(self):
        mkdir('data')
        loadKANJIDIC()

    def tearDown(self):
        rmtree('data')

    def test_iterator(self):
        '''Creates the parser opbject, then checks that it can read the first 10 elements
        '''
        try:
            parseObject = parseCharacter(path.join('data', 'kanjidic2.xml'))
        except Exception as e:
            print("Unable to load parser")
            raise e
        count = 10
        for x in range(count):
            try:
                next(parseObject)
            except Exception as e:
                print(f"Was only able to load {x}/{count} elements from the parsing")
                raise e

        print("Parser is successful")

    def test_readFirst(self):
        '''Reades the first element, which should be 亜
        '''
        parseObject = parseCharacter(path.join('data', 'kanjidic2.xml'))
        kanjiItem = next(parseObject)
        print(kanjiItem)
        self.assertEqual(kanjiItem[0], '亜', 'Did not grab the right Kanji. Got {} but expected 亜'.format(kanjiItem[0]))


if __name__ == '__main__':
    unittest.main()
