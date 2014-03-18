Basque DX1 Generator
====================
Generates a DX1 file given a sample corpus for the Basque language.

Requirements
------------
* Python 3
* [Regex](https://pypi.python.org/pypi/regex)

Generating DX1 Files
--------------------
````
python dx1-generator.py -r ./sources basque.dx1
````

Analysing DX1 Files
-------------------
````
python dx1-phoneme-anlyzer.py basque.dx1 analysis.txt
````

CLI Phonetic Transcription
--------------------------
````
python basque_pronunciation.py word
````
