# Standard library imports
import math

# Third-party imports
import pygame

# Local imports
from tank import Tank
from terrain import Terrain
from sprites import BulletSprite, TankSprite, TerrainSprite
import colors


def main(WIDTH, HEIGHT, SCALE):
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

    # Tank 1 starts the game
    tank1_sprite.tank.current_player = True
    current_player = 1

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
        if tank1_sprite.tank.bullet.pos[1] > tank1_sprite.get_bottom_pos():
            tank1_sprite.tank.bulletHit = True
        if tank2_sprite.tank.bullet.pos[1] > tank2_sprite.get_bottom_pos():
            tank2_sprite.tank.bulletHit = True

        # Switches players
        if not tank1_sprite.tank.current_player and current_player == 1:
            current_player = 2
            tank2_sprite.tank.current_player = True
        elif not tank2_sprite.tank.current_player and current_player == 2:
            current_player = 1
            tank1_sprite.tank.current_player = True

        tank1_sprite.tank.update(keys)
        tank2_sprite.tank.update(keys)

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
        clock.tick(30)

    # Quit Pygame
    pygame.quit()
    return


if __name__ == "__main__":
    main(64, 48, 10)
