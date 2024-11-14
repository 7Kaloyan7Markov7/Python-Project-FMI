import pygame

pygame.init()

screen_width = 1280
screen_height = 720
white = (255,255,255)

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
floor = pygame.image.load('test_floor.png').convert_alpha()
    
class Sprite:
    def __init__(self,image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, color):
        image = pygame.Surface((width,height)).convert_alpha()
        image.blit(self.sheet, (0,0) , (frame * 64 + 16, 21, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image


current_direction = 'down'
current_frame = 0
player_x = 0
player_y = 0

def get_all_frames(file_path, width, height, scale):
    whole_image = pygame.image.load(file_path).convert_alpha()
    taking_frames = Sprite(whole_image)
    list = []

    for i in range(0,5):
        list.append(taking_frames.get_image(i, width, height, scale, white))
    
    return list
    
animations = {}
animations['down'] = get_all_frames('down_animation.png', 31, 31, 3)
animations['up'] = get_all_frames('up_animation.png', 31, 31, 3)
animations['left'] = get_all_frames('left_animation.png', 31, 31, 3)
animations['right'] = get_all_frames('right_animation.png', 31, 31, 3)

sword_animations= {'down':get_all_frames('white.png',48,39, 4),
                    'up':get_all_frames('white.png',48, 39, 4)}
sword_animations['right'] = get_all_frames('sword_right.png', 48,39,4)
sword_animations['left'] = get_all_frames('sword_left1.png', 48,39, 4)


sword_IDLE = get_all_frames('sword_right.png', 48, 39, 4)
sword_x = 400
sword_y = 100
is_picked_up = False
is_hit_limit = False


run = True
while run:
    clock.tick(40)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    keys = pygame.key.get_pressed()

    is_walking = False

    if keys[pygame.K_a] and player_x > 0:
        player_x -= 10
        current_direction = 'left'
        is_walking = True
    if keys[pygame.K_d] and player_x < screen_width - 95:
        player_x += 10
        current_direction = 'right'
        is_walking = True
    if keys[pygame.K_w] and player_y > 0:
        player_y -= 10
        current_direction = 'up'
        is_walking = True
    if keys[pygame.K_s] and player_y < screen_height - 95:
        player_y += 10
        current_direction = 'down'
        is_walking = True
    if not is_walking:
        current_frame = 0

    screen.blit(floor, (0,0))
    
    player_hit_box = animations['down'][0].get_rect(topleft = (player_x,player_y))
    sword_pick_up_box = sword_IDLE[0].get_rect(width  = 80, height = 80, centerx = sword_x + 120, centery = sword_y + 55)


    screen.blit(animations[current_direction][current_frame], (player_x, player_y))

    if not is_picked_up:
        screen.blit(sword_IDLE[0], (sword_x,sword_y))
    else:
        screen.blit(sword_animations[current_direction][0], (sword_x, sword_y))

    if pygame.Rect.colliderect(player_hit_box, sword_pick_up_box): is_picked_up = True

    if not is_picked_up:
        if not is_hit_limit:
            sword_y += 0.5
        else:
            sword_y -= 0.5

        if sword_y == 124:
            is_hit_limit = True
        elif sword_y == 100:
            is_hit_limit = False
        
    else:
        if current_direction == 'left':
            sword_x = player_x - 87
            sword_y = player_y
        elif current_direction == 'right':
            sword_x = player_x - 20
            sword_y = player_y

    current_frame += 1
    if current_frame == 5: current_frame = 0


    pygame.display.update()        

pygame.quit()
