import os
import xml.etree.ElementTree as ET


''' Structure
<entry> # Contains the list of elements
    <ent_seq> # The sequence number of the entry
    <k_ele> # The non-kana elements of the word
        <keb> # The word or short phrase
        <ke_inf> # Information regarding the word
            -ateji "ateji (phonetic) reading"
            -ik "word containing irregular kana usage"
            -iK "word containing irregular kanji usage"
            -io "irregular okurigana usage"
            -oK "word containing out-dated kanji or kanji usage"
            -rK "rarely-used kanji form"
        <ke_pri> # Record information regarding the entry
            -news1 "word frequency in first 12,000 of "wordfreq" by Alexandre Girardi"
            -news2 "word frequency in second 12,000 of "wordfreq" by Alexandre Girardi"
            -ichi1 "appear frequenty in "Ichimango goi bunruishuu", Senmon Kyouiku Publishing, Tokyo, 1998
            -ichi1 "appear infrequenty in "Ichimango goi bunruishuu", Senmon Kyouiku Publishing, Tokyo, 1998
            -spec1/spec2 "common words not included in other lists"
            -gai1/2 "common loanwords, based on the wordfreq file"
            -nfxx "frequency of word in wordfreq file in the xxth set of 500
    <r_ele> # The reading element of the word
        <reb> # The word or short phrase
        <re_nokanji> # Null marker indicating reb is not true reading of kanji [foreign place names, gairaigo, etc]
        <re_restr> # Indicates that <r_ele> only applies to specific <k_ele>
        <re_inf> # Information regarding the word
            -gikun "(meaning as reading) or jukujikun (special kanji reading)"
            -ik "word containing irregular kana usage"
            -ok "out-dated or obsolete kana usage"
            -uK "word usually written using kanji alone"
        <re_pri> # Record information regarding the entry (same as ke_pri)
    <sense> # Translation information of the word
        <stagk> # Indicates that sense is restricted to specified non-kana element
        <stagr> # Indicates that sense is restricted to specified read element
        <xref> # Cross-reference to another entry with similar sense
            -keb
            -reb
            -keb・reb
            -keb・sense number
            -keb・reb・sense number
        <ant> # Cross-reference to another entry that is antonym (same list as <xref>)
        <pos> # Indicates part-of-speech
        <field> # Information regarding field of appliation
        <misc> # Other relevant information about entry
        <lsource> # Information regarding source of the word (if no text, same as gloss)
        <!lsource xlm:lang="xxx"> # lsource with language in ISO 639-2 standard
        <!lsource ls_type="#IMPLIED"> # lsource with indication of how much loanword
            -full [implied] "fully describes the source of the loanword"
            -part "partially describes the source of the loanword"
        <!lsource ls_wasei="#IMPLIED"> # lsource with indication of how Japanese word is constructed from source (example wasei-eigo)
            -n [implied] "is not wasei"
            -y "is wasei"
        <dial> # Indicates regional dialects associated with entry
        <gloss> # Equivalent word or phrase to the entry
        <example> # Stores examples associated with the sense
            <ex_srce exsrc_type="xxx"> # The source number of the sentences from xxx
            <ex_text> # the word (including conjugation) in the example
            <ex_sent xml:lang='xxx'> # The example sentence in the xxx language
        <!gloss xml:lang='xxx'> # Gloss with language in ISO 639-2 standard
        <!gloss g_gend="#IMPLIED"> # Indicates gender of the gloss in the target language
        <pri> # Highlights particular word in target language strongly associated with entry
        <s_inf> # Sense-information about the entry
'''

def main():
    '''Example function for using the functions in this form
    '''
    for kana, item in parseEntries(os.path.join('.', 'data', 'JMdict_e_examp.xml')):
        # Print words with only Kana elements
        if kana:
            for word in item.keys():
                print()
                print(word + ' (' + ','.join(item[word]['part_of_speech']) + '):')
                for defin in item[word]['phrases'].keys():
                    print('\t'+defin)

        # Print words with non-Kana elements
        else:
            for word in item.keys():
                print()
                for pronounce in item[word].keys():
                    print(word + ' [' + pronounce + '] (' + ','.join(item[word][pronounce]['part_of_speech']) + '):')
                    for defin in item[word][pronounce]['phrases'].keys():
                        print('\t'+defin)

# Interpret XML Parts
def getEntryIter(root):
    '''Creates the iterator for the JMdict
    root - the root of the xml

    returns the iterator of entries for the xml
    '''
    return root.iter('entry')

