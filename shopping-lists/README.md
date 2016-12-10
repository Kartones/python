Shopping Lists
==============

A small web application to manage shopping lists. Very simple, file-based, quick to use even from a mobile device or tablet.

## Instructions

- Copy `config.sample.py` to `config.py` and setup parameters inside it according to your preferences
- To create a new list you must manually create an empty txt file inside your configured data folder
- To edit a list, just click it from the lists view
- Once viewing items, click/tap them one or more times to change their state to:
    - Grey: No need to buy right now ("inactive")
    - Orange: Need to buy ("wanted")
    - Red: Important to buy ("highly wanted")
    - Black: Remove from list. Will dissapear upon changing list or reloading, except if you tap and change its state again
- You can also create new items from the item view at the bottom, just fill the textbox with the item name and press the `+` button.

![Screenshots](screenshot.jpg)

And that's all... It was coded in an afternoon (originally in C#/ASP.NET) and then added more states based on feedback, but as of now I have no plans to further improve it.