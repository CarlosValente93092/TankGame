Tanks Game
This repository contains the code for a tanks game implemented in Python using the Pygame library. The game allows for two players to play against each other over the internet, and includes a chat feature for communication during the game.

File Structure
The repository contains the following files:

main.py: This is the main file of the game. It contains the game loop and logic for handling user input, updating game elements, and rendering the game to the screen.

tank.py: This file defines the Tank class, which represents a tank in the game. It has attributes such as position, health, and a finite state machine (FSM) to control its behavior. The Tank_Spawner class is also defined in this file, which is responsible for creating new tanks.

terrain.py: This file defines the Terrain class, which represents the terrain in the game. It has attributes such as the type of terrain and the position of the terrain on the screen.

sprites.py: This file defines the BaseSprite class, which is a subclass of pygame.sprite.Sprite and serves as a base class for the TankSprite and BulletSprite classes. It also defines the TerrainSprite class, which is responsible for rendering the terrain on the screen.

multicast_transceiver.py: This file contains functions for creating multicast sender and receiver sockets and for sending and receiving messages between the sockets.

Gameplay
In the game, players control tanks and attempt to destroy the other player's tank. The tanks can move, fire bullets, and reload their guns. The terrain of the game can also affect the movement of the tanks.

Innovative Aspects
One innovative aspect of the game is the use of networking to allow two players to play against each other over the internet. The game also has a chat feature that allows players to communicate during the game.
