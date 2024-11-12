import pygame

class Character:
    def __init__(self,x,y,width,height,vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel

    
class Sprite:
    def __init__(self,image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, color):
        image = pygame.Surface((width,height)).convert_alpha()
        image.blit(self.sheet, (0,0) , (frame * 64 + 16, 21, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image


class PlayerAnimations:
    def __init__(self, animation_files):
        self.animations = {}
        for direction, file_path in animation_files.items():
            sprite_sheet = pygame.image.load(file_path).convert_alpha()
            sprite = Sprite(sprite_sheet)
            self.animations[direction] = sprite

    def get_animation(self, direction):
        return self.animations.get(direction)
    

class Weapon:
    def __init__(self, x, y, animations):
        self.x = x
        self.y = y
        self.animations = animations
        self.current_weapon_frame = 0
        self.attacking = False  
        self.attack_frame_count = 5  

    def attack(self, mouse_click, direction,is_one_attack):
        
        if mouse_click and not self.attacking and is_one_attack:
            self.attacking = True
            self.current_weapon_frame = 0 

        if self.attacking:
            animation = self.animations.get_animation(direction).get_image(
                self.current_weapon_frame, 47, 41, 4, (255, 255, 255)
            )
            self.current_weapon_frame += 1 
            
            if self.current_weapon_frame >= self.attack_frame_count:
                self.attacking = False
                self.current_weapon_frame = 0 

            return animation
        else:

            return self.animations.get_animation(direction).get_image(0, 47, 41, 4, (255, 255, 255))
        
    def regulate_position(self,x,y,direction):
        if direction == 'left':
            self.x = x - 87
            self.y = y
        elif direction == 'right':
            self.x = x - 20
            self.y = y


class Player(Character):
    def __init__(self, x, y, width, height, vel, animations):
        super().__init__(x, y,width, height, vel)
        self.current_frame = 0
        self.scaled_3_times = 3
        self.animations = animations 
        self.last_direction = 'down'
        
    def move_and_animate(self, keys, screen_width, screen_height, offset, last_frame, white):
 
        if self.last_direction == 'down':
            animation = self.animations.get_animation('down').get_image(0, self.width, self.height, self.scaled_3_times, white)
        if self.last_direction == 'up':    
            animation = self.animations.get_animation('up').get_image(0, self.width, self.height, self.scaled_3_times, white)
        if self.last_direction == 'left':
             animation = self.animations.get_animation('left').get_image(4, self.width, self.height, self.scaled_3_times, white)
        if self.last_direction == 'right':
             animation = self.animations.get_animation('right').get_image(0, self.width, self.height, self.scaled_3_times, white)

        if keys[pygame.K_a] and self.x > 0:
            self.x -= self.vel
            animation = self.animations.get_animation('left').get_image(self.current_frame, self.width, self.height, self.scaled_3_times, white)
            self.last_direction = 'left'

        if keys[pygame.K_d] and self.x <= screen_width - self.width - offset:
            self.x += self.vel
            animation = self.animations.get_animation('right').get_image(self.current_frame, self.width, self.height, self.scaled_3_times, white)
            self.last_direction = 'right'

        if keys[pygame.K_w] and self.y > 0:
            self.y -= self.vel
            animation = self.animations.get_animation('up').get_image(self.current_frame, self.width, self.height, self.scaled_3_times, white)
            self.last_direction = 'up'
            
        if keys[pygame.K_s] and self.y <= screen_height - self.height - offset:
            self.y += self.vel
            animation = self.animations.get_animation('down').get_image(self.current_frame, self.width, self.height, self.scaled_3_times, white)
            self.last_direction = 'down'

        self.current_frame = (self.current_frame + 1) % last_frame  
        return animation
    
    def get_hitbox(self,animation):
        return animation.get_rect(topleft = (self.x,self.y))
   

    