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
                if self.enemy_rect.y > self.player_rect.y and self.enemy_rect.bottom >= self.enemy_ground_level:
                    # Check if enough time has passed since the last jump
                    if time - self.enemy_last_jump_time >= self.enemy_jump_delay:
                        self.enemy_vertical_velocity = self.enemy_jump_strength  # Make the enemy jump
                        self.enemy_last_jump_time = time  # Update the last jump time