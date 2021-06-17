import os

from src.download import loadJMdict, loadKANJIDIC
from src.parseJMdict import parseEntries
from src.parseKANJIDIC import parseCharacter

TEST_NUM = 10
try:
    os.mkdir("data")
except:
    pass

# Test the JMdict
# Load the Dataset
loadJMdict()

# Print few elements
JMdict_gen = parseEntries(os.path.join("data","JMdict_e_examp.xml"))
for count in range(TEST_NUM):
    isKana, word = next(JMdict_gen)
    if isKana:
        print("Word contains only Kana elements")
    else:
        print("Words does not contain only Kana elements")
    print(word)
    print()

# Delete Dataset
os.remove(os.path.join("data","JMdict_e_examp.xml"))

# Test the KANJIDIC
# Load the Dataset
loadKANJIDIC()

# Print few elements
kanjidic_gen = parseCharacter(os.path.join("data","kanjidic2.xml"))
for count in range(TEST_NUM):
    kanji, _, _, _, _, _, stroke, _, _, jlpt, _, _, _, _, _, onList, kunList, meanList, nanoriList = next(kanjidic_gen)
    print("{} N{} ({} strokes): ".format(kanji, jlpt, stroke) + ", ".join(meanList))
    print('\tOnyomi:  ' + ', '.join(onList))
    print('\tKunyomi: ' + ', '.join(kunList))
    print('\tNanori:  ' + ', '.join(nanoriList))
    print()

# Delete Dataset
os.remove(os.path.join("data","kanjidic2.xml"))

# Cleanup
os.rmdir("data")