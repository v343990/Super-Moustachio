import pygame
import os
import random
import csv # storing level data
import json # storing keybinds

pygame.init()

width = 1280
height = 800

clock = pygame.time.Clock()
fps = 60
gravity = 0.75

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Super Moustachio")
icon = pygame.image.load('Images/icon.png')
pygame.display.set_icon(icon)

# Level Variables
rows = 16
scrollThreshold = 200
columns = 150
tile_size = height // rows
tileTypes = 21
level = 1
screenScroll = 0
backgroundScroll = 0
fadeStart = False

startGame = False
showSettings = False
startTime = pygame.time.get_ticks()
inputActive = False
inputBox = pygame.Rect(width // 2 - 140, height // 2 - 30, 280, 50)
inputText = ""
levelCompleteTime = None
showLeaderboard = False
leaderboardStartTime = None


# Load Images
bulletImage = pygame.image.load('Images/bullet/9mm.png').convert_alpha()
poopImage = pygame.image.load('Images/poop/poop.png').convert_alpha()
healthImage = pygame.image.load('Images/healthBox.png').convert_alpha()
ammoImage = pygame.image.load('Images/ammoBox.png').convert_alpha()
poopBoxImage = pygame.image.load('Images/poopBox.png').convert_alpha()
skyImage = pygame.image.load('Images/background/sky.png')
mountainImage = pygame.image.load('Images/background/mountain.png').convert_alpha()
pine1Image = pygame.image.load('Images/background/pine1.png').convert_alpha()
pine2Image = pygame.image.load('Images/background/pine2.png').convert_alpha()
menuImage = pygame.image.load('Images/Background Image.jpeg')

# Load Buttons
startButton = pygame.image.load('Images/buttons/startButton.png').convert_alpha()
settingsButton = pygame.image.load('Images/buttons/settingsButton.png').convert_alpha()
quitButton = pygame.image.load('Images/buttons/quitButton.png').convert_alpha()
restartButton = pygame.image.load('Images/buttons/restartButton.png').convert_alpha()
leaderboardButton = pygame.image.load('Images/buttons/leaderboardButton.png').convert_alpha()
mainMenuButton = pygame.image.load('Images/buttons/mainMenuButton.png').convert_alpha()

# Settings Background
settingsBGImage = pygame.image.load('Images/settingsBGImage.png').convert_alpha()

# Load tiles in a list
imageList = []
for x in range(tileTypes): # Iterates through the 21 tiles and loads them in
    img = pygame.image.load(f'Images/tile/{x}.png') # Saves time because each file is a number
    img = pygame.transform.scale(img, (tile_size, tile_size)) # Scale them to the size of each tile
    imageList.append(img) # Add to image list

font = pygame.font.SysFont('Agency FB', 30)
pixelFont = pygame.font.SysFont('Pixeltype Regular', 40)

boxes = {
    'Health'    : healthImage,
    'Ammo'      : ammoImage,
    'Poop'      : poopBoxImage
}

# Player action
movingLeft = False
movingRight = False
shoot = False
poopPressed = False
poopThrown = False

# save the current key bindings to a JSON file
def saveKeybinds():
    with open("keybinds.json", "w") as file: # Open the file in write mode, 'f' is file
        # Dump the keybinds dictionary to the file as JSON
        # The dictionary is created by iterating over the 'keybinds' items and saving it in JSON format
        json.dump({keybind: value for keybind, value in keybinds.items()}, file) # f is file

# load the key bindings from a JSON file
def loadKeybinds():
    try:
        with open("keybinds.json", "r") as file: # Try to open the keybinds JSON file in read mode
            # Load the JSON data from the file
            data = json.load(file)
            return {keybind: int(value) for keybind, value in data.items()} # Line converts all key codes into integers and with same structure as 'data'
    except FileNotFoundError: # If file doesn't exist, return default keybinds
        return {
            'move_left': pygame.K_a,
            'move_right': pygame.K_d,
            'jump': pygame.K_w,
            'shoot': pygame.K_SPACE,
            'poop': pygame.K_s
        }
    
# Key binding array, so they can be changed
keybinds = loadKeybinds()
changingKey = None  # Tracks which key the player is trying to rebind

def saveScore(name, minutes, seconds, filePath="leaderboard.json"): # Saves players time to a JSON file to display on a leaderboard
    try:
        with open(filePath, "r") as file: # Opens file in read mode
            leaderboard = json.load(file) # Loads the file if it is present
    except FileNotFoundError:
        leaderboard = [] # If file not found, load empty
    
    leaderboard.append({"name": name, "minutes": minutes, "seconds": seconds}) # Adds the name, minutes and seconds to the leaderboard in a nice format
    leaderboard.sort(key=lambda x: x["minutes"] * 60 + x["seconds"]) # lambda is part of JSON to calculate total time in seconds

    with open(filePath, "w") as file:
        json.dump(leaderboard, file, indent=4)

def drawLeaderboard(file_path="leaderboard.json"):
    try:
        with open(file_path, "r") as f:
            leaderboard = json.load(f)
    except FileNotFoundError:
        leaderboard = []

    # Background
    screen.fill((0,0,0))
    screen.blit(settingsBGImage, (0,0))
    
    # Title
    titleFont = pygame.font.SysFont('Pixeltype Regular', 50)
    entryFont = pygame.font.SysFont('Pixeltype Regular', 30)
    textDisplayer("Leaderboard", titleFont, (255, 215, 0), width // 2 - 105, 50)

    # Create a box behind the leaderboard for contrast
    boxWidth = 500
    boxHeight = 300
    boxX = width // 2 - boxWidth // 2
    boxY = 120
    pygame.draw.rect(screen, (40, 40, 40), (boxX, boxY, boxWidth, boxHeight), border_radius=12)
    pygame.draw.rect(screen, (200, 200, 200), (boxX, boxY, boxWidth, boxHeight), 2, border_radius=12)

    # Display top 5 scores
    for i, entry in enumerate(leaderboard[:5]):
        name = entry["name"]
        minutes = entry["minutes"]
        seconds = entry["seconds"]
        time_str = f"{minutes:02}:{seconds:02}"
        y_pos = boxY + 30 + i * 50

        if i == 0:
            color = (255, 215, 0)  # Gold
        elif i == 1:
            color = (192, 192, 192)  # Silver
        elif i == 2:
            color = (205, 127, 50)  # Bronze
        else:
            color = (255, 255, 255)

        textDisplayer(f"{i+1}. {name}", entryFont, color, boxX + 30, y_pos)
        textDisplayer(time_str, entryFont, color, boxX + boxWidth - 100, y_pos)

    # Return to Menu Text
    if leaderboardStartTime and pygame.time.get_ticks() - leaderboardStartTime > 3500:
        returnFont = pygame.font.SysFont('Pixeltype Regular', 24)
        textDisplayer("Returning to menu...", returnFont, (180, 180, 180), width // 2 - 80, boxY + boxHeight + 20)

def drawBackground(): # Draws the background
    screen.fill((129,42,15))
    for x in range(5):
        screen.blit(skyImage, ((x * skyImage.get_width()) - backgroundScroll * 0.5, 0))
        screen.blit(mountainImage, ((x * skyImage.get_width()) - backgroundScroll * 0.6, height - mountainImage.get_height() - 325))
        screen.blit(pine1Image, ((x * skyImage.get_width()) - backgroundScroll * 0.7, height - pine1Image.get_height() - 150))
        screen.blit(pine2Image, ((x * skyImage.get_width()) - backgroundScroll * 0.8, height - pine2Image.get_height()))

def textDisplayer(text, font, colour, x, y): # Creates a text object really easily
    image = font.render(text, True, colour)
    screen.blit(image, (x,y))

def resetLevel(): # Reset level function
    enemyGroup.empty()
    poopGroup.empty()
    pooplosionGroup.empty()
    itemGroup.empty()
    decorationGroup.empty()
    waterGroup.empty()
    exitGroup.empty()

    data = [] # Tile List
    for row in range(rows):
        r = [-1] * columns # Creates list with a hundred entries of -1
        data.append(r)
    return data

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

        # AI Variables
        self.moveCounter = 0
        self.vision = pygame.Rect(0,0, 200, 20)
        self.isIdle = False
        self.idleCounter = 0

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
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.animate()
        if self.shotCooldown > 0:
            self.shotCooldown -= 1
        self.checkAlive()

    def movePlayer(self, movingLeft, movingRight):
        # set movement to stop
        screenScroll = 0
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
            self.velocity = -13
            self.isJumping = False
            self.isAirtime = True
        
        self.velocity += gravity # gravity keeps player from moving off screen when jumping
        if self.velocity > 10:
            self.velocity
        deltaY += self.velocity

        # Check for Collisions
        for tile in world.obstacleList:
            if tile[1].colliderect(self.rect.x + deltaX, self.rect.y, self.width, self.height): # Check for collisions on the x axis
                deltaX = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + deltaY, self.width, self.height): # Check for collisions on the y axis
                if self.velocity < 0:  # Check if below the ground? 
                    self.velocity = 0
                    deltaY = tile[1].bottom - self.rect.top # Bottom of the tile to players head
                elif self.velocity >= 0:  # Check if above the ground?
                    self.velocity = 0
                    self.isAirtime = False
                    deltaY = tile[1].top - self.rect.bottom # Players feet to the top of the tile

        # Water collision check
        if pygame.sprite.spritecollide(self, waterGroup, False):
            self.health = 0
        
        # Level complete check
        levelComplete = False
        if pygame.sprite.spritecollide(self, exitGroup, False):
            levelComplete = True

        # Falling off map
        if self.rect.bottom > height:
            self.health = 0

        if self.charType == 'player': # Check if going off the edges of the screen
            if self.rect.left + deltaX < 0 or self.rect.right + deltaX > width:
                deltaX = 0

        self.rect.x += deltaX # Update deltaX - Players X position
        self.rect.y += deltaY # Update deltaY - Players Y position

        # Scrolling Updates
        if self.charType == 'player':
            if (self.rect.right > width - scrollThreshold and backgroundScroll < (world.levelLength * tile_size) - width) or (self.rect.left < scrollThreshold and backgroundScroll > abs(deltaX)):
                self.rect.x -= deltaX # Stops the player from moving ahead of everything
                screenScroll = -deltaX # Moves the background in the opposite direction to the player, scrolling behind him

        return screenScroll, levelComplete

    def shoot(self):
        if self.shotCooldown == 0 and self.ammo > 0:
            self.shotCooldown = 17
            bullet = Bullet(self.rect.centerx + (0.65 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
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
            self.changeMode(2) # 2 = Death. Set the animation of the player to death state.
    
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def enemyAI(self):
        if self.alive and player.isAlive:
        # Idle code
            if self.isIdle == False and random.randint(1, 180) == 1: # 1 in 180 chance while player is moving
                self.changeMode(0) # 0 = Idle. Set the animation state of ai accordingly
                self.isIdle = True # Cause the player to idle
                self.idleCounter = 100 # Idle duration is 100
        # Reaction to seeing the player
            if self.vision.colliderect(player.rect):
                self.changeMode(0) # 0 = Idle
                self.shoot()
        # Moving code
            else:
                if self.isIdle == False: # If no idle, move
                    if self.direction == 1: # Move Right
                        aiMoveRight = True
                    else:
                        aiMoveRight = False # Move left
                    aiMoveLeft = not aiMoveRight # Set aiMoveLeft to the oppposite of aiMoveRight
                    self.movePlayer(aiMoveLeft, aiMoveRight) # Move the ai left or right using movePlayer function
                    self.changeMode(1) # 1 = Run. Set the animation state of the ai accordingly
                    self.moveCounter += 1 # Count up until it reaches value, then change direction
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery + 15) # Vision is updated as the ai moves

                    if self.moveCounter > tile_size: # If they have walked past a tile size
                        self.direction *= -1 # Move in opposite direction
                        self.moveCounter *= -1 # Count down
                else: # If they are idle
                    self.idleCounter -= 1 # Reduce idleCounter value
                    if self.idleCounter <= 0: # When idle counter is 0
                        self.isIdle = False # Go back to walking, idle is false

        # Scroll players
        self.rect.x += screenScroll

class HealthBar():
    def __init__(self, x, y, health, maxHealth):
        self.x = x
        self.y = y
        self.health = health
        self.maxHealth = maxHealth
    
    def Update(self, health):
        
        self.health = health
        pygame.draw.rect(screen, (0, 0, 0), (self.x - 2, self.y - 2, 204, 24))
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, 200, 20))
        if self.health >= self.maxHealth - 64:
            pygame.draw.rect(screen, (0, 200, 0), (self.x, self.y, 200 * self.health / self.maxHealth, 20))
        elif self.health >= self.maxHealth - 65:
            pygame.draw.rect(screen, (150, 50, 0), (self.x, self.y, 200 * self.health / self.maxHealth, 20))
        else:
            pygame.draw.rect(screen, (200, 0, 0), (self.x, self.y, 200 * self.health / self.maxHealth, 20))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 11
        self.image = bulletImage
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    
    def update(self):
        self.rect.x += (self.direction * self.speed) + screenScroll
        if self.rect.right < 0 or self.rect.left > width:
            self.kill()

        # World Tile Collision
        for tile in world.obstacleList:
            if tile[1].colliderect(self.rect): # Destroy bullet if it collides with the level
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

class World():
    def __init__(self):
        self.obstacleList = []

    def processData(self, data):
        self.levelLength = len(data[0]) # Checks how many columns of tiles there are
        for y, row in enumerate(data): # iterates through each value in the data file
            for x, tile in enumerate(row): # enumerate helps us keep track of where we are in the iterations
                if tile >= 0:
                    img = imageList[tile] # Pulls image from the list
                    imgRect = img.get_rect()
                    imgRect.x = x * tile_size # Places them at each point on the grid, multiplied by the size each tile should be
                    imgRect.y = y * tile_size # Places them at each point on the grid, multiplied by the size each tile should be
                    # Allows for resizing?
                    tileData = (img, imgRect)
                    if tile >= 0 and tile <= 8: # Earth
                        self.obstacleList.append(tileData)
                    elif tile >= 9 and tile <= 10: # Water
                        water = Water(img, x * tile_size, y * tile_size)
                        waterGroup.add(water)
                    elif tile >= 11 and tile <= 14: # Decorations
                        decoration = Decorations(img, x * tile_size, y * tile_size)
                        decorationGroup.add(decoration)
                    # Moved these all up from the bottom and associated them with each tile
                    elif tile == 15: # Create Player
                        player = Character('player', x * tile_size, y * tile_size, 0.4, 7, 30, 5)
                        healthBar = HealthBar(75, 81, player.health, player.maxHealth)
                    elif tile == 16: # Create enemies
                        enemy = Character('enemy', x * tile_size, y * tile_size, 0.4, 2, 30, 0)
                        enemyGroup.add(enemy)
                    elif tile == 17: # Ammo Box
                        box = Item('Ammo', x * tile_size, y * tile_size)
                        itemGroup.add(box)
                    elif tile == 18: # Poop Box
                        box = Item('Poop', x * tile_size, y * tile_size)
                        itemGroup.add(box)
                    elif tile == 19: # Health Box
                        box = Item('Health', x * tile_size, y * tile_size)
                        itemGroup.add(box)
                    elif tile == 20: # Exit Level
                        exit = Exit(img, x * tile_size, y * tile_size)
                        exitGroup.add(exit)
        
        return player, healthBar
    
    def draw(self):
        for tile in self.obstacleList:
            tile[1][0] += screenScroll
            screen.blit(tile[0], tile[1])

class Decorations(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height())) # Place it in the middle of a grid, on top of a tile
    
    def update(self):
        self.rect.x += screenScroll

