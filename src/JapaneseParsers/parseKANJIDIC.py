import xml.etree.ElementTree as ET
import os

'''Example
<character>
    <literal>本</literal>
    <codepoint>
        <cp_value cp_type="ucs">672c</cp_value>
        <cp_value cp_type="jis208">43-60</cp_value>
    </codepoint>
    <radical>
        <rad_value rad_type="classical">75</rad_value>
        <rad_value rad_type="nelson_c">2</rad_value>
    </radical>
    <misc>
        <grade>1</grade>
        <stroke_count>5</stroke_count>
        <variant var_type="jis208">52-81</variant>
        <freq>10</freq>
        <jlpt>4</jlpt>
    </misc>
    <dic_number>
        <dic_ref dr_type="nelson_c">96</dic_ref>
        <dic_ref dr_type="nelson_n">2536</dic_ref>
        <dic_ref dr_type="halpern_njecd">3502</dic_ref>
        <dic_ref dr_type="halpern_kkld">2183</dic_ref>
        <dic_ref dr_type="heisig">211</dic_ref>
        <dic_ref dr_type="gakken">15</dic_ref>
        <dic_ref dr_type="oneill_names">212</dic_ref>
        <dic_ref dr_type="oneill_kk">20</dic_ref>
        <dic_ref dr_type="moro" m_vol="6" m_page="0026">14421</dic_ref>
        <dic_ref dr_type="henshall">70</dic_ref>
        <dic_ref dr_type="sh_kk">25</dic_ref>
        <dic_ref dr_type="sakade">45</dic_ref>
        <dic_ref dr_type="jf_cards">61</dic_ref>
        <dic_ref dr_type="henshall3">76</dic_ref>
        <dic_ref dr_type="tutt_cards">47</dic_ref>
        <dic_ref dr_type="crowley">6</dic_ref>
        <dic_ref dr_type="kanji_in_context">37</dic_ref>
        <dic_ref dr_type="busy_people">2.1</dic_ref>
        <dic_ref dr_type="kodansha_compact">1046</dic_ref>
        <dic_ref dr_type="maniette">215</dic_ref>
    </dic_number>
    <query_code>
        <q_code qc_type="skip">4-5-3</q_code>
        <q_code qc_type="sh_desc">0a5.25</q_code>
        <q_code qc_type="four_corner">5023.0</q_code>
        <q_code qc_type="deroo">1855</q_code>
    </query_code>
    <reading_meaning>
        <rmgroup>
            <reading r_type="pinyin">ben3</reading>
            <reading r_type="korean_r">bon</reading>
            <reading r_type="korean_h">본</reading>
            <reading r_type="ja_on">ホン</reading>
            <reading r_type="ja_kun">もと</reading>
            <meaning>book</meaning>
            <meaning>present</meaning>
            <meaning>main</meaning>
            <meaning>true</meaning>
            <meaning>real</meaning>
            <meaning>counter for long cylindrical things</meaning>
            <meaning m_lang="fr">livre</meaning>
            <meaning m_lang="fr">présent</meaning>
            <meaning m_lang="fr">essentiel</meaning>
            <meaning m_lang="fr">origine</meaning>
            <meaning m_lang="fr">principal</meaning>
            <meaning m_lang="fr">réalité</meaning>
            <meaning m_lang="fr">vérité</meaning>
            <meaning m_lang="fr">compteur d'objets allongés</meaning>
            <meaning m_lang="es">libro</meaning>
            <meaning m_lang="es">origen</meaning>
            <meaning m_lang="es">base</meaning>
            <meaning m_lang="es">contador de cosas alargadas</meaning>
            <meaning m_lang="pt">livro</meaning>
            <meaning m_lang="pt">presente</meaning>
            <meaning m_lang="pt">real</meaning>
            <meaning m_lang="pt">verdadeiro</meaning>
            <meaning m_lang="pt">principal</meaning>
            <meaning m_lang="pt">sufixo p/ contagem De coisas longas</meaning>
        </rmgroup>
        <nanori>まと</nanori>
    </reading_meaning>
</character>
'''
'''
<character> # List of elements for a Kanji
    <literal> # The Kanji reading
    <codepoint> # List of encodings used to represent the Kanji character
        <cp_value cp_type="xxx"> # Code number for the xxx Standard
    <radical> # List of radical values for the Kanji
        <rad_value rad_type="xxx"> # Radical number for the xxx radical classification method
    <misc> # Miscellaneous information regarding the kanji
        <grade> # Kanji grade level (1-6 Kyouiku Kanji, 8 Jouyou Kanji, 9 Jinmeiyou, 10 Jinmeiyou and Jouyou variant)
        <stroke_count> # Stroke count for the Kanji (if more than 1, first is accepted/true value)
        <variant var_type="x"> # Cross-reference or alternative indexing for Kanji of variant type xxx
        <freq> # Frequency-of-use ranking for modern Japanese (none if not common)
        <jlpt> # Japanese Language Proficiency test level for the post 2010 test (none if not required)
    <dic_number> # Information regarding the index number from different published dictionaries
        <dic_ref dr_type="xxx"> # Index number for the Kanji in reference xxx
        <!dic_ref dr_type="xxx" m_vol='yyy' m_page='zzz'> # If xxx=='moro', then page and volume are included
    <query_code> # Information regarding glyphs 
        <q_code qc_type="xxx"> # The query-code value in accordance to the type xxx
        <!q_code qc_type="xxx" skip_misclass='yyy'> # Missclassification attribute of type yyy
    <reading_meaning> # Contains all the readings for the Kanji
        <rmgroup> # List of readings and definitions
            <reading r_type="xxx"> # The reading of the Kanji in different languages (important xxx='ja_on','ja_kun')
            <!reading r_type="xxx" on_type='yyy'> # Currently not used
            <!reading r_type="xxx" r_status='yyy'> # Currently not used
            <meaning> # Meaning associated with the Kanji
            <meaning m_lang='xxx'> # Target language of the meaning (assumed en)
        <nanori> # Japanese reading for names
'''

