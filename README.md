KD's Mines in Python/PyGame
===========================

A Minesweeper clone written in Python using PyGame.
Putting more information in this README file is on the todo list.

Running the Game
----------------
```
make init
make test
make try
```

TODO List
---------
- Add more information to this README
- Develop grid translate algorithm for first click
  - Ideally the player should always get a clearing, if possible
- Separate rendering from model
- Add trigger for winning
- Give different numbers different colours

Contributing
------------
There are tons of Minesweeper clones. As such, anything that's neat will
be added to the repo even if it's not on the TODO list. My only condition
is that the classic gameplay is always an option.

Here are some creative ideas:

1. Skins (probably wait until rendering is separate though)
2. Game mode system
3. Powerup system (#2 is a prerequisite)
4. Scenario editor/creator
   - Save/load scenarios using JSON format?
5. Board analysis tools
   - Part of scenario creator?
6. Multiplayer
   - I'd like to make a JavaScript clone in the future some
     websockets would be an awesome option for this.
