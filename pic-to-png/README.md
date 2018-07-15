# Opera Soft's PIC to PNG exporter

## Intro

Converts from [Opera Soft](https://en.wikipedia.org/wiki/Opera_Soft)'s MS-DOS games .PIC file to standard PNG. These files were typically loading screens for old games from the company.

This was just a personal retro reverse engineering attempt to try to grab graphics from the DOS version of [Mutan Zone](http://computeremuzone.com/ficha.php?id=666) game. I was curious of how the image data would be stored to make the code portable to other computers from that era and found how to "see" the loading/title screens from a few games.

## Setup

- Python 3.5+
- `pip3 install pillow`

## Running

Just check inside `pic_to_png.py`, you should only need to change the `FILENAME` constant to the file you wish to export (see `samples` folder for some). I've included some sample PIC fils from classic games.

```bash
python3 pict_to_png.py
```

## Example output
![Mutan Zone](img/mutan_zone.png)

![Abadia del Crimen](img/abadia_del_crimen.png)

![Corsarios](img/corsarios.png)

![Livingstone Supongo 2](img/livingstone_supongo_2.png)

![Sol Negro](img/sol_negro.png)
