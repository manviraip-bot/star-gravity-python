import pygame
import random
import math

pygame.init()
pygame.mixer.init()

width, height = 900, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("🌀 Gravity Playground PRO")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)



NUM_PARTICLES = 150
GRAVITY = 0.002
SUCTION_RADIUS = 120

particles = []
score = 0
mode = "normal"
chaos = False

class Particle:
    def __init__(self):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.size = random.randint(2, 4)
        self.color_shift = random.randint(0, 255)

    def update(self, mx, my):
        dx = mx - self.x
        dy = my - self.y
        dist = math.sqrt(dx*dx + dy*dy) + 0.1

        if mode == "blackhole":
            self.vx += dx/dist * 0.01
            self.vy += dy/dist * 0.01
            self.vx += -dy * 0.002
            self.vy += dx * 0.002

        elif mode == "repel":
            self.vx -= dx/dist * 0.01
            self.vy -= dy/dist * 0.01

        elif mode == "orbit":
            self.vx += -dy * 0.003
            self.vy += dx * 0.003

        else:
            self.vx += dx/dist * GRAVITY
            self.vy += dy/dist * GRAVITY

        if chaos:
            self.vx += random.uniform(-0.5, 0.5)
            self.vy += random.uniform(-0.5, 0.5)

        self.vx *= 0.98
        self.vy *= 0.98

        self.x += self.vx
        self.y += self.vy

        if self.x < 0: self.x = width
        if self.x > width: self.x = 0
        if self.y < 0: self.y = height
        if self.y > height: self.y = 0

        self.color_shift += 2

    def draw(self):
        r = (math.sin(self.color_shift * 0.05) * 127 + 128)
        g = (math.sin(self.color_shift * 0.07) * 127 + 128)
        b = (math.sin(self.color_shift * 0.09) * 127 + 128)

        for i in range(3):
            pygame.draw.circle(
                screen,
                (int(r), int(g), int(b)),
                (int(self.x), int(self.y)),
                self.size + i,
                1
            )


for _ in range(NUM_PARTICLES):
    particles.append(Particle())

running = True

while running:

    fade = pygame.Surface((width, height))
    fade.set_alpha(30)
    fade.fill((10, 10, 20))
    screen.blit(fade, (0, 0))

    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.MOUSEBUTTONDOWN:
            
            for p in particles:
                p.vx += random.uniform(-5, 5)
                p.vy += random.uniform(-5, 5)

            flash = pygame.Surface((width, height))
            flash.set_alpha(80)
            flash.fill((255, 255, 255))
            screen.blit(flash, (0, 0))

        if event.type == pygame.KEYDOWN:
           

            if event.key == pygame.K_SPACE:
                chaos = not chaos

            if event.key == pygame.K_b:
                mode = "blackhole"

            if event.key == pygame.K_r:
                mode = "repel"

            if event.key == pygame.K_o:
                mode = "orbit"

            if event.key == pygame.K_n:
                mode = "normal"

    new_particles = []

   
    if mode == "blackhole":
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(50)
        overlay.fill((20, 0, 40))
        screen.blit(overlay, (0, 0))

        pygame.draw.circle(screen, (0, 0, 0), (mx, my), 80)
        pygame.draw.circle(screen, (150, 0, 255), (mx, my), SUCTION_RADIUS, 2)

    for p in particles:
        dist = math.sqrt((mx - p.x)**2 + (my - p.y)**2)

       
        if mode == "blackhole" and dist < SUCTION_RADIUS:
         
            pygame.draw.circle(screen, (255, 255, 255), (int(p.x), int(p.y)), 4)
            score += 1
            continue

        p.update(mx, my)
        p.draw()
        new_particles.append(p)

    particles = new_particles

    
    while len(particles) < NUM_PARTICLES:
        particles.append(Particle())

    
    if chaos:
        shake_x = random.randint(-3, 3)
        shake_y = random.randint(-3, 3)
        screen.blit(screen, (shake_x, shake_y))

   
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    mode_display = font.render(f"Mode: {mode.upper()}", True, (255, 255, 255))
    screen.blit(mode_display, (10, 40))

    controls = font.render("B: BlackHole | R: Repel | O: Orbit | N: Normal | SPACE: Chaos", True, (200, 200, 200))
    screen.blit(controls, (10, height - 30))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