class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height())) # Place it in the middle of a grid, on top of a tile

    def update(self):
        self.rect.x += screenScroll

class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height())) # Place it in the middle of a grid, on top of a tile

    def update(self):
        self.rect.x += screenScroll

class Item(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = boxes[self.type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

    def update(self):
        self.rect.x += screenScroll
        if pygame.sprite.collide_rect(self, player): # Player Box Collision
            if self.type == 'Health':
                player.health += 25
                if player.health > player.maxHealth:
                    player.health = player.maxHealth
            elif self.type == 'Ammo':
                player.ammo += 15
                print(player.ammo)
            elif self.type == 'Poop':
                player.poops += 3
            self.kill()
            
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
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        # Gravity affects poop
        self.velocity += gravity
        deltaX = self.direction * self.speed
        deltaY = self.velocity

        for tile in world.obstacleList:
            if tile[1].colliderect(self.rect.x + deltaX, self.rect.y, self.width, self.height):
                self.direction *= -1
                deltaX = self.direction * self.speed   
        # Bounces of walls
            if tile[1].colliderect(self.rect.x, self.rect.y + deltaY, self.width, self.height): # Check for collisions on the y axis
                self.speed = 3
                if self.velocity < 0:  # Check if below the ground? 
                    self.velocity = 0
                    deltaY = tile[1].bottom - self.rect.top # Bottom of the tile to top of poop
                elif self.velocity >= 0:  # Check if above the ground?
                    self.velocity = 0
                    deltaY = tile[1].top - self.rect.bottom # Bottom of poop to the top of the tile

        # Handles grenade position updates
        self.rect.x += deltaX
        self.rect.y += deltaY

        self.rect.x += screenScroll

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
        self.rect.x += screenScroll
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
itemGroup = pygame.sprite.Group()
decorationGroup = pygame.sprite.Group()
waterGroup = pygame.sprite.Group()
exitGroup = pygame.sprite.Group()

worldData = [] # Tile List
for row in range(rows):
    r = [-1] * columns # Creates list with a hundred entries of -1
    worldData.append(r)

with open(f'level{level}Data.csv', newline='') as csvfile:      # Open the level data file and load it in
    reader = csv.reader(csvfile, delimiter=',') # Reads the CSV, and everytime theres a comma, is a new value
    for x, row in enumerate(reader): # Break CSV into individual chunks
        for y, tile in enumerate(row): # enumerate allows us to keep count of where we are in the iteration
            worldData[x][y] = int(tile)

world = World()
player, healthBar = world.processData(worldData)

run = True
while run:

    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            saveKeybinds()
            run = False
        if event.type == pygame.KEYDOWN:
            if changingKey:
                keybinds[changingKey] = event.key
                saveKeybinds()
                changingKey = None
            elif showSettings:
                if event.key == pygame.K_ESCAPE:
                    showSettings = False
            else:
                if event.key == keybinds['move_left']:
                    movingLeft = True
                if event.key == keybinds['move_right']:
                    movingRight = True
                if event.key == keybinds['shoot']:
                    shoot = True
                if event.key == keybinds['poop']:
                    poopPressed = True
                if event.key == keybinds['jump'] and player.alive:
                    player.isJumping = True
                if inputActive: # If text box is up
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN: # If enter is pressed do this
                            totalTime = (levelCompleteTime - startTime) // 1000 # Total time is the time when level was completed, subtract the startTime
                            minutes = totalTime // 60
                            seconds = totalTime % 60
                            saveScore(inputText, minutes, seconds) # Saves the score the player has inputted
                            inputActive = False # Disables inputActive
                            showLeaderboard = True # Shows the leaderboard
                            leaderboardStartTime = pygame.time.get_ticks() # Leaderboard duration counter
                        elif event.key == pygame.K_BACKSPACE: # Handles deleting text
                            inputText = inputText[:-1] # Deletes 1 character from inputText string
                        else:
                            if len(inputText) <= 12: # Allows us to enter 12 characters
                                inputText += event.unicode

        if event.type == pygame.KEYUP:
            if event.key == keybinds['move_left']:
                movingLeft = False
            if event.key == keybinds['move_right']:
                movingRight = False
            if event.key == keybinds['shoot']:
                shoot = False
            if event.key == keybinds['poop']:
                poopPressed = False
                poopThrown = False


    if not startGame and not showSettings and not showLeaderboard: # Menu Stuff

        screen.blit(menuImage, (0,0)) # Menu Background
        # Start Button
        startButtonRect = startButton.get_rect()
        startButtonRect.centerx = width // 2
        startButtonRect.centery = height // 2 + 215
        screen.blit(startButton, startButtonRect)

        # Settings Button
        settingsButtonRect = settingsButton.get_rect()
        settingsButtonRect.centerx = width // 2
        settingsButtonRect.centery = height // 2 + 275
        screen.blit(settingsButton, settingsButtonRect)

        # Quit Button
        quitButtonRect = quitButton.get_rect()
        quitButtonRect.centerx = width // 2
        quitButtonRect.centery = height // 2 + 335
        screen.blit(quitButton, quitButtonRect)

        # Leaderboard
        leaderboardButtonRect = leaderboardButton.get_rect()
        leaderboardButtonRect.bottomright = (width - 20, height - 20)
        screen.blit(leaderboardButton, leaderboardButtonRect)

        mousePos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]: # If left mouse button is clicked
            if startButtonRect.collidepoint(mousePos):
                startGame = True
                startTime = pygame.time.get_ticks()
            elif settingsButtonRect.collidepoint(mousePos):
                print("Show Settings")
                showSettings = True
            elif quitButtonRect.collidepoint(mousePos):
                run = False
                quit()
            elif leaderboardButtonRect.collidepoint(mousePos):
                showLeaderboard = True
                leaderboardStartTime = pygame.time.get_ticks()
        
    elif showSettings == True: # Settings Menu
        screen.fill((0, 0, 0))
        screen.blit(settingsBGImage, (0,0))
        textDisplayer("Settings - Press a key to rebind", pixelFont, (255, 255, 255), 420, 100)  # Title

        # List of action identifiers and display names
        actions = ['move_left', 'move_right', 'jump', 'shoot', 'poop']
        action_names = ['Move Left', 'Move Right', 'Jump', 'Shoot', 'Poop']

        mousePos = pygame.mouse.get_pos()  # Get mouse position for hover/click detection

        for i, action in enumerate(actions): # Loop through each action with its index (i) and action name (e.g. 'move_left')
            # Display current key binding next to its action name
            label = f"{action_names[i]}: {pygame.key.name(keybinds[action])}" # Creates the list of all the key presets, and their current bind
            textDisplayer(label, pixelFont, (255, 255, 255), 480, 180 + i * 60) # Just displays the label visually

            # Create clickable area (rect) for each action
            rect = pygame.Rect(470, 175 + i * 60, 300, 40)

            # Highlight the box if the mouse is over it
            if rect.collidepoint(mousePos):
                pygame.draw.rect(screen, (100, 100, 255), rect, 2)  # Blue border when hovering over the key box

                if pygame.mouse.get_pressed()[0]: # If clicked on the button, allows for the changing of the keybind
                    changingKey = action
            else:
                pygame.draw.rect(screen, (255, 255, 255), rect, 2)  # Normal white border
        textDisplayer("Press ESC to return", pixelFont, (200, 200, 0), 500, 550) # Back to menu instruction
 
    else:
        drawBackground() # Draw background
        world.draw() # Draw the world

        textDisplayer('Ammo:' , font, (255,255,255), 5, 2) # Draw Ammo Value Text
        for x in range(player.ammo):
            screen.blit(bulletImage, (75 + (x * 17), 22)) # Draw Visual Ammo Counter (Like Call of Duty: WaW and MW)
        textDisplayer('Poops: ', font, (255,255,255), 5, 35) # Draw Poops Value Text
        for x in range(player.poops):
            screen.blit(poopImage, (75 + (x * 20), 49)) # Draw Visual Grenade Counter (Like Call of Duty)
        textDisplayer('Health: ', font, (255,255,255), 5, 69)
        healthBar.Update(player.health)
        player.update()
        player.draw()

        for enemy in enemyGroup:
            enemy.enemyAI()
            enemy.update()
            enemy.draw()

        # Groups Updating and Drawing
        bulletGroup.update()
        poopGroup.update()
        pooplosionGroup.update()
        itemGroup.update()
        decorationGroup.update()
        waterGroup.update()
        exitGroup.update()

        bulletGroup.draw(screen)
        poopGroup.draw(screen)
        pooplosionGroup.draw(screen)
        itemGroup.draw(screen)
        decorationGroup.draw(screen)
        waterGroup.draw(screen)
        exitGroup.draw(screen)

        if player.alive and not inputActive:
            # Tracking Timer
            elapsedTime = pygame.time.get_ticks() - startTime
            elapsedSeconds = elapsedTime // 1000
            minutes = elapsedSeconds // 60
            seconds = elapsedSeconds % 60
            timer = (f"Time: {minutes:02}:{seconds:02}")
             # Center it under the player health bar which is 200 pixels wide
            textDisplayer(timer, font, (255, 255, 255), 1165, 5)
            # Shooting
            if shoot:
                player.shoot()
            elif poopPressed and poopThrown == False and player.poops > 0:
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
            screenScroll, levelComplete = player.movePlayer(movingLeft, movingRight)
            backgroundScroll -= screenScroll

            # Check if player has completed level
            if levelComplete and levelCompleteTime is None:
                levelCompleteTime = pygame.time.get_ticks() # gets the time after level is complete
                inputActive = True

        elif not levelComplete:
            deathOverlay = pygame.Surface((width, height)) # Dark overlay
            deathOverlay.fill((150,0,0)) # Fill the darkOverlay surface with red
            deathOverlay.set_alpha(100)
            screen.blit(deathOverlay, (0,0))

            screenScroll = 0 # Stop everything from scrolling

            # Restart Button
            restartButtonRect = restartButton.get_rect()
            restartButtonRect.centerx = width // 2
            restartButtonRect.centery = height // 2 - 50
            screen.blit(restartButton, restartButtonRect)
            # Main Menu Button
            mainMenuButtonRect = mainMenuButton.get_rect()
            mainMenuButtonRect.centerx = width // 2
            mainMenuButtonRect.centery = height // 2 + 50
            screen.blit(mainMenuButton, mainMenuButtonRect)

            mousePos = pygame.mouse.get_pos()
            if restartButtonRect.collidepoint(mousePos):
                restartButton.set_alpha(180) # Show that button is being hovered over
                if pygame.mouse.get_pressed()[0]: # If left click is pressed
                    backgroundScroll = 0 # Reset background position
                    worldData = resetLevel()
                    with open(f'level{level}Data.csv', newline='') as csvfile: # Open the level data file and load it in
                        reader = csv.reader(csvfile, delimiter=',') # Reads the CSV, and everytime theres a comma, is a new value
                        for x, row in enumerate(reader): # Break CSV into individual chunks
                            for y, tile in enumerate(row): # enumerate allows us to keep count of where we are in the iteration
                                worldData[x][y] = int(tile)
                    world = World()
                    player, healthBar = world.processData(worldData)
                    startTime = pygame.time.get_ticks()
            else:
                restartButton.set_alpha(255)
            if mainMenuButtonRect.collidepoint(mousePos):
                mainMenuButton.set_alpha(180) # Show that button is being hovered over
                if pygame.mouse.get_pressed()[0]: # If left click is pressed
                    backgroundScroll = 0 # Reset background position
                    worldData = resetLevel()
                    with open(f'level{level}Data.csv', newline='') as csvfile: # Open the level data file and load it in
                        reader = csv.reader(csvfile, delimiter=',') # Reads the CSV, and everytime theres a comma, is a new value
                        for x, row in enumerate(reader): # Break CSV into individual chunks
                            for y, tile in enumerate(row): # enumerate allows us to keep count of where we are in the iteration
                                worldData[x][y] = int(tile)
                    world = World()
                    player, healthBar = world.processData(worldData)
                    startGame = False
            else:
                mainMenuButton.set_alpha(255)

        if inputActive:
            darkOverlay = pygame.Surface((width, height)) # Dark overlay
            darkOverlay.set_alpha(180)
            darkOverlay.fill((0,0,0)) # Fill the darkOverlay surface with black
            screen.blit(darkOverlay, (0,0)) # blit the dark overlay
            pygame.draw.rect(screen, (180, 180, 180), inputBox)
            textSurf = pixelFont.render(inputText, False, (20, 20, 20))
            screen.blit(textSurf, (inputBox.x + 10, inputBox.y + 15))
            textDisplayer("Enter your name: ", pixelFont, (255,255,255), inputBox.x, inputBox.y - 40)
        
        elif showLeaderboard:
            drawLeaderboard()
            if leaderboardStartTime and pygame.time.get_ticks() - leaderboardStartTime > 5000:
                showLeaderboard = False
                startGame = False
                levelCompleteTime = None
                inputText = ""
                inputActive = False
                leaderboardStartTime = None

    pygame.display.update()

pygame.quit()