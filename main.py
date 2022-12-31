# Standard library imports
import math
import random
import pygame
import pickle
import sys
import time

# Local imports
from tank import Tank, Tank_Spawner
from terrain import Terrain
from sprites import BulletSprite, TankSprite, TerrainSprite
import colors
from multicast_transceiver import createReceiverSocket, createSenderSocket, sendMessage

FRAMES: int = 0
FRAME_LIMIT: int = 60
SOUND_PLAYED_ONCE: bool = True


def intersection(line1, line2):
    ''' Calculate the intersection point between two lines. Each line is represented
    by a tuple of four elements (x1, y1, x2, y2) that correspond to the coordinates
    of the two points that define the line. The function returns a tuple with the
    coordinates of the intersection point if the lines intersect, or None if the
    lines are parallel or don't intersect.
    '''
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
            # Calculate the intersection point
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            return (x, y)
        else:
            return None  # Lines do not intersect


def check_off_limits(gameWidth: int, rect_centerx: int) -> bool:
    # Check if the center x position of the given rectangle is outside of the game screen
    return rect_centerx > gameWidth or rect_centerx < 0


def bullet_hit_animation(start_animation: bool, screen: pygame.Surface, sound: pygame.mixer.Sound, image: pygame.Surface, position: tuple[int, int]):
    """Plays bullet hit animation and sound"""
    global FRAMES, FRAME_LIMIT, SOUND_PLAYED_ONCE
    if not start_animation:
        return False

    if SOUND_PLAYED_ONCE:
        # Play explosion sound once per animation
        sound.play()
        # Reset flag to only play sound once per explosion
        SOUND_PLAYED_ONCE = False
    # Draw explosion image on the screen
    screen.blit(image, position)
    # Increase frames
    FRAMES += 1
    # If total of frames per animation reaches FRAME_LIMIT, corresponds to 1 second
    if FRAMES == FRAME_LIMIT:
        # Reset sound played flag and frames counter
        SOUND_PLAYED_ONCE = True
        FRAMES = 0
        return True
    else:
        return False


