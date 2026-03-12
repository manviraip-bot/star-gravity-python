import pygame
import random
import math

pygame.init()

width, height = 900, 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Mouse Gravity Field")
clock = pygame.time.Clock()

particles = []

class Particle:

    def __init__(self):
        self.x = random.randint(0,width)
        self.y = random.randint(0,height)
        self.vx = random.uniform(-1,1)
        self.vy = random.uniform(-1,1)

    def update(self, mx, my):

        dx = mx - self.x
        dy = my - self.y
        dist = math.sqrt(dx*dx + dy*dy)

        if dist < 200:
            self.vx += dx*0.0005
            self.vy += dy*0.0005

        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pygame.draw.circle(screen,(255,255,255),(int(self.x),int(self.y)),3)

for i in range(120):
    particles.append(Particle())

running = True

while running:

    screen.fill((0,0,0))
    mx,my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for p in particles:
        p.update(mx,my)
        p.draw()

    pygame.display.update()
    clock.tick(60)

pygame.quit()