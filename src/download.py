import requests
import gzip
import shutil
import os

def loadDataset(url):
    r = requests.get(url)
    if r.status_code == 200:
        saveName = os.path.join('..','data',url.split('/')[-1])
        open(saveName,'wb').write(r.content)
        return saveName
    else:
        raise Exception("Recieved status code {}".format(r.status_code))

def unzip_gz(saveName,newExtention=''):
    newName = saveName[:-3] + newExtention
    with gzip.open(saveName,'rb') as f_in:
        with open(newName,'wb') as f_out:
            shutil.copyfileobj(f_in,f_out)
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

@errorDeco("JMdict",)
def loadJMdict():
    ''' Loads the JMdict dataset into the current directory
    '''
    downloadName = loadDataset('http://ftp.edrdg.org/pub/Nihongo/JMdict_e.gz')
    unzip_gz(downloadName,'.xlm')
    os.remove(downloadName)

if __name__ == '__main__':
    try:
        os.mkdir(os.path.join("..","data"))
        loadJMdict()
    except FileExistsError:
        conRun = input("File 'data' already exists. Existing files may be overwritten. Continue? [[Y]/n]: ")
        if conRun.lower() in ['n','no']:
            print("Please move/rename 'data' and try again.")
        else:
            loadJMdict()
        