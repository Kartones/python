# RPG Combat Kata

## Intro

My implementation of the [RPG Combat Kata](http://www.slideshare.net/DanielOjedaLoisel/rpg-combat-kata).

- I had time to code 4 out of the 5 iterations.
- I decided to the lean way, only implementing the absolute minimum for the requested features. That's why for example I don't have a map or battleground where players fight and the "distance" is just unidimensional or I didn't went for a GameEngine or GameEntity abstractions.
- I did TDD all the time, but doing iterations means test contexts sometimes are not perfectly defined (e.g. there are faction-related tests inside their context AND outside in the available actions)


I really liked the kata, despite not having fully finished it.




## Results (**spoilers**):
- My implementation survived quite well the changes of the 4 first iterations.
- For the last one I would have to probably build a game entity or world entity who had properties like being able to be healed, but having abstracted the player from the character would allow me to easily have a "GodPlayer" or "World" player-like entity containing all props and non-player characters. I could also easily make the player have N characters and/or props. So I'm relatively happy with my approach
- That said, it contains some ugly ifs, structure is not perfect, combat rules should go separate, and in general given more time I'd have implemented an actions
- Tests could be improved a lot, I don't have test mothers or similar instance providers, so some changes to the constructors made me change a few instance creations
