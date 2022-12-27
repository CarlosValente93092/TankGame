import math
import pygame
import colors

from tank import Tank
from terrain import Terrain
from sprites import BulletSprite, TankSprite, TerrainSprite


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
    tank1_sprite = TankSprite(Tank((WIDTH*SCALE/4, 3*HEIGHT*SCALE/4)), SCALE)
    tank2_sprite = TankSprite(Tank((3*WIDTH*SCALE/4, 3*HEIGHT*SCALE/4)), SCALE)
    # Create terrain for tanks to move
    terrain_sprite = TerrainSprite(Terrain(WIDTH, HEIGHT, SCALE, colors.GREEN, tank1_sprite.get_bottom_pos()), SCALE)
    # Create bullet sprites for tanks
    bullet1_sprite = BulletSprite(tank1_sprite.tank.bullet, SCALE)
    bullet2_sprite = BulletSprite(tank2_sprite.tank.bullet, SCALE)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(bullet1_sprite, bullet2_sprite, tank1_sprite, tank2_sprite, terrain_sprite)

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

        keys = pygame.key.get_pressed()
        # Tank 1 controls
        if keys[pygame.K_d]:
            tank1_sprite.tank.move((1, 0))
        if keys[pygame.K_a]:
            tank1_sprite.tank.move((-1, 0))
        if keys[pygame.K_q]:
            tank1_sprite.tank.set_angle(-0.05)
        if keys[pygame.K_e]:
            tank1_sprite.tank.set_angle(0.05)
        if keys[pygame.K_s]:
            tank1_sprite.tank.set_power(-1)
        if keys[pygame.K_w]:
            tank1_sprite.tank.set_power(1)

        # Tank 2 controls
        if keys[pygame.K_l]:
            tank2_sprite.tank.move((1, 0))
        if keys[pygame.K_j]:
            tank2_sprite.tank.move((-1, 0))
        if keys[pygame.K_u]:
            tank2_sprite.tank.set_angle(-0.1)
        if keys[pygame.K_o]:
            tank2_sprite.tank.set_angle(0.1)
        if keys[pygame.K_k]:
            tank2_sprite.tank.set_power(-1)
        if keys[pygame.K_i]:
            tank2_sprite.tank.set_power(1)

        # Shoot button
        if keys[pygame.K_SPACE]:
            bullet1_sprite.image.set_alpha(255)
            bullet2_sprite.image.set_alpha(255)
            tank1_sprite.tank.shoot()
            tank2_sprite.tank.shoot()

        # Update the game logic
        tank1_sprite.tank.update()
        tank2_sprite.tank.update()
        if tank1_sprite.tank.bullet.pos[1] > tank1_sprite.get_bottom_pos():
            tank1_sprite.tank.bullet.shooting = False
            bullet1_sprite.image.set_alpha(0)
        if tank2_sprite.tank.bullet.pos[1] > tank2_sprite.get_bottom_pos():
            tank2_sprite.tank.bullet.shooting = False
            bullet2_sprite.image.set_alpha(0)

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
