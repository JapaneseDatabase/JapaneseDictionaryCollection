import xml.etree.ElementTree as ET
import os

''' Example entry [0]
<entry>
    <ent_seq>1000000</ent_seq>
    <r_ele>
        <reb>ヽ</reb>
    </r_ele>
    <sense>
        <pos>&unc;</pos>
        <xref>一の字点</xref>
        <gloss g_type="expl">repetition mark in katakana</gloss>
    </sense>
</entry>
'''
''' Example entry
<entry>
    <ent_seq>2406710</ent_seq>
    <k_ele>
        <keb>直</keb>
    </k_ele>
    <r_ele>
        <reb>ただ</reb>
    </r_ele>
    <sense>
        <pos>&adj-na;</pos>
        <pos>&n;</pos>
        <pos>&adv;</pos>
        <misc>&arch;</misc>
        <gloss>straight</gloss>
        <gloss>direct</gloss>
    </sense>
</entry>
'''
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
        <!gloss xml:lang='xxx'> # Gloss with language in ISO 639-2 standard
        <!gloss g_gend="#IMPLIED"> # Indicates gender of the gloss in the target language
        <pri> # Highlights particular word in target language strongly associated with entry
        <s_inf> # Sense-information about the entry
'''

def main():
    # Load in data and enter the main xml
    tree = ET.parse(os.path.join('..','data','JMdict_e.xlm'))
    root = tree.getroot()

    # Iterate over each root
    for item in entryIter(root):
        if not isKana(item):
            print(parseNKana(item))
            #break
    #print(curElem)

def entryIter(root):
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

def isKana(entry):
    '''Determines if the entry contains non-Kana elements
    entry - an entry from the xml

    returns False if non-Kana element is present in entry
    '''
    return entry.find("k_ele") is None

def parseNKana(entry):
    '''Parses an entry that has non-Kana elements
    entry - an entry from the xml

    returns
    '''
    wordDict = {}

    # Iterate over non-kana
    # Need to get kanji reading
    for kele in entry.findall('k_ele'):
        word_jp = kele.find('keb').text
        wordDict[word_jp] = {}

    # Iterate over readable
    # Need to get reading
    for rele in entry.findall('r_ele'):
        restrictEle = rele.findall('re_restr')
        if not restrictEle:
            restrictEle = list(wordDict.keys())
        else:
            restrictEle = [restrict.text for restrict in restrictEle]

        pronounce = rele.find('reb').text
        for restrict in restrictEle:
            wordDict[restrict][pronounce] = {'pos':[], 'def':[]}

    # Iterate over sense
    # Need to get definition, part-of-speech
    for sense in entry.findall('sense'):
        stagk = sense.findall("stagk")
        if not stagk:
            stagk = list(wordDict.keys())
        else:
            stagk = [stag.text for stag in stagk]

        stagr = sense.findall("stagr")
        if not stagr:
            stagr = []
            for stag in stagk:
                stagr.extend(pro for pro in list(wordDict[stag].keys()) if pro not in stagr)
        else:
            stagr = [stag.text for stag in stagr]

        define = sense.findall('gloss')
        pos = sense.findall('pos')
        for sk in stagk:
            for sr in stagr:
                if sr in wordDict[sk].keys():
                    wordDict[sk][sr]['def'] = [item.text for item in define]
                    wordDict[sk][sr]['pos'] = [item.text for item in pos]

    return wordDict

#def get

if __name__ == '__main__':
    main()