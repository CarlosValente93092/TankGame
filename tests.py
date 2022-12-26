import pygame
import math

# Set up Pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))

# Set up the projectile sprite (a circle in this case)
projectile_radius = 25

# Set up initial position, angle, and power
initial_position = (100, 480)
angle = - 10 * math.pi / 21  # 45 degrees in radians
power = 300  # pixels per second

# Calculate the initial velocity
vx = power * math.cos(angle)
vy = power * math.sin(angle)
velocity = (vx, vy)

# Set up acceleration (constant in this case)
acceleration = (0, 2000)  # pixels per second squared

# Set up the clock to control the frame rate
clock = pygame.time.Clock()

dt = 0.02
elapsed_time = 0
# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # Calculate the elapsed time in seconds
    elapsed_time = elapsed_time + dt

    # Calculate the new position of the projectile
    x, y = initial_position
    vx, vy = velocity
    ax, ay = acceleration
    x += vx * elapsed_time + 0.5 * ax * elapsed_time**2
    y += vy * elapsed_time + 0.5 * ay * elapsed_time**2

    # Update the initial position
    initial_position = (x, y)

    # Draw the projectile (a circle in this case)
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), projectile_radius)
    pygame.display.flip()
    clock.tick(15)