def main(WIDTH, HEIGHT, SCALE) -> None:
    # Create the window
    screen: pygame.Surface = pygame.display.set_mode((WIDTH*SCALE, HEIGHT*SCALE))
    # Set the title of the window
    pygame.display.set_caption("Tanks Game")
    # Load background image
    background_image: pygame.Surface = pygame.image.load("images/sky_background.png")
    background_image_offset = random.randint(0, background_image.get_size()[0] - WIDTH*SCALE)
    background_image = pygame.transform.scale(background_image, (background_image.get_width(), HEIGHT*(SCALE+1)))
    # Set the key repeat delay and interval
    pygame.key.set_repeat(50, 50)
    # Load explosion sound
    explosion_sound: pygame.mixer.Sound = pygame.mixer.Sound("images/explosion.wav")
    # Load explosion image
    explosion_image: pygame.Surface = pygame.image.load("images/explosion.png").convert_alpha()
    explosion_image = pygame.transform.scale(explosion_image, (2*SCALE, 2*SCALE))
    # Create a Pygame clock to control the frame rate
    clock: pygame.time.Clock = pygame.time.Clock()

    # Create players tank
    TankSpawner = Tank_Spawner()
    tank_base = Tank((-10, -10), controls=1)
    tank1_sprite: TankSprite = TankSprite(TankSpawner.spawn_tank(tank_base), SCALE)
    tank2_sprite: TankSprite = TankSprite(TankSpawner.spawn_tank(tank_base), SCALE)
    tank1_sprite.tank.set_pos((WIDTH*SCALE/4, 3*HEIGHT*SCALE/4))\
        .set_controls(1)\
        .set_tank_name(USERNAME)
    tank2_sprite.tank.set_pos((3*WIDTH*SCALE/4, 3*HEIGHT*SCALE/4))\
        .set_controls(2)\
        .set_tank_name("Ines")
    tank1_sprite.update_center_pos()
    tank2_sprite.update_center_pos()
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

    senderSocket = createSenderSocket()
    receiverSocket = createReceiverSocket()
    receiverSocket.setblocking(False)

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
    # Create a font object to use for drawing text
    font = pygame.font.Font(None, 36)
    # Signal to indicate game ended and present game over screen
    game_over = False
    # Variable that holds tank's ID of game winner
    game_winner = 0
    # Create a text surface to display the score
    text = font.render(f"Tank {game_winner} Won", True, colors.BLACK)
    # Get the dimensions of the rendered text
    text_rect = text.get_rect()
    # Set the position of the text so it is centered on the screen
    text_rect.center = (WIDTH*SCALE // 2, HEIGHT*SCALE // 2)
    # Run the game loop
    running: bool = True
    while running:
        try:
            input_keys = [False]*512
            if (msg := receiverSocket.recvfrom(8192)):
                userCommand: dict = pickle.loads(msg[0])
                input_username: str = userCommand.get('user')
                if (input_username is not USERNAME):
                    input_keys: list[int] = userCommand.get('keys')
        except BlockingIOError:
            pass

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
        keys_pressed: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        keys: pygame.key.ScancodeWrapper = pygame.key.ScancodeWrapper([a or b for a, b in zip(keys_pressed, input_keys)])
        if any(keys_pressed):
            sendMessage(senderSocket, pickle.dumps({'user': USERNAME, 'keys': keys}))

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
            game_over = True
            game_winner = 2
        if not tank2_sprite.tank.update(keys):
            game_over = True
            game_winner = 1

        # Draw the background image onto the window
        screen.blit(background_image, (-background_image_offset, 0))

        # Update all sprites
        all_sprites.update()
        # Draw all sprites to screen
        all_sprites.draw(screen)

        # Draw preview lines for tank's bullets
        if current_player == 1 and not game_over:
            pygame.draw.line(screen, colors.BLACK, tank1_sprite.rect.center, (
                tank1_sprite.rect.center[0] + tank1_sprite.tank.bullet_power * math.cos(tank1_sprite.tank.bullet_angle),
                tank1_sprite.rect.center[1] + tank1_sprite.tank.bullet_power * math.sin(tank1_sprite.tank.bullet_angle)))
        elif current_player == 2 and not game_over:
            pygame.draw.line(screen, colors.BLACK, tank2_sprite.rect.center, (
                tank2_sprite.rect.center[0] + tank2_sprite.tank.bullet_power * math.cos(tank2_sprite.tank.bullet_angle),
                tank2_sprite.rect.center[1] + tank2_sprite.tank.bullet_power * math.sin(tank2_sprite.tank.bullet_angle)))

        # Draw tank1's name
        tank1_sprite.draw_name(screen)
        # Draw tank2's name
        tank2_sprite.draw_name(screen)

        # Draw tank1's health
        tank1_sprite.draw_health(screen)
        # Draw tank2's health
        tank2_sprite.draw_health(screen)

        if bullet_hit_animation(bullet_1_explosion, screen, explosion_sound, explosion_image, bullet1_sprite.bullet.bullet_hit_position):
            bullet_1_explosion = False
        if bullet_hit_animation(bullet_2_explosion, screen, explosion_sound, explosion_image, bullet2_sprite.bullet.bullet_hit_position):
            bullet_2_explosion = False

        if game_over:
            # Create a text surface to display the score
            text = font.render(f"Tank {game_winner} Won", True, colors.BLACK)
            # Blit the text surface to the screen
            screen.blit(text, text_rect)

        # Update screen
        pygame.display.flip()
        # Limit the frame rate
        clock.tick(frame_limit)

    return True


if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()
    # Initialize pygame mixer
    pygame.mixer.init()

    # Get player name
    USERNAME: str = str(input("Insert your name: "))
    USER_ID: int = random.random()*sys.maxsize
    # Enter game
    while True:
        if main(64, 48, 10):
            break

    # Quit Pygame
    pygame.quit()