def getSeqNum(entry):
    '''Returns the sequence number of the entry
    entry - an entry from the xml

    returns the sequence number as a string
    '''
    return entry.find('ent_seq').text

def getKEle(k_ele):
    '''Parses everything in the k_ele entry
    k_ele - an k_ele element from the xml

    returns the reading, list of reading information, and list of record information
    '''
    infList = [item.text for item in k_ele.findall('ke_inf')]
    priList = [item.text for item in k_ele.findall('ke_pri')]
    return k_ele.find('keb').text, infList, priList

def getREle(r_ele):
    '''Parses everything in the r_ele entry
    r_ele - an r_ele element from the xml

    returns the reading, if it is the true reading of a kanji, list of nonKana elements it apply to (empty if all),
        list of reading information, list of record information
    '''
    trueKanji = not r_ele.find('re_nokanji')

    restrict = [item.text for item in r_ele.findall('re_restr')]
    infList = [item.text for item in r_ele.findall('re_inf')]
    priList = [item.text for item in r_ele.findall('re_pri')]

    return r_ele.find('reb').text, trueKanji, restrict, infList, priList

def getSense(sense):
    '''Parses everything in the sense entry
    sense - a sense element from the xml

    returns the following:
    list of nonKana elements sense applies to [empty if applied to all in entry]
    list of Kana elements sense applies to [empty if applied to all in entry]
    list of references that are synonyms
    list of references that are antonyms
    list of part-of-speech associated with word
    list of fields where word would be used
    list of miscellaneous information regarding the word
    dictionary regarding the source of the word {source:{lang:lang, type:ls_type, wasei:ls_wasei}}
    list of regional dialects the word is associated with
    dictionary of equivalent english phrases {phrase:{lang:lang, gender:g_gend}}
    list of words in english associated with the entry
    list of sensory information associated with the entry
    list of examples
    '''

    kRestrict = [item.text for item in sense.findall('stagk')]
    rRestrict = [item.text for item in sense.findall('stagr')]
    xref = [item.text.split('・') for item in sense.findall('xref')]
    ant = [item.text.split('・') for item in sense.findall('ant')]
    posList = [item.text for item in sense.findall('pos')]
    fieldList = [item.text for item in sense.findall('field')]
    mscList = [item.text for item in sense.findall('misc')]
    dialList = [item.text for item in sense.findall('dial')]
    priList = [item.text for item in sense.findall('pri')]
    infList = [item.text for item in sense.findall('s_inf')]

    lsourceList = {}
    for item in sense.findall('lsource'):
        lsource = item.text
        lang = item.get('xlm:lang')
        lstype = item.get('ls_type')
        wasei = item.get('ls_wasei')
        lsourceList[lsource] = {'lang': lang, 'type': lstype, 'wasei': wasei}

    glossList = {}
    for item in sense.findall('gloss'):
        gloss = item.text
        lang = item.get('xml:lang')
        gend = item.get('g_gend')
        glossList[gloss] = {'lang': lang, 'gender': gend}

    exampleList = [getExample(item) for item in sense.findall('example')]

    return kRestrict, rRestrict, xref, ant, posList, fieldList, mscList, lsourceList, dialList, glossList, priList, infList, exampleList

def getExample(example):
    '''Parses everything in a sentence example entry
    example - an example entry from the xml

    returns the location of example sentence, form of the word, english example, and japanese example
    '''
    srce = example.find('ex_srce')
    source = [srce.get('exsrc_type'), srce.text]

    eExample = None
    jExample = None
    for item in example.findall('ex_send'):
        if item.get('xml:lang') == 'jpn':
            jExample = item.text
        elif item.get('xml:lang') == 'eng':
            eExample = item.text

    return source, example.find('ex_text').text, eExample, jExample

def isKana(entry):
    '''Determines if the entry contains non-Kana elements
    entry - an entry from the xml

    returns False if non-Kana element is present in entry
    '''
    return entry.find("k_ele") is None

# Parsing Functions
def parseEntries(xlmFile):
    '''Parses all the entries in a JMdict
    xlmFile - the file path for the JMdict file

    yields boolean determine if word is only Kana (True) or not (False)
    yields dictionary for either Kana of non-Kana words
    '''
    # Load in data and enter the main xml
    tree = ET.parse(xlmFile)
    root = tree.getroot()

    # Iterate over each root
    for item in getEntryIter(root):
        if isKana(item):
            yield True, parseKana(item)
        else:
            yield False, parseNKana(item)

