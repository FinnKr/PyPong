# PyPong
Short and simple Pong-Game written in python using the pygame module.  
You need the pygame python-module. Install it with ```pip install pygame```.  
To play the game just start ```game.py```

You can either play against a bot or against a second player.
          
  Key (Player 1/2)  | Action
  ----------------- | -----------------
  w / arrow UP      |     move UP
  s / arrow DOWN    |     move DOWN

--

If you're a ``wayland`` user just set global variable ``SDL_VIDEODRIVER=x11`` to run it using ``XWayland`` or wait until ``pygame`` will support ``wayland`` natively