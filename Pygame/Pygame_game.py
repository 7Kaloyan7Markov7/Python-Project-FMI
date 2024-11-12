import pygame
import Sprite_sheet as classes

pygame.init()

screen_width = 1280
screen_height = 720
white = (255,255,255)

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

floor_image = pygame.image.load('test_floor.png').convert_alpha()
skeleton_image = pygame.image.load('enemy_skeleton.png').convert_alpha()
skeleton = classes.Sprite(skeleton_image)
enemy = skeleton.get_image(0,31,31,3,(255,255,255))


animation_files = {
    'down': 'down_animation.png',
    'right': 'right_animation.png',
    'left': 'left_animation.png',
    'up': 'up_animation.png'
}

sword_files = {
    'right': 'sword_right.png',
    'left' : 'sword_left1.png',
    'up': 'white.png',
    'down': 'white.png',
}

player_animations = classes.PlayerAnimations(animation_files)
sword_animations = classes.PlayerAnimations(sword_files)

player = classes.Player(590, 360, 31, 31, 5, player_animations)
sword = classes.Weapon(player.x + 10, player.y, sword_animations)

off_set = 64
scaled_3_times = 3
last_frame = 5

is_one_attack = True
run = True

while run:
    clock.tick(40)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    keys = pygame.key.get_pressed()

    mouse_clicked = pygame.mouse.get_pressed()[0]

    current_animation = player.move_and_animate(keys, screen_width, screen_height, off_set, last_frame, white)
    enemy_hit_box = enemy.get_rect(width = 62, height = 62)

    current_sword_frame = sword.attack(mouse_clicked ,player.last_direction,is_one_attack)

    if mouse_clicked:
        is_one_attack = False
    elif event.type == pygame.MOUSEBUTTONUP:
        is_one_attack = True

    screen.blit(floor_image, (0,0))

    pygame.draw.rect(screen, (0,0,0), player.get_hitbox(current_animation))
    screen.blit(current_animation, (player.x,player.y))

    sword.regulate_position(player.x, player.y - 25, player.last_direction)
    screen.blit(current_sword_frame , (sword.x, sword.y))

    if player.get_hitbox(current_animation).colliderect(enemy_hit_box):
        print("MONI E GEI")

    pygame.display.update()        

pygame.quit()

