import pygame

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((400, 300))

# Set up the projectile
projectile = pygame.Rect(100, 100, 10, 10)
speed = (5, 5)
trail = []
counter = 0

# Run the game loop
running = True
while running:
    # Update the projectile position
    projectile.x += speed[0]
    projectile.y += speed[1]

    # Add the projectile position to the trail
    counter += 1
    if counter % 1000 == 0:  # only add a position every tenth frame
        trail.append((projectile.x, projectile.y))

    # Draw the trail
    if trail:
        for pos in trail:
            pygame.draw.circle(screen, (255, 255, 255), pos, 2)

    # Draw the projectile
    pygame.draw.rect(screen, (255, 255, 255), projectile)

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the screen
    pygame.display.flip()

# Quit Pygame
