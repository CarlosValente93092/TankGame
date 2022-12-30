# Standard library imports
import math
import random
import pygame
import time

# Local imports
from tank import Tank
from terrain import Terrain
from sprites import BulletSprite, TankSprite, TerrainSprite
import colors

FRAMES: int = 0
FRAME_LIMIT: int = 60
SOUND_PLAYED_ONCE: bool = True


def intersection(line1, line2):
    # Extract the points from the lines
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    # Calculate the intersection point
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:
        return None  # Lines are parallel
    else:
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
        if 0 <= t <= 1 and 0 <= u <= 1:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            return (x, y)
        else:
            return None  # Lines do not intersect


def check_off_limits(gameWidth: int, rect_centerx: int) -> bool:
    # Check if the center x position of the given rectangle is outside of the game screen
    return rect_centerx > gameWidth or rect_centerx < 0


def bullet_hit_animation(start_animation: bool, screen: pygame.Surface, sound: pygame.mixer.Sound, image: pygame.Surface, position: tuple[int, int]):
    global FRAMES, FRAME_LIMIT, SOUND_PLAYED_ONCE
    if not start_animation:
        return False

    if SOUND_PLAYED_ONCE:
        # Play explosion sound
        sound.play()
        # Reset flag to only play sound once per explosion
        SOUND_PLAYED_ONCE = False
    # Draw explosion image on the screen
    screen.blit(image, position)
    # image_width, image_height = image.get_size()
    # screen.blit(image, (position[0]-image_width//2, position[1]-image_height//2))
    # Increse frames
    FRAMES += 1
    # If total of frames per animation reaches FRAME_LIMIT, corresponds to 1 seconds
    if FRAMES == FRAME_LIMIT:
        SOUND_PLAYED_ONCE = True
        FRAMES = 0
        return True
    else:
        return False


