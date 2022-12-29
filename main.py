# Standard library imports
import math
import random
import pygame

# Local imports
from tank import Tank
from terrain import Terrain
from sprites import BulletSprite, TankSprite, TerrainSprite
import colors


def check_off_limits(gameWidth: int, rect_centerx: int) -> bool:
    # Check if the center x position of the given rectangle is outside of the game screen
    return rect_centerx > gameWidth or rect_centerx < 0


def main(WIDTH, HEIGHT, SCALE) -> None:
    # Initialize Pygame
    pygame.init()
    # Create the window
    screen = pygame.display.set_mode((WIDTH*SCALE, HEIGHT*SCALE))
    # Set the title of the window
    pygame.display.set_caption("Tanks Game")

    # Set the key repeat delay and interval
    pygame.key.set_repeat(50, 50)

    # Create a Pygame clock to control the frame rate
    clock = pygame.time.Clock()

    # Create player tank
    tank1_sprite = TankSprite(Tank((WIDTH*SCALE/4, 3*HEIGHT*SCALE/4), 1), SCALE)
    tank2_sprite = TankSprite(Tank((3*WIDTH*SCALE/4, 3*HEIGHT*SCALE/4), 2), SCALE)
    # Create terrain for tanks to move
    terrain_sprite = TerrainSprite(Terrain(WIDTH, HEIGHT, SCALE, colors.GREEN, tank1_sprite.get_bottom_pos()), SCALE)
    # Create bullet sprites for tanks
    bullet1_sprite = BulletSprite(tank1_sprite.tank.bullet, SCALE)
    bullet2_sprite = BulletSprite(tank2_sprite.tank.bullet, SCALE)
    # Add all sprites to a group of sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(bullet1_sprite, bullet2_sprite, tank1_sprite, tank2_sprite, terrain_sprite)

    # Establish first frame positions
    tank1_sprite.update()
    tank2_sprite.update()
    bullet1_sprite.update()
    bullet2_sprite.update()

    # Choose a random player to start
    current_player = random.randint(1, 2)
    # Set the current player flag for the chosen player
    if current_player == 1:
        tank1_sprite.tank.current_player = True
    else:
        tank2_sprite.tank.current_player = True

    # Set frame limit variable
    frame_limit = 30

    # Run the game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        # Update the game logic
        # Retrieve all keys that are being pressed
        keys = pygame.key.get_pressed()

        # Check for collisions
        # Check if bullet1 is off the limits of the screen
        if check_off_limits(WIDTH*SCALE, bullet1_sprite.rect.centerx):
            # Set the flag indicating that bullet2 has hit something
            tank1_sprite.tank.bulletHit = True
        # Check if bullet1 has hit the second tank
        elif bullet1_sprite.rect.colliderect(tank2_sprite.rect):
            # Set the flag indicating that bullet2 has hit something
            tank1_sprite.tank.bulletHit = True
        # Check if bullet1 has hit the terrain
        elif bullet1_sprite.rect.colliderect(terrain_sprite.rect):
            # Set the flag indicating that bullet2 has hit something
            tank1_sprite.tank.bulletHit = True

        # Check if bullet2 is off the limits of the screen
        if check_off_limits(WIDTH*SCALE, bullet2_sprite.rect.centerx):
            # Set the flag indicating that bullet2 has hit something
            tank2_sprite.tank.bulletHit = True
        # Check if bullet2 has hit the second tank
        elif bullet2_sprite.rect.colliderect(tank1_sprite.rect):
            # Set the flag indicating that bullet2 has hit something
            tank2_sprite.tank.bulletHit = True
        # Check if bullet2 has hit the terrain
        elif bullet2_sprite.rect.colliderect(terrain_sprite.rect):
            # Set the flag indicating that bullet2 has hit something
            tank2_sprite.tank.bulletHit = True

        # Switch players
        if not tank1_sprite.tank.current_player and current_player == 1:
            # Switch to player 2
            current_player = 2
            # Tank2 can now move and prepare to shoot
            tank2_sprite.tank.current_player = True
        elif not tank2_sprite.tank.current_player and current_player == 2:
            # Switch to player 1
            current_player = 1
            # Tank1 can now move and prepare to shoot
            tank1_sprite.tank.current_player = True

        # Update tank information
        if not tank1_sprite.tank.update(keys):
            print("Tank 1 destroyed")
        if not tank2_sprite.tank.update(keys):
            print("Tank 2 destroyed")

        # Fill screen
        screen.fill(colors.AZURE)

        # Update all sprites
        all_sprites.update()
        # Draw all sprites to screen
        all_sprites.draw(screen)

        # Draw preview lines for tank's bullets
        pygame.draw.line(screen, colors.BLACK, tank1_sprite.rect.center, (
            tank1_sprite.rect.center[0] + tank1_sprite.tank.bullet_power * math.cos(tank1_sprite.tank.bullet_angle),
            tank1_sprite.rect.center[1] + tank1_sprite.tank.bullet_power * math.sin(tank1_sprite.tank.bullet_angle)))
        pygame.draw.line(screen, colors.BLACK, tank2_sprite.rect.center, (
            tank2_sprite.rect.center[0] + tank2_sprite.tank.bullet_power * math.cos(tank2_sprite.tank.bullet_angle),
            tank2_sprite.rect.center[1] + tank2_sprite.tank.bullet_power * math.sin(tank2_sprite.tank.bullet_angle)))

        # Update screen
        pygame.display.flip()
        # Limit the frame rate
        clock.tick(frame_limit)

    # Quit Pygame
    pygame.quit()
    return


if __name__ == "__main__":
    main(64, 48, 10)