def parseNKana(entry):
    '''Parses an entry that has non-Kana elements
    entry - an entry from the xml

    returns a dictionary in the form
        {word: {pronounce: {
            'synonyms', 'antonyms', 'part_of_speech', 'fields', 'info_def',
            'source', 'dialects', 'phrases', 'association', 'sensory', 'examples',
            'info_word', 'record'
        }}}
    '''
    wordDict = {}

    # Iterate over non-kana
    # Need to get kanji reading
    for item in entry.findall('k_ele'):
        word_jp, infList, priList = getKEle(item)
        wordDict[word_jp] = {}

    # Iterate over readable
    # Need to get reading
    for item in entry.findall('r_ele'):
        word_jp, trueKanji, restrict, infList, priList = getREle(item)

        if not restrict:
            restrict = list(wordDict.keys())

        for r in restrict:
            wordDict[r][word_jp] = {
                'synonyms': [], 'antonyms': [], 'part_of_speech': [], 'fields': [], 'info_def': [],
                'source': {}, 'dialects': [], 'phrases': {}, 'association': [], 'sensory': [], 'examples': [],
                'info_word': infList, 'record': priList
            }

    # Iterate over sense
    # Need to get definition, part-of-speech
    for item in entry.findall('sense'):
        kRestrict, rRestrict, xref, ant, posList, fieldList, mscList, lsourceList, \
            dialList, glossList, priList, infList, exampleList = getSense(item)

        if not kRestrict:
            kRestrict = list(wordDict.keys())
        if not rRestrict:
            rRestrict = []
            for stag in kRestrict:
                rRestrict.extend(pro for pro in list(wordDict[stag].keys()) if pro not in rRestrict)

        for kstag in kRestrict:
            for rstag in rRestrict:
                if rstag in wordDict[kstag].keys():
                    wordDict[kstag][rstag]['synonyms'].extend(xref)
                    wordDict[kstag][rstag]['antonyms'].extend(ant)
                    wordDict[kstag][rstag]['part_of_speech'].extend(posList)
                    wordDict[kstag][rstag]['fields'].extend(fieldList)
                    wordDict[kstag][rstag]['info_def'].extend(mscList)
                    wordDict[kstag][rstag]['source'].update(lsourceList)
                    wordDict[kstag][rstag]['dialects'].extend(dialList)
                    wordDict[kstag][rstag]['phrases'].update(glossList)
                    wordDict[kstag][rstag]['association'].extend(priList)
                    wordDict[kstag][rstag]['sensory'].extend(infList)
                    wordDict[kstag][rstag]['examples'].extend(exampleList)

    return wordDict

def parseKana(entry):
    '''Parses an entry that has only Kana elements
    entry - an entry from the xml

    returns a dictionary in the form
        {word: {
            'synonyms', 'antonyms', 'part_of_speech', 'fields', 'info_def',
            'source', 'dialects', 'phrases', 'association', 'sensory', 'examples',
            'info_word', 'record'
        }}}
    '''
    wordDict = {}

    # Iterate over kana
    # Only contains readable
    for item in entry.findall('r_ele'):
        word_jp, _, _, infList, priList = getREle(item)
        wordDict[word_jp] = {
            'synonyms': [], 'antonyms': [], 'part_of_speech': [], 'fields': [], 'info_def': [],
            'source': {}, 'dialects': [], 'phrases': {}, 'association': [], 'sensory': [], 'examples': [],
            'info_word': infList, 'record': priList
        }

    # Iterate over sense
    for item in entry.findall('sense'):
        _, rRestrict, xref, ant, posList, fieldList, mscList, lsourceList, \
            dialList, glossList, priList, infList, exampleList = getSense(item)

        if not rRestrict:
            rRestrict = list(wordDict.keys())

        for rstag in rRestrict:
            wordDict[rstag]['synonyms'].extend(xref)
            wordDict[rstag]['antonyms'].extend(ant)
            wordDict[rstag]['part_of_speech'].extend(posList)
            wordDict[rstag]['fields'].extend(fieldList)
            wordDict[rstag]['info_def'].extend(mscList)
            wordDict[rstag]['source'].update(lsourceList)
            wordDict[rstag]['dialects'].extend(dialList)
            wordDict[rstag]['phrases'].update(glossList)
            wordDict[rstag]['association'].extend(priList)
            wordDict[rstag]['sensory'].extend(infList)
            wordDict[rstag]['examples'].extend(exampleList)

    return wordDict


if __name__ == '__main__':
    main()