def main():
    '''Example function for using the functions in this form
    '''
    for kanjiItem in parseCharacter(os.path.join('..','data','kanjidic2.xml')):
        print(kanjiItem[0])
        print('\tOnyomi:  ' + ', '.join(kanjiItem[15]))
        print('\tKunyomi: ' + ', '.join(kanjiItem[16]))
        print()


# XML Parts
def getEntryIter(root):
    '''Creates the iterator for the KANJIDIC
    root - the root of the xml

    returns the iterator of entries for the xml
    '''
    return root.iter('character')

def getKanji(character):
    '''Gets the Kanji of the given character
    character - the character entry of the xml

    returns the Kanji text
    '''
    return character.find('literal').text

def getCodePoints(codepoint):
    '''Gets list of encodings to represent the Kanji
    codepoint - a codepoint section for the character in the xml

    returns list of standards and list of code number
    '''
    standList = []
    codeList = []
    for item in codepoint.findall('cp_value'):
        standList.append(item.get('cp_value'))
        codeList.append(item.text)
    return standList, codeList

def getRadicals(radical):
    '''Gets list of radicals to represent the Kanji
    radical - a radical section for the character in the xml

    returns list of radical types and list of radicals
    '''
    typeList = []
    radList = []
    for item in radical.findall('rad_value'):
        typeList.append(item.get('rad_type'))
        radList.append(item.text)
    return typeList, radList

def getMisc(misc):
    '''Gets miscellaneous information regarding the Kanji
    misc - the misc section for the character in the xml

    returns grade level, primary stroke count, list of variants [type,reference], frequency rating, and jlpt level
    '''
    variants = []
    for item in misc.findall('variant'):
        variants.append([item.get("var_type"), item.text])

    grade = misc.find('grade')
    if grade is not None:
        grade = grade.text
    frequency = misc.find('freq')
    if frequency is not None:
        frequency = frequency.text
    jlpt = misc.find('jlpt')
    if jlpt is not None:
        jlpt = jlpt.text

    return grade, misc.find('stroke_count').text, variants, frequency, jlpt

