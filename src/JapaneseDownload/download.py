import gzip
import os
import shutil
import sys

import requests


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

@errorDeco("JMdict")
def loadJMdict():
    ''' Loads the JMdict dataset
    '''
    downloadName = loadDataset('http://ftp.edrdg.org/pub/Nihongo/JMdict_e_examp.gz')
    unzip_gz(downloadName, '.xml')
    os.remove(downloadName)

@errorDeco("KANJIDIC")
def loadKANJIDIC():
    '''Loads the KANJIDICT dataset
    '''
    downloadName = loadDataset('http://www.edrdg.org/kanjidic/kanjidic2.xml.gz')
    unzip_gz(downloadName)
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
        elif data in ['jmdict', 'edict', 'japanese-multilingual', 'japanese-multilingual dictionary']:
            loadJMdict()
        elif data in ['kanjidic']:
            loadKANJIDIC()
        else:
            print("Dataset specificatio needs to be 'all', 'jmdict', or 'kanjidic")
