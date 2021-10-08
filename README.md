# JapaneseDictionaryCollection
When creating the Japanese Database, it is important to collect up-to-date and complete information. The purpose of this repository to provide tools to collect Japanese words from trusted, opensource references.

## Install
This repository is created for python3 >=3.8. The code is currently begin developed in python 3.9, but will likly work in older version. To install, build from the one of the provided sources. For example:

```
pip install Japanese_Dictionary_Collector-__VERSION__-py3-none-any.whl
```

## Using

### Testing
A test functions are provided to ensure that the data could be downloaded and parsed properly. This is done by install and running `pytest`.

These function will temporarily created a data folder to download each of the used datasets. The datasets will be downloaded, have the first few words printed, then the datafolder will be deleted.

## Databases
Data from the following sources are used to created the our data:

### JMdict/EDICT KANJIDIC2 and Japanese/English Dictionary Project
A collection of Japanese-English translations created by Jim Breen and is being managed by the [Electionic Dictionary Research and Development Group (EDRDG)](http://www.edrdg.org/).

The files are available under the [Creative Commons Attribution-ShareAlike Licence (V3.0)](https://creativecommons.org/licenses/by-sa/3.0/legalcode).

The JMdict is a collection of over 170,000 Japanese/English words. KanjiDic is a collection of Kanji including readings, meaning, and metadata. RADKFILE is a database of Kanji and the radicals that make them.
