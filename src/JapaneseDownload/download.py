import gzip
import os
import shutil
import sys

import requests

import deprecation
from .__version import __version__


# Utility functions
def loadDataset(url):
    r = requests.get(url)
    if r.status_code == 200:
        saveName = os.path.join('data', url.split('/')[-1])
        open(saveName, 'wb').write(r.content)
        return saveName
    else:
        raise Exception("Recieved status code {}".format(r.status_code))

def unzip_gz(saveName, newExtention=''):
    newName = saveName[:-3] + newExtention
    with gzip.open(saveName, 'rb') as f_in:
        with open(newName, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return newName

def unzip_file(saveName):
    newName = saveName[:-3]
    shutil.unpack_archive(saveName, newName)
    return newName

def errorDeco(name):
    def deco(func):
        def wrapper():
            try:
                print("Attempting to load the {}".format(name))
                func()
                print("Successfully loaded {}".format(name))
            except Exception as e:
                print(e)
                print("Unable to load {}".format(name))
        return wrapper
    return deco

# Extraction Functions
@errorDeco("JMdict")
def loadJMdict():
    ''' Loads the JMdict dataset as JMdict_e_examp.xml
    '''
    downloadName = loadDataset('http://ftp.edrdg.org/pub/Nihongo/JMdict_e_examp.gz')
    unzip_gz(downloadName, '.xml')
    os.remove(downloadName)

@errorDeco("KANJIDIC")
def loadKANJIDIC():
    '''Loads the KANJIDICT dataset as kanjidic2.xml
    '''
    downloadName = loadDataset('http://www.edrdg.org/kanjidic/kanjidic2.xml.gz')
    unzip_gz(downloadName)
    os.remove(downloadName)

@deprecation.deprecated(deprecated_in="0.0",
                        current_version=__version__,
                        details="Use Radicals instead")
@errorDeco("RADKFILE")
def loadRADKFILE():
    '''Loads the RADKFILE dataset as radkfile
    '''
    downloadName = loadDataset('http://ftp.usf.edu/pub/ftp.monash.edu.au/pub/nihongo/radkfile.gz')
    unzip_gz(downloadName)
    os.remove(downloadName)

@deprecation.deprecated(deprecated_in="0.0", removed_in="1.0",
                        current_version=__version__,
                        details="Use Radicals instead")
@errorDeco("KRADFILE")
def loadKRADFILE():
    '''Loads the KRADFILE dataset as kradfile
    '''
    downloadName = loadDataset('http://ftp.usf.edu/pub/ftp.monash.edu.au/pub/nihongo/kradfile.gz')
    unzip_gz(downloadName)
    os.remove(downloadName)

@errorDeco("RADFILE")
def loadRadicals():
    '''Loads the KRAD and RADK datasets as kradfile, kradfile2, and radkfilex in the kradzip folder
    '''
    downloadName = loadDataset('http://ftp.edrdg.org/pub/Nihongo/kradzip.zip')
    unzip_file(downloadName)
    os.remove(downloadName)


if __name__ == '__main__':
    running = True
    try:
        os.mkdir(os.path.join("data"))
    except FileExistsError:
        conRun = input("File 'data' already exists. Existing files may be overwritten. Continue? [[Y]/n]: ")
        if conRun.lower() in ['n', 'no']:
            print("Please move/rename 'data' and try again.")
            running = False

    if running:
        try:
            data = sys.argv[1].lower()
        except Exception as e:
            print(e)
            print("Dataset not specified, so install all")
            data = 'all'

        if data in ['all', 'a']:
            loadJMdict()
            loadKANJIDIC()
            loadRadicals()
        elif data in ['jmdict', 'edict', 'japanese-multilingual', 'japanese-multilingual dictionary']:
            loadJMdict()
        elif data in ['kanjidic']:
            loadKANJIDIC()
        elif data in ['radkfile']:
            loadRADKFILE()
        elif data in ['kradfile']:
            loadKRADFILE()
        elif data in ['radical']:
            loadRadicals()
        else:
            print("Dataset specificatio needs to be 'all', 'jmdict', 'kanjidic', 'radkfile', or 'kradfile'")
