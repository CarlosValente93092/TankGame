from tank import Tank
import pygame
import colors


def main(WIDTH, HEIGHT, SCALE):
    # Initialize Pygame
    pygame.init()
    # Create the window
    screen = pygame.display.set_mode((WIDTH*SCALE, HEIGHT*SCALE))
    # Set the title of the window
    pygame.display.set_caption("Tanks Game")

    # Set the key repeat delay and interval
    pygame.key.set_repeat(100, 50)

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
                if keys[pygame.K_RIGHT]:
                    tank1.move((1, 0))
                elif keys[pygame.K_LEFT]:
                    tank1.move((-1, 0))

                if keys[pygame.K_d]:
                    tank2.move((1, 0))
                elif keys[pygame.K_a]:
                    tank2.move((-1, 0))

        # Update the game logic

        # Draw the screen
        screen.fill(colors.AZURE)
        pygame.draw.rect(screen, colors.CHARTREUSE, (tank1.pos[0], tank1.pos[1], SCALE, SCALE))
        pygame.draw.rect(screen, colors.RED, (tank2.pos[0], tank2.pos[1], SCALE, SCALE))
        pygame.draw.rect(screen, colors.ROSE, (0, tank1.pos[1] + SCALE, WIDTH*SCALE, HEIGHT*SCALE-tank1.pos[1]))
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(15)

    # Quit Pygame
    pygame.quit()
    return


if __name__ == "__main__":
    main(64, 48, 10)