def main(WIDTH, HEIGHT, SCALE) -> None:
    # Initialize Pygame
    pygame.init()
    # Create the window
    screen: pygame.Surface = pygame.display.set_mode((WIDTH*SCALE, HEIGHT*SCALE))
    # Set the title of the window
    pygame.display.set_caption("Tanks Game")
    # Load background image
    background_image: pygame.Surface = pygame.image.load("images/sky_background.png")
    background_image_offset = random.randint(0, background_image.get_size()[0] - WIDTH*SCALE)
    # Set the key repeat delay and interval
    pygame.key.set_repeat(50, 50)
    # Initialize pygame mixer and load explosion sound
    pygame.mixer.init()
    explosion_sound: pygame.mixer.Sound = pygame.mixer.Sound("images/explosion.wav")
    # Load explosion image
    explosion_image: pygame.Surface = pygame.image.load("images/explosion.png").convert_alpha()
    explosion_image = pygame.transform.scale(explosion_image, (2*SCALE, 2*SCALE))
    # Create a Pygame clock to control the frame rate
    clock: pygame.time.Clock = pygame.time.Clock()

    # Create player tank
    tank1_sprite: TankSprite = TankSprite(Tank((WIDTH*SCALE/4, 3*HEIGHT*SCALE/4), 1), SCALE)
    tank2_sprite: TankSprite = TankSprite(Tank((3*WIDTH*SCALE/4, 3*HEIGHT*SCALE/4), 2), SCALE)
    # Create terrain for tanks to move
    terrain_sprite = TerrainSprite(Terrain(WIDTH, HEIGHT, SCALE, colors.GREEN, tank1_sprite.get_bottom_pos()), SCALE)
    # Create bullet sprites for tanks
    bullet1_sprite: BulletSprite = BulletSprite(tank1_sprite.tank.bullet, SCALE)
    bullet2_sprite: BulletSprite = BulletSprite(tank2_sprite.tank.bullet, SCALE)
    # Add all sprites to a group of sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(bullet1_sprite, bullet2_sprite, tank1_sprite, tank2_sprite, terrain_sprite)

    # Establish first frame positions
    tank1_sprite.update()
    tank2_sprite.update()
    bullet1_sprite.update()
    bullet2_sprite.update()

    # Choose a random player to start
    current_player: int = random.randint(1, 2)
    # Set the current player flag for the chosen player
    if current_player == 1:
        tank1_sprite.tank.current_player = True
    else:
        tank2_sprite.tank.current_player = True

    # Set frame limit variable
    frame_limit: int = FRAME_LIMIT
    # Explosion animation flags
    bullet_1_explosion: bool = False
    bullet_2_explosion: bool = False
    # Set health bar size
    health_bar_size: int = 20
    # Run the game loop
    running: bool = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    return False
        # Update the game logic
        # Retrieve all keys that are being pressed
        keys = pygame.key.get_pressed()

        # Check for collisions
        # Check if bullet1 is off the limits of the screen
        if check_off_limits(WIDTH*SCALE, bullet1_sprite.rect.centerx):
            # Set the flag indicating that bullet2 has hit something
            tank1_sprite.tank.bulletHit = True
        # Check if bullet1 has hit the second tank or hit the terrain
        elif bullet1_sprite.rect.colliderect(tank2_sprite.rect):
            # Set the flag indicating that bullet2 has hit something
            tank1_sprite.tank.bulletHit = True
            # Calculates and infliches damage to other tank
            tank2_sprite.tank.calculate_damage(bullet1_sprite.rect.center)
            # Bullet explosion animation flag
            bullet_1_explosion = True
            bullet1_sprite.bullet.set_bullet_hit_position(tank_hit=True)
        elif bullet1_sprite.rect.colliderect(terrain_sprite.rect):
            # Set the flag indicating that bullet2 has hit something
            tank1_sprite.tank.bulletHit = True
            # Calculates and infliches damage to other tank
            tank2_sprite.tank.calculate_damage(bullet1_sprite.rect.center)
            # Bullet explosion animation
            bullet_1_explosion = True
            # Set bullet 2 hit position
            bullet1_sprite.bullet.set_bullet_hit_position(pos=intersection(bullet1_sprite.rect.bottomleft+bullet1_sprite.bullet.last_pos,
                                                                           terrain_sprite.rect.topleft+terrain_sprite.rect.topright))

            # Check if bullet2 is off the limits of the screen
        if check_off_limits(WIDTH*SCALE, bullet2_sprite.rect.centerx):
            # Set the flag indicating that bullet2 has hit something
            tank2_sprite.tank.bulletHit = True
        # Check if bullet2 has hit the second tank or hit the terrain
        elif bullet2_sprite.rect.colliderect(tank1_sprite.rect):
            # Set the flag indicating that bullet2 has hit something
            tank2_sprite.tank.bulletHit = True
            # Calculates and infliches damage to other tank
            tank1_sprite.tank.calculate_damage(bullet2_sprite.rect.center)
            # Bullet explosion animation
            bullet_2_explosion = True
            # Set bullet 2 hit position
            bullet2_sprite.bullet.set_bullet_hit_position(tank_hit=True)
        elif bullet2_sprite.rect.colliderect(terrain_sprite.rect):
            # Set the flag indicating that bullet2 has hit something
            tank2_sprite.tank.bulletHit = True
            # Calculates and infliches damage to other tank
            tank1_sprite.tank.calculate_damage(bullet2_sprite.rect.center)
            # Bullet explosion animation
            bullet_2_explosion = True
            # Set bullet 2 hit position
            bullet2_sprite.bullet.set_bullet_hit_position(pos=intersection(bullet2_sprite.rect.bottomleft+bullet2_sprite.bullet.last_pos,
                                                                           terrain_sprite.rect.topleft+terrain_sprite.rect.topright))

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

        # Draw the background image onto the window
        screen.blit(background_image, (-background_image_offset, 0))

        # Update all sprites
        all_sprites.update()
        # Draw all sprites to screen
        all_sprites.draw(screen)

        # Draw preview lines for tank's bullets
        if current_player == 1:
            pygame.draw.line(screen, colors.BLACK, tank1_sprite.rect.center, (
                tank1_sprite.rect.center[0] + tank1_sprite.tank.bullet_power * math.cos(tank1_sprite.tank.bullet_angle),
                tank1_sprite.rect.center[1] + tank1_sprite.tank.bullet_power * math.sin(tank1_sprite.tank.bullet_angle)))
        elif current_player == 2:
            pygame.draw.line(screen, colors.BLACK, tank2_sprite.rect.center, (
                tank2_sprite.rect.center[0] + tank2_sprite.tank.bullet_power * math.cos(tank2_sprite.tank.bullet_angle),
                tank2_sprite.rect.center[1] + tank2_sprite.tank.bullet_power * math.sin(tank2_sprite.tank.bullet_angle)))

        # Draw tank1's health
        pygame.draw.rect(screen, colors.RED, pygame.Rect(0, 0, (health_bar_size*SCALE)*tank1_sprite.tank.health/tank1_sprite.tank.max_health, 2*SCALE))
        pygame.draw.rect(screen, colors.BLACK, pygame.Rect(0, 0, health_bar_size*SCALE, 2*SCALE), width=1)

        # Draw tank2's health
        pygame.draw.rect(screen, colors.RED, pygame.Rect(WIDTH*SCALE-health_bar_size*SCALE, 0, (health_bar_size*SCALE)*tank2_sprite.tank.health/tank2_sprite.tank.max_health, 2*SCALE))
        pygame.draw.rect(screen, colors.BLACK, pygame.Rect(WIDTH*SCALE-health_bar_size*SCALE, 0, health_bar_size*SCALE, 2*SCALE), width=1)

        if bullet_hit_animation(bullet_1_explosion, screen, explosion_sound, explosion_image, bullet1_sprite.bullet.bullet_hit_position):
            bullet_1_explosion = False
        if bullet_hit_animation(bullet_2_explosion, screen, explosion_sound, explosion_image, bullet2_sprite.bullet.bullet_hit_position):
            bullet_2_explosion = False

        # Update screen
        pygame.display.flip()
        # Limit the frame rate
        clock.tick(frame_limit)

    return True


if __name__ == "__main__":
    while True:
        if main(64, 48, 10):
            break
    # Quit Pygame
    pygame.quit()
