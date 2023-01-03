# **Tanks Game**
This repository contains the code for a tanks game implemented in Python using the Pygame library.
The game allows for two players to play against each other over the internet in the same LAN.

Features
- Object-oriented programming and inheritance for organizing game elements
- Pygame library for handling graphics and sound
- Command pattern for handling user inputs
- Prototype pattern for tank generation
- State pattern for controlling tank actions
- Double buffer to avoid flickering
- Game loop pattern for main game loop
- Update pattern for updating positions of tanks and bullets using sprites
- Subclass sandbox pattern for sprites and states
- Networking for online multiplayer

## File Structure
The repository contains the following files:

- `bullet.py`: This file contains the code for the Bullet class, which represents a bullet object in the game.
- `colors.py`: This file contains constants for various colors used in the game.
- `fsm.py`: This file contains the code for the Finite State Machine (FSM) used to control the behavior of tanks in the game.
- `input_handler.py`: This file contains the code for the InputHandler class, which handles user inputs and maps them to specific actions.
- `main.py`: This is the main file of the game, containing the code for the game loop and overall game logic.
- `multicast_transceiver.py`: This file contains the code for the multicast sender and receiver sockets used for networking in the game.
- `sprites.py`: This file contains the code for the sprite classes used to display game elements (tanks, bullets, terrain) on the screen.
- `tank.py`: This file contains the code for the Tank class, which represents a tank object in the game, as well as the Tank_Spawner class which is used to generate new tanks.
- `terrain.py`: This file contains the code for the Terrain class, which represents the terrain objects in the game.

## Gameplay
In the game, players control tanks and attempt to destroy the other player's tank. The tanks can move, fire bullets, and reload their guns. The terrain of the game can also affect the movement of the tanks.

