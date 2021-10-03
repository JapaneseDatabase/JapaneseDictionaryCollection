import os


def main():
    '''Example function for using the functions in this form
    '''
    for radical, strokes, kanji in parseRadK(os.path.join('data', 'kradzip', 'radkfilex')):
        print(radical, strokes)
        print(kanji)
        print()

def parseRadK(fileName):
    '''Parses all radicals and Kanji using the radicals in the file
    fileName - file location for the KRAD dataset

    yields the radical character
    yields the stroke count for the radical
    yields a string Kanji character using the radical'''
    currentRadical = ''
    currentStrokes = ''
    currentKanji = ''
    with open(fileName, 'r', encoding='euc-jp') as file:
        for line in file:
            line = line[:-1]
            if line[0] == '#':
                continue
            elif line[0] == '$':
                if currentRadical:
                    yield currentRadical, currentStrokes, currentKanji
                splitLine = line.split()
                currentRadical = splitLine[1]
                currentStrokes = splitLine[2]
                currentKanji = ''
            else:
                currentKanji = currentKanji + line


if __name__ == '__main__':
    main()
