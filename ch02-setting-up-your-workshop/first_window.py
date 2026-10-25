import pygame

pygame.init()
screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption("My first Pygame window")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((30, 20, 40))
    pygame.draw.circle(screen, (255, 170, 60), (320, 180), 60)
    pygame.display.flip()
pygame.quit()
