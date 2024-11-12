import pygame

pygame.init()

screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

class Sprite:
    def __init__(self,image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, color):
        image = pygame.Surface((width,height)).convert_alpha()
        image.blit(self.sheet, (0,0) , (frame * 64 + 16, 21, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image



screen_width = 1280
screen_height = 720
white = (0,255,0)
current_direction = 'down'
current_frame = 0
player_x = 0
player_y = 0

def get_all_frames(file_path):
    whole_image = pygame.image.load(file_path).convert_alpha()
    taking_frames = Sprite(whole_image)
    list = []

    for i in range(0,5):
        list.append(taking_frames.get_image(i, 31, 31, 3, white))
    
    return list
    
animations = {}
animations['down'] = get_all_frames('down_animation.png')
animations['up'] = get_all_frames('up_animation.png')
animations['left'] = get_all_frames('left_animation.png')
animations['right'] = get_all_frames('right_animation.png')

run = True
while run:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    keys = pygame.key.get_pressed()

    is_walking = False

    if keys[pygame.K_a] and player_x > 0:
        player_x -= 5
        current_direction = 'left'
        is_walking = True
    if keys[pygame.K_d] and player_x < screen_width - 95:
        player_x += 5
        current_direction = 'right'
        is_walking = True
    if keys[pygame.K_w] and player_y > 0:
        player_y -= 5
        current_direction = 'up'
        is_walking = True
    if keys[pygame.K_s] and player_y < screen_height - 95:
        player_y += 5
        current_direction = 'down'
        is_walking = True
    if not is_walking:
        current_frame = 0




    screen.fill((0,0,0))
    screen.blit(animations[current_direction][current_frame], (player_x, player_y))
    current_frame += 1
    if current_frame == 5: current_frame = 0

    
    pygame.display.update()        

pygame.quit()