import pygame

pygame.init()

width = 1280
height = 720

clock = pygame.time.Clock()
fps = 60
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Super Moustachio")

# Player action
moving_left = False
moving_right = False

def drawBackground():
    screen.fill((23,54,60))

class Character(pygame.sprite.Sprite):
    def __init__(self, charType, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.charType = charType
        self.speed = speed
        self.direction = 1
        self.flip = False
        img = pygame.image.load(f'Images/{self.charType}/moustache.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))  # Resize the imagea
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        # set moement to stop
        deltaX = 0
        deltaY = 0
        # movement left and right variables
        if moving_left:
            deltaX = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            deltaX = self.speed
            self.flip = False
            self.direction = 1

        self.rect.x += deltaX
        self.rect.y += deltaY

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

player = Character('player', 640, 400, 0.25, 7)
enemy = Character('enemy', 800, 200, 0.25, 7)


run = True
while run:

    clock.tick(fps)
    drawBackground()
    player.draw()
    enemy.draw()

    player.move(moving_left, moving_right)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keyboard down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
        # keyboard up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()

pygame.quit()