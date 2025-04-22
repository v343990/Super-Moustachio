import pygame
from player import Player
from pygame.locals import *
from enemy import Enemy

class Menu:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1280, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Moustache Display')
        self.font = pygame.font.Font('Font/Pixeltype.ttf', 50)
        self.run = True


        # Load the background image
        self.background = pygame.image.load('Images/Background Image.jpeg').convert()

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Draw Menu Buttons to Click
        # self.start_button = pygame.draw.rect(self.screen, (0, 0, 0), (640 - 100, 400 - 25, 200, 50), border_radius=25)
        # Start Button
        self.start = pygame.draw.rect(self.screen, (0, 0, 0), (640 - 100, 640 - 25, 200, 50), border_radius=25)
        self.start_text = self.font.render("Start", True, (255, 255, 255))
        self.start_text_rect = self.start_text.get_rect(center=(640, 645))
        self.screen.blit(self.start_text, self.start_text_rect)
        # Options Button
        self.options = pygame.draw.rect(self.screen, (0, 0, 0), (640 - 100, 700 - 25, 200, 50), border_radius=25)
        self.options_text = self.font.render("Options", True, (255, 255, 255))
        self.options_text_rect = self.options_text.get_rect(center=(640, 705))
        self.screen.blit(self.options_text, self.options_text_rect)
        # Quit Button
        self.quit = pygame.draw.rect(self.screen, (0, 0, 0), (640 - 100, 760 - 25, 200, 50), border_radius=25)
        self.quit_text = self.font.render("Quit", True, (255, 255, 255))
        self.quit_text_rect = self.quit_text.get_rect(center=(640, 765))
        self.screen.blit(self.quit_text, self.quit_text_rect)

    def run_menu(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start.collidepoint(event.pos):
                        game = Game()
                        game.run_game()  # Start the game loop
                    elif self.quit.collidepoint(event.pos):
                        self.run = False
                        quit()
                    elif self.options.collidepoint(event.pos):
                        print("Options clicked")
                        # Add options functionality here

            self.draw()  # Draw everything
            pygame.display.flip()  # Update the display
            pygame.time.Clock().tick(60)  # Cap the frame rate

class Game:
    def __init__(self):
        pygame.init()
        self.fps = 60
        self.fpsClock = pygame.time.Clock()
        self.width, self.height = 1280, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Moustache Display')

        # Player setup (imported from player.py)
        self.player = Player()
        self.player_surf = self.player.player_surf
        self.player_rect = self.player.player_rect
        self.speed = self.player.speed
        self.gravity = self.player.gravity
        self.vertical_velocity = self.player.vertical_velocity
        self.jump_strength = self.player.jump_strength
        self.ground_level = self.height
        self.player_health = self.player.health
        
        # Makes player change colour when damaged
        self.is_Flashing_Damage = False
        self.is_Flashing = False
        self.flash_duration = 50  # Duration of the flash in milliseconds
        self.flash_duration_health = 150  # Duration of the flash in milliseconds
        self.flash_start_time = 0
        self.flash_surface = pygame.Surface((self.player_rect.width, self.player_rect.height))
        self.flash_surface.fill((0, 255, 0))
        self.flash_surface.set_alpha(128)
        self.flash_surface_damage = pygame.Surface((self.player_rect.width, self.player_rect.height))
        self.flash_surface_damage.fill((255, 0, 0))
        self.flash_surface_damage.set_alpha(128)


        # Enemy setup (imported from enemy.py)
        self.enemy_defeated = False
        self.enemy = Enemy()
        self.enemy_surf = self.enemy.enemy_surf
        self.enemy_rect = self.enemy.enemy_rect
        self.enemy_speed = self.enemy.speed
        self.enemy_health = self.enemy.health
        self.enemy_vertical_velocity = self.enemy.vertical_velocityn
        self.enemy_jump_strength = self.enemy.jump_strength
        self.enemy_gravity = self.enemy.gravity
        self.enemy_ground_level = self.height
        self.enemy_jump_delay = 500  # Delay in milliseconds (1 second)
        self.enemy_last_jump_time = 0  # Time of the last jump
        self.enemy_damage_delay = 1000  # Delay in milliseconds (1 second)
        self.enemy_last_damage_time = 0  # Time of the last damage

        # UI Setup
        self.text_font = pygame.font.Font('Font/Pixeltype.ttf', 50)
        
        # Bullets setup
        self.bullets = []
        self.bullet_speed = 10
        self.bullet_width, self.bullet_height = 10, 5

        # Health Pickup setup
        self.healthPickup = [
            pygame.Rect(250, 775, 25, 25)
        ]
        
        # Platform setup
        self.platforms = [
            pygame.Rect(200, 600, 200, 10),
            pygame.Rect(500, 500, 200, 10),
            pygame.Rect(800, 400, 200, 10),
            # pygame.Rect(150, 300, 200, 10)
        ]
        self.run = True

    # Event handling
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_LEFT:  # Left button
                    direction = 'left' # Bullet goes left
                    bullet_rect = pygame.Rect(self.player_rect.centerx, self.player_rect.centery, self.bullet_width, self.bullet_height) # Create a bullet rectangle after shooting
                    self.bullets.append((bullet_rect, direction, (0, 0, 0)))  
                if event.key == K_RIGHT:  # Right button
                    direction = 'right' # Bullet goes right
                    bullet_rect = pygame.Rect(self.player_rect.centerx, self.player_rect.centery, self.bullet_width, self.bullet_height) # Create a bullet rectangle after shooting
                    self.bullets.append((bullet_rect, direction, (0, 0, 0)))

                if event.key == K_s:  # 's' key
                    bullet_rect = pygame.Rect(self.player_rect.centerx, self.player_rect.bottom, self.bullet_height, self.bullet_width)
                    self.bullets.append((bullet_rect, 'down', (139, 69, 19)))  # Brown bullets for 's' key
                    self.vertical_velocity = self.jump_strength + 5

    # Player movement
    def update_player(self):

        # Key handling
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            self.player_rect.x -= self.speed # Move left
        if keys[K_d]:
            self.player_rect.x += self.speed # Move right
        if keys[K_SPACE] and (self.player_rect.bottom >= self.ground_level or self.on_platform):
            self.vertical_velocity = self.jump_strength # Jump ahoy!

        # Gravity checks
        self.vertical_velocity += self.gravity # Apply gravity
        self.player_rect.y += self.vertical_velocity
        self.on_platform = False

        # Collision checks with platforms
        for platform in self.platforms:
            if self.player_rect.colliderect(platform) and self.vertical_velocity >= 0:
                self.player_rect.bottom = platform.top  # Move the player to the top of the platform
                self.vertical_velocity = 0 # Stop the player from falling
                self.on_platform = True # Boolean which allows the player to stop falling through platform

        if self.player_rect.bottom >= self.ground_level and not self.on_platform:
            self.player_rect.bottom = self.ground_level # Stop the player from falling through the ground
            self.vertical_velocity = 0
        self.player_rect.x = max(0, min(self.player_rect.x, self.width - self.player_rect.width)) # Keep the player in bounds
        
        # Collision checks with enemy (damage the player)
        if self.player_rect.colliderect(self.enemy_rect):
            time = pygame.time.get_ticks()
            if time - self.enemy_last_damage_time >= self.enemy_damage_delay:
                self.player_health -= self.enemy.damage
                self.enemy_last_damage_time = time
                print(self.player_health)
                self.player_Flash_Damage()

        # Player death check

        if self.player_health <= 0:
            self.run = False

    def health_pickup(self):       
        # Collision checks with health pickups
        for health in self.healthPickup[:]: # Copy the list to avoid modifying it while iterating
            if self.player_rect.colliderect(health): # If the player collides with a health pickup
                self.healthPickup.remove(health) # Remove the health pickup
                previous_health = self.player_health  # Define previous_health variable
                self.player_health += 25 # Increase player health
                self.player_Flash()
                if self.player_health > 100: # Ensure player health does not exceed 100
                    self.player_health = 100
                health_increase = self.player_health - previous_health
                print(f"Health Increased by {health_increase}")
                self.healthDisp = self.text_font.render(f"+{self.player_health}", True, (20, 20, 20))


    def player_Flash_Damage(self):
        self.is_Flashing_Damage = True
        self.flash_start_time = pygame.time.get_ticks()

    def player_Flash(self):
        self.is_Flashing = True
        self.flash_start_time = pygame.time.get_ticks()


    def update_enemy(self, time):

    # Gravity checks
        self.enemy_vertical_velocity += self.enemy_gravity  # Apply gravity
        self.enemy_rect.y += self.enemy_vertical_velocity
        self.enemy_on_platform = False

    # Collision checks with platforms
        for platform in self.platforms:
            if self.enemy_rect.colliderect(platform) and self.enemy_vertical_velocity >= 0:
                self.enemy_rect.bottom = platform.top  # Move the enemy to the top of the platform
                self.enemy_vertical_velocity = 0  # Stop the enemy from falling
                self.enemy_on_platform = True  # Boolean which allows the enemy to stop falling through platform

            if self.enemy_rect.bottom >= self.enemy_ground_level and not self.enemy_on_platform:
                self.enemy_rect.bottom = self.enemy_ground_level  # Stop the enemy from falling through the ground
                self.enemy_vertical_velocity = 0

    # Collision checks with bullets
        for bullet, direction, color in self.bullets[:]:  # Copy the list to avoid modifying it while iterating
            if self.enemy_rect.colliderect(bullet):  # If the enemy collides with a bullet
                self.bullets.remove((bullet, direction, color))  # Remove the bullet
                self.enemy_health -= 10  # Decrease enemy health by 10
                print(self.enemy_health)
                if self.enemy_health <= 0:
                    self.enemy_defeated = True
                    self.enemy_rect = pygame.Rect(-100, -100, 0, 0)  # Move the enemy off-screen
        
        if not self.enemy_defeated:
        # Calculate the direction to the player
            if self.enemy_rect.x < self.player_rect.x:
                self.enemy_rect.x += self.enemy_speed  # Move right
            elif self.enemy_rect.x > self.player_rect.x:
                self.enemy_rect.x -= self.enemy_speed  # Move left

        # Check if the enemy can jump
                if self.enemy_rect.y > self.player_rect.y or self.enemy_rect.bottom >= self.enemy_ground_level:

                    if time - self.enemy_last_jump_time >= self.enemy_jump_delay: # Check if enough time has passed since the last jump
                        self.enemy_vertical_velocity = self.enemy_jump_strength  # Make the enemy jump
                        self.enemy_last_jump_time = time  # Update the last jump time


    # Bullet handling
    def update_bullets(self):
        for bullet, direction, color in self.bullets[:]: # Copy the list to avoid modifying it while iterating
            pygame.draw.rect(self.screen, color, bullet) # Draw the bullet
            
            if direction == 'right':
                bullet.x += self.bullet_speed # Move the bullet to the right
                if bullet.x > self.width:
                    self.bullets.remove((bullet, direction, color))
            
            elif direction == 'left':
                bullet.x -= self.bullet_speed # Move the bullet to the left
                if bullet.x < 0:
                    self.bullets.remove((bullet, direction, color)) # Remove the bullet if it goes off-screen
            
            elif direction == 'down':
                bullet.y += self.bullet_speed  # Move the bullet downwards
                
                if bullet.y > self.height:
                    self.bullets.remove((bullet, direction, color)) # Remove the bullet if it goes off-screen
                else:
                    for platform in self.platforms:
                        if bullet.colliderect(platform):
                            bullet.y = platform.top - self.bullet_height # Place the bullet on top of the platform
                            break
            
            pygame.draw.rect(self.screen, color, bullet) # Draw the bullet again

    # Drawing everything
    def draw(self):
        self.screen.fill((255, 255, 255)) # Fill white background
        self.healthDisp = self.text_font.render(f"+{self.player_health}",True,(20,20,20))
        self.screen.blit(self.healthDisp,(10,10)) # Display health
        
        # Draw Platforms
        for platform in self.platforms:
            pygame.draw.rect(self.screen, (0, 0, 0), platform) # Draw the platforms in platforms array
        
        # Draw Bullets
        for bullet, direction, color in self.bullets:
            pygame.draw.rect(self.screen, color, bullet) # Draw the bullets in bullet array
        
        # Draw Health Pickups
        for health in self.healthPickup:
            pygame.draw.rect(self.screen, (240, 0, 0), health) # Draw the health pickups in the array
        
        # Player Flashing (Damage and Health) and Draw Player
        # Damage Flash
        if self.is_Flashing_Damage:
            if pygame.time.get_ticks() - self.flash_start_time < self.flash_duration:
                flash_damage_active = True
            else:
                self.is_Flashing_Damage = False
                flash_damage_active = False
        else:
            flash_damage_active = False      

        # Health Flash
        if self.is_Flashing:
            if pygame.time.get_ticks() - self.flash_start_time < self.flash_duration_health:
                flash_active = True
            else:
                self.is_Flashing = False
                flash_active = False
        else:
            flash_active = False      

        self.screen.blit(self.player_surf, self.player_rect) # Draw the player
        
        if flash_damage_active:
            self.screen.blit(self.flash_surface_damage, self.player_rect)  # Draw the player flash for damage

        if flash_active:
            self.screen.blit(self.flash_surface, self.player_rect)  # Draw the player flash for gaining health

        if not self.enemy_defeated:
            self.screen.blit(self.enemy_surf, self.enemy_rect) # Draw the enemy

        pygame.display.flip()

    # Main game loop
    def run_game(self):
        while self.run:
            time = pygame.time.get_ticks()
            self.handle_events() # Handle events
            self.update_player() # Update player position
            self.update_enemy(time) # Update enemy position
            self.update_bullets() # Update bullets
            self.health_pickup()
            self.draw()  # Draw everything
            self.fpsClock.tick(self.fps) # Cap the frame rate / physics updates

# Load Menu
if __name__ == "__main__":
    menu = Menu()
    menu.run_menu()