Python Assorted code
====================

Miscellaneous Python code snippets and experiments.

Individual files:
* `\change_detector.py`: Given a list of urls fetches their HTML, stores a CRC32 and upon next run will compare stored CRC with new one to see if has changed. Call me lazy ;)
* `\list_search.py`: Search for a command line provided string in all txt files of folder where script is launched. Made for personal use as I keep my catalog of games, movies, etc. in text files. Sample text files format:
```
0   /media/kartones/pre1/test 1/blablabla
123 /media/kartones/pre1/test 1/blablabla2
0   /media/kartones/pre1/test 1
0   /media/kartones/pre1/test 2/blablabla
0   /media/kartones/pre1/test.1/blablabla
```

Folders (see inside for details):
* `\pelican\`: Plugins for the Pelican static site generator tool.
* `\rpg-combat-kata`: A coding kata.
