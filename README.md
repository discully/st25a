# 25ani

Python tools for extracting and converting files from the game Star Trek: 25th Anniversary.

There are three applications:
* st25a_index.py - Prints an index of files from the game
* st25a_dump.py - Exports files from the game in their raw data form
* st25a_export.py - Exports data files from the game into modern file formats

Each requires you to privde the path to your installation directory,
which contains the files `DATA.001` and `DATA.DIR`.


# st25a_index.py

The `st25a_index.py` utility prints the index of files within the game.

```sh
python3 st25a_index.py -d /path/to/install
```

Optionally, you can provide a search string which filters file names which match the string provided.

```sh
python3 st25a_index.py -d /path/to/install -s KIRK
```


# st25a_dump.py

The `st25a_dump.py` utility dumps any file from the game in its raw binary format.
For example, the following will create the file IKIRK.BMP:

```sh
python3 st25a_dump.py -d /path/to/install -f IKIRK.BMP
```


# st25a_export.py

The `st25a_export.py` utility will export some of the files into modern formats.
For example, the following will create the file IKIRK.BMP.png:

```sh
python3 st25a_export.py -d /path/to/install -f IKIRK.BMP
```

Currently, the utiliyt supports the ".ANM", ".BMP", ".DB", ".KEY", ".PAL", and ".TXT" files.


# File Types

* AD
* ADV
* ANM - Animation file (describes a sprite)
* BAN
* BM
* BMP - Bitmap image
* DAT
* DB  - Database entry (essentially just a text file)
* DSC
* EGA
* FNT
* IW
* KEY - Index of the 'DB' database files
* LUT
* MAP
* MNU
* MT
* PAL - Colour palette (all BMPs use 'PALETTE.PAL', except 'BRIDGE.BMP' and 'GOLDLOGO.BMP')
* PC
* PRI
* R3S
* RDF
* SDT
* SHP
* TD
* TXT - Text files
* XOR - Sprite image files, described as a xor-diff on the McCoy 'BMP' sprite images


# Thanks

I mostly figured this out on my own, but did sneak a peek at the
[SCUMMVM startrek engine](https://github.com/Vahti/scummvm-startrek)
by Drenn1 and clone2727.
