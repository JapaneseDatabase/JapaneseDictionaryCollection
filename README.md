# JapaneseDictionaryCollection
When creating the Japanese Database, it is important to collect up-to-date and accurate information. The purpose of this repository to provide tools to collect Japanese words from trusted, opensource references.

## Install
This repository mainly runs in python3. The code is currently begin developed in python 3.9, but will likly work in older version. The required modules can be found in requirements.txt.

```
pip install -r requirements.txt
```

## Using

### Testing
A test function was provided to ensure that the data could be downloaded and parsed properly. To use this function, simply run the following command:

```
python test.py
```

This function will temporarily created a data folder to download each of the used datasets. The datasets will be downloaded, have the first few words printed, then the datafolder will be deleted.

## Databases
Data from the following sources are used to created the our data:

### JMdict/EDICT KANJIDIC2 and Japanese/English Dictionary Project
The goal of that project is to expand on the EDICT Japanese-English dictionary file. The project began in 1991 with the last archive dated on June 2003. The project is led by Jim Breen when it was relocated to the [Electionic Dictionary Research and Development Group](http://www.edrdg.org/).

The files are available under the [Creative Commons Attribution-ShareAlike Licence (V3.0)](https://creativecommons.org/licenses/by-sa/3.0/legalcode).

This publication has included material from the JMdict and KANJIDIC dictionary files in accordance with the licence provisions of the [Electronic Dictionaries Research Group](http://www.edrdg.org/).
