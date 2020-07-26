Python Assorted code
====================

Miscellaneous Python code snippets and experiments.

## Running

```
make shell
```

And then from inside the Python 3.7 container install and run whatever you want.

**Note**: Only basic `python 3.7`, `pytest` and `flake8` are installed.


### Miscellaneous
* `\double-linked-list`: A Python implementation of a double linked list, with sorting, reversing, item flipping and inserting at specific position (by data).
* `\list_search.py`: Old search prototype for a command-line provided string in all txt files of folder where script is launched. Sample text files format:
```
0   /media/kartones/pre1/test 1/blablabla
123 /media/kartones/pre1/test 1/blablabla2
0   /media/kartones/pre1/test 1
0   /media/kartones/pre1/test 2/blablabla
0   /media/kartones/pre1/test.1/blablabla
```
* `\pelican\plugins`: Some plugins for the Pelican static site generator tool I've built.
* `\pelican\blogengine_to_pelican.py`: Tool to migrate from BlogEngine.Net to Pelican (posts and pages).
* `\pelican\publisher`: Tool to allow post-processing of Pelican builds and optionally upload a post via FTP.
* `\shopping-cart-with-discounts`: Tiny implementation of a shopping cart with an extensible discounts system.
* `\shopping-lists`: A pet project to easily manage shopping lists. Mobile-friendly although nothing too complex nor feature-full. See its README for more details.
* `\trello-backup`: Script to export your trello boards as json files, plus all attachments. One folder per board with data inside.
* `\twitter-purge`: Script to delete your tweets older than X days (5 with sample config). Best setup as a cron job to run hourly or daily.
* `\weather-email`: **(No longer works)** Small script that fetches Madrid's current weather info and sends it via email. Perfect to be setup as a cron job at 7AM to remind me daily of the weather before I head out for work.

### Games & Gaming Related

* `\barnsley_fern.py`:  A [Barnsley Fern fractal](https://en.wikipedia.org/wiki/Barnsley_fern) implementation using Pygame for the graphics.

![Barnsley Fern fractal](https://images.kartones.net/posts/kartonesblog/barnsley_fern.jpg)

* `\game-of-life-kata`: A coding kata. Inside-out TDD approach + PyGame "visualizer":

![sample game of life run](game-of-life-kata/doc/python_game_of_life_sample.gif)

* `\fire-effect.py`: Python/Pygame implementation of Doom PSX fire effect:

![Doom PSX fire effect in pygame](doc/fire-effect.png)

* `\flappy-kirby`: Pygame Zero Flappy Bird game clone (with some classic graphics).

* `\pic-to-png`: Exporter from Oper Soft's old MS-DOS games .PIC files to .PNG images. More info at [this blogpost](https://blog.kartones.net/post/opera-soft-pic-to-png-exporter/) & [part 2](https://blog.kartones.net/post/mutan-zone-sprite-exporter-wip/):

![Mutan Zone main screen](doc/pic_2_png_mutan_zone.png) ![Abadia del Crimen main screen](doc/pic_2_png_abadia_del_crimen.png)

* `\rpg-combat-kata`: A coding kata. I went for an inside-out TDD approach, building only the minimal needed functionality.

* `\transarctica-battles`: A prototype of re-imagining of the battles section of the MS-DOS and AMIGA game [Transarctica](https://en.wikipedia.org/wiki/Transarctica). Also an experiment with Pygame to learn about screen resizing. Totally WIP.

![Transarctica Battles](doc/transarctica-battles.png)