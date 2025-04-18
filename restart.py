import pygame
import os

pygame.init()

width = 1280
height = 720

clock = pygame.time.Clock()
fps = 60
gravity = 0.75

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Super Moustachio")

# Level Variables
tile_size = 40

# Load Images
bulletImage = pygame.image.load('Images/bullet/9mm.png').convert_alpha()
poopImage = pygame.image.load('Images/poop/poop.png').convert_alpha()

# Player action
movingLeft = False
movingRight = False
shoot = False
poop = False
poopThrown = False

def drawBackground():
    screen.fill((23,54,60))
    pygame.draw.line(screen, (255,10,0), (0,600), (width, 600))



class Character(pygame.sprite.Sprite):
    def __init__(self, charType, x, y, scale, speed, ammo, poops):
        pygame.sprite.Sprite.__init__(self)
        # Alive and Type
        self.isAlive = True
        self.charType = charType
        self.health = 100
        self.maxHealth = self.health

        # Movement variables
        self.speed = speed
        self.direction = 1
        self.velocity = 0

        # Weapons Player Handling
        self.shotCooldown = 0
        self.ammo = ammo
        self.poops = poops

        # Jumping Variables
        self.isJumping = False
        self.isAirtime = True

        # Direction
        self.flip = False
        
        # Animations
        self.playerAnimations = [] # Array for all frames
        self.index = 0 # Index of current frame
        self.timePassed = pygame.time.get_ticks()
        self.mode = 0
        animationTypes = ['Idle', 'Run', 'Death']
        for animation in animationTypes:
            tempList = []
            numFrames = len(os.listdir(f'Images/{self.charType}/{animation}'))
            for i in range(numFrames):
                img = pygame.image.load(f'Images/{self.charType}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))  # Resize the image
                tempList.append(img)
            self.playerAnimations.append(tempList)
        self.playerAnimations.append(tempList)

        self.image = self.playerAnimations[self.mode][self.index] # Display the first frame
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.animate()
        if self.shotCooldown > 0:
            self.shotCooldown -= 1
        self.checkAlive()

    def movePlayer(self, movingLeft, movingRight):
        # set movement to stop
        deltaX = 0
        deltaY = 0
        # Movement left
        if movingLeft:
            deltaX = -self.speed
            self.flip = True
            self.direction = -1
        # Movement right
        if movingRight:
            deltaX = self.speed
            self.flip = False
            self.direction = 1
        
        # Player Jumping
        if self.isJumping and self.isAirtime == False:
            self.velocity = -15
            self.isJumping = False
            self.isAirtime = True
        
        self.velocity += gravity # gravity keeps player from moving off screen when jumping
        if self.velocity > 10:
            self.velocity
        deltaY += self.velocity

        # Ground Collisions
        if self.rect.bottom + deltaY > 600:
            deltaY = 600 - self.rect.bottom
            self.isAirtime = False

        self.rect.x += deltaX
        self.rect.y += deltaY
    
    def shoot(self):
        if self.shotCooldown == 0 and self.ammo > 0:
            self.shotCooldown = 17
            bullet = Bullet(self.rect.centerx + (0.64 * self.rect.size[0] * self.direction), self.rect.centery + (15), self.direction)
            bulletGroup.add(bullet)
            self.ammo -= 1 # Take ammo away
            print(f'{self.ammo} bullets left') # Display ammo in console

    def animate(self):
        COOLDOWN = 100 # Time between each frame
        self.image = self.playerAnimations[self.mode][self.index] # Set the image to the current index
        if pygame.time.get_ticks() - self.timePassed > COOLDOWN: # If the time between each frame has passed
            self.timePassed = pygame.time.get_ticks() # Reset time
            self.index += 1 # Increase the index by 1 to signal change to next frame
            
        if self.index >= len(self.playerAnimations[self.mode]): # If we reach the end of number of frames
            if self.mode == 2:
                self.index = len(self.playerAnimations[self.mode]) - 1
            else:
                self.index = 0 # Set the index back to zero

    def changeMode(self, newMode):
        if newMode != self.mode:
            self.mode = newMode
            self.index = 0
            self.timePassed = pygame.time.get_ticks()

    def checkAlive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.changeMode(2)
    
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 11
        self.image = bulletImage
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    
    def update(self):
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > width:
            self.kill()

        # Character collision
        if pygame.sprite.spritecollide(player, bulletGroup, False):
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in enemyGroup:
            if pygame.sprite.spritecollide(enemy, bulletGroup, False):
                if enemy.alive:
                    enemy.health -= 25
                    print(f'Enemy Health: {enemy.health}')
                    self.kill()

class Item(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = boxes[self.type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2)

class Poop(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.velocity = -11
        self.speed = 10
        self.image = poopImage
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # Gravity affects poop
        self.velocity += gravity
        deltaX = self.direction * self.speed
        deltaY = self.velocity

        # Ground Collision Check
        if self.rect.bottom + deltaY > 600:
            deltaY = 600 - self.rect.bottom
            self.speed = 0
        
        # Bounces of walls
        if self.rect.left + deltaX < 0 or self.rect.right + deltaX > width:
            self.direction *= -1
            deltaX = self.direction * self.speed

        # Handles grenade position updates
        self.rect.x += deltaX
        self.rect.y += deltaY

        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            pooplosion = Pooplosion(self.rect.x, self.rect.y, 0.5) # Create an explosion
            pooplosionGroup.add(pooplosion) # Generate explosion sprite

            # Damaging anyone in range
            if abs(self.rect.centerx - player.rect.centerx) < tile_size * 2 and abs(self.rect.centery - player.rect.centery) < tile_size * 4: # abs incase a negative is given, i just want the value 
                player.health -= 50
            for enemy in enemyGroup:
                if abs(self.rect.centerx - enemy.rect.centerx) < tile_size * 2 and abs(self.rect.centery - enemy.rect.centery) < tile_size * 4: # abs incase a negative is given, i just want the value 
                    enemy.health -= 50
                    print(f'Enemy Health: {enemy.health}')

class Pooplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f'Images/pooplosions/poop{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
            self.index = 0
            self.image = self.images[self.index]

        self.image = poopImage
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.count = 0
    
    def update(self):
        speed = 4
        self.count += 1

        if self.count >= speed:
            self.count = 0
            self.index += 1
            if self.index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.index]



enemyGroup = pygame.sprite.Group()
bulletGroup = pygame.sprite.Group()
poopGroup = pygame.sprite.Group()
pooplosionGroup = pygame.sprite.Group()

player = Character('player', 640, 400, 0.457, 7, 30, 5)
enemy = Character('enemy', 800, 545, 3, 7, 30, 0)
enemy2 = Character('enemy', 150, 545, 3, 7, 30, 0)
enemyGroup.add(enemy)
enemyGroup.add(enemy2)


run = True
while run:

    clock.tick(fps)
    drawBackground()
    player.update()
    player.draw()

    for enemy in enemyGroup:
        enemy.update()
        enemy.draw()

    # Groups Drawing and Updating
    bulletGroup.update()
    poopGroup.update()
    pooplosionGroup.update()
    bulletGroup.draw(screen)
    poopGroup.draw(screen)
    pooplosionGroup.draw(screen)

    if player.alive:
        # Shooting
        if shoot:
            player.shoot()
        elif poop and poopThrown == False and player.poops > 0:
            poop = Poop(player.rect.centerx + (50 * player.direction), player.rect.centery - 10, player.direction)
            poopGroup.add(poop)
            player.poops -= 1
            poopThrown = True
            print(f'Player has {player.poops} poops left')
        # Moving    
        if movingLeft or movingRight:
            player.changeMode(1) # 1 = Run
        else:
            player.changeMode(0) # 0 = Idle
        player.movePlayer(movingLeft, movingRight)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keyboard key pressed down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                movingLeft = True
            if event.key == pygame.K_d:
                movingRight = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_s:
                poop = True
            if event.key == pygame.K_w and player.alive:
                player.isJumping = True
        # keyboard key lifted up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                movingLeft = False
            if event.key == pygame.K_d:
                movingRight = False
            if event.key == pygame.K_d:
                player.isJumping = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_s:
                poop = False
                poopThrown = False

    pygame.display.update()

pygame.quit()