from tank import Tank
import pygame
import colors
import math


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
    tank1 = Tank((WIDTH*SCALE/4, 3*HEIGHT*SCALE/4))
    tank2 = Tank((3*WIDTH*SCALE/4, 3*HEIGHT*SCALE/4))

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
            tank1.move((1, 0))
        if keys[pygame.K_a]:
            tank1.move((-1, 0))
        if keys[pygame.K_q]:
            tank1.set_angle(-0.05)
        if keys[pygame.K_e]:
            tank1.set_angle(0.05)
        if keys[pygame.K_s]:
            tank1.set_power(-1)
        if keys[pygame.K_w]:
            tank1.set_power(1)

        # Tank 2 controls
        if keys[pygame.K_l]:
            tank2.move((1, 0))
        if keys[pygame.K_j]:
            tank2.move((-1, 0))
        if keys[pygame.K_u]:
            tank2.set_angle(-0.1)
        if keys[pygame.K_o]:
            tank2.set_angle(0.1)
        if keys[pygame.K_k]:
            tank2.set_power(-1)
        if keys[pygame.K_i]:
            tank2.set_power(1)

        # Shoot button
        if keys[pygame.K_SPACE]:
            tank1.shoot()
            tank2.shoot()

        # Update the game logic
        tank1.update()
        tank2.update()
        if tank1.bullet.pos[1] > tank1.pos[1]:
            tank1.bullet.shooting = False
        if tank2.bullet.pos[1] > tank2.pos[1]:
            tank2.bullet.shooting = False

        # Fill screen
        screen.fill(colors.AZURE)
        # Draw preview lines for tank's bullets
        pygame.draw.line(screen, colors.BLACK, (tank1.pos[0], tank1.pos[1]), (tank1.pos[0] + tank1.bullet_power *
                         math.cos(tank1.bullet_angle), tank1.pos[1] + tank1.bullet_power * math.sin(tank1.bullet_angle)))
        pygame.draw.line(screen, colors.BLACK, (tank2.pos[0], tank2.pos[1]), (tank2.pos[0] + tank2.bullet_power *
                         math.cos(tank2.bullet_angle), tank2.pos[1] + tank2.bullet_power * math.sin(tank2.bullet_angle)))
        # Draw the terrain
        pygame.draw.rect(screen, colors.CHARTREUSE, (tank1.pos[0], tank1.pos[1], SCALE, SCALE))
        # Draw the tanks
        pygame.draw.rect(screen, colors.RED, (tank2.pos[0], tank2.pos[1], SCALE, SCALE))
        pygame.draw.rect(screen, colors.ROSE, (0, tank1.pos[1] + SCALE, WIDTH*SCALE, HEIGHT*SCALE-tank1.pos[1]))
        # Draw the bullets
        pygame.draw.rect(screen, colors.BLACK, (tank1.bullet.pos[0], tank1.bullet.pos[1], SCALE/2, SCALE/2))
        pygame.draw.rect(screen, colors.BLACK, (tank2.bullet.pos[0], tank2.bullet.pos[1], SCALE/2, SCALE/2))
        # Update screen
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(30)

    # Quit Pygame
    pygame.quit()
    return


if __name__ == "__main__":
    main(64, 48, 10)