def getDict(dic_number):
    '''Gets dictionary information regarding the Kanji
    dic_number - the dic_number section for the character in the xml

    returns list of dictionary references and list of [index | volumne, page]
    '''
    refList = []
    indList = []
    for item in dic_number.findall("dic_ref"):
        drType = item.get("dr_type")
        if drType == "moro":
            indList.append([drType, item.get("m_vol"), item.get("m_page")])
        else:
            indList.append([drType])
        refList = [item.text]
    return refList, indList

def getQuery(query_code):
    '''Gets informations regarding the glyphs of the Kanji
    query_code - the query_code section for the character in the xml

    returns list of query codes, list of query types, and list of mistaken classifications
    '''
    qCodes = []
    qTypes = []
    qMiscl = []
    for item in query_code.findall('q_code'):
        qCodes.append(item.text)
        qTypes.append(item.get("qc_type"))
        qMiscl.append(item.get("skip_misclass"))
    return qCodes, qTypes, qMiscl

def getRM(reading_meaning):
    '''Gets the readings, meaning, and nanori for the Kanji
    reading_meaning - the reading_meaning section for the character in the xml

    returns list of on readings, list of kun readings, list of meanings, and list of nanoris
    '''
    onList = []
    kunList = []
    meanList = []
    nanoriList = [item.text for item in reading_meaning.findall("nanori")]

    rmgroup = reading_meaning.find("rmgroup")

    for item in rmgroup.findall("reading"):
        if item.get("r_type") == 'ja_on':
            onList.append(item.text)
        elif item.get("r_type") == 'ja_kun':
            kunList.append(item.text)

    for item in rmgroup.findall("meaning"):
        if item.get("m_lang") == 'en':
            meanList.append(item.text)

    return onList, kunList, meanList, nanoriList

# Parsing Functions
def parseCharacter(xmlFile):
    '''Parse a character from the KANJIDIC dataset
    xmlFile - the file location for the KANJIDIC dataset

    yields the following:
    The Kanji
    List of code numbers
    List of standards for the code numbers
    List of radicals
    List of classifications for the radicals
    Grade level
    Stroke count
    List of cross-reference/alternative indexing
    List of sources for the cross-referencing
    Frequency ranking for common, modern Japanese
    JLPT test level (outdated)
    List of references
    List of indexes for the references
    List of query-code glyphs
    List of query-code types corresponding to the glyphs
    List of mistaken query-codes corresponding to the glyphs
    List of on readings
    List of kun readings
    List of meanings in english
    List of nanori
'''
    # Load in data and enter the main xml
    tree = ET.parse(xmlFile)
    root = tree.getroot()

    # Iterate over each root
    for item in getEntryIter(root):
        kanji = getKanji(item)

        codepoint = item.find("codepoint")
        if codepoint:
            standList, codeList = getCodePoints(codepoint)
        else:
            standList, codeList = [], []

        radical = item.find("radical") 
        if radical:
            typeList, radList = getRadicals(radical)
        else:
            typeList, radList = [], []

        misc = item.find("misc")
        if misc:
            grade, stroke, variants, frequency, jlpt = getMisc(misc)
        else:
            grade, stroke, variants, frequency, jlpt = None, None, [], None, None

        dic = item.find("dic_number")
        if dic:
            refList, indList = getDict(dic)
        else:
            refList, indList = [], []

        query = item.find('query_code')
        if query:
            qCodes, qTypes, qMiscl = getQuery(query)
        else:
            qCodes, qTypes, qMiscl = [], [], []

        reading = item.find('reading_meaning')
        if reading:
            onList, kunList, meanList, nanoriList = getRM(reading)
        else:
            onList, kunList, meanList, nanoriList = [], [], [], []

        yield kanji, \
            codeList, standList, \
            radList, typeList, \
            grade, stroke, variants, frequency, jlpt, \
            refList, indList, \
            qCodes, qTypes, qMiscl, \
            onList, kunList, meanList, nanoriList

if __name__ == '__main__':
    main()