import os


def main():
    '''Example function for using the functions in this form
    '''
    for kanji, radical in parseKRad(os.path.join('..', 'data', 'kradfile')):
        print(kanji)
        print(radical)
        print()

def parseKRad(fileName):
    '''Parses all Kanjis and their radicals in the file
    fileName - file location for the KRAD dataset

    yields the Kanji character
    yields a list of radical characters for the Kanji character'''
    with open(fileName, 'r', encoding='euc-jp') as file:
        for line in file:
            if line[0] != '#':
                kradArray = line.split()
                kanji = kradArray[0]
                radicals = kradArray[2:]
                yield kanji, radicals


if __name__ == '__main__':
    main()
