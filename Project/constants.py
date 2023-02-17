import pygame
from pygame.locals import *
from pygame import mixer


pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

pygame.display.set_caption('От девет планини в десетта')
clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

# load image (move to assets)
sun_img = pygame.image.load('Project/img/sun.png')
sky_img = pygame.image.load('Project/img/sky.png')

# load sounds
coin_fx = pygame.mixer.Sound('Project/sounds/coin.wav')
coin_fx.set_volume(0.5)

jump_fx = pygame.mixer.Sound('Project/sounds/jump.wav')
jump_fx.set_volume(0.5)

boss_jump_fx = pygame.mixer.Sound('Project/sounds/final_boss_jump.mp3')
boss_jump_fx.set_volume(0.6)

shooting_fx = pygame.mixer.Sound('Project/sounds/shooting_sound.mp3')
shooting_fx.set_volume(0.5)

game_over_fx = pygame.mixer.Sound('Project/sounds/game_over.wav')
game_over_fx.set_volume(0.5)

pygame.mixer.music.load('Project/sounds/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)

# game
tile_size = 50
game_over = 0
lifes = 3
reset_coordinates = (100, screen_height - 130)
boss_coordinates = (reset_coordinates[0] + 650, 650)
menu = True
weapon_menu = True
weapon_menu_text = False
level = 1
final_level = 3
score = 0
shot_damage = 100
is_won = False

# load shots
fire_shot_img = pygame.image.load('Project/img/small_shot.png')
fire_shot_damage = 5
fire_shot_price = 2

fire_blast_img = pygame.image.load('Project/img/medium_shot.png')
fire_blast_damage = 10
fire_blast_price = 5

fire_wave_img = pygame.image.load('Project/img/large_shot.png')
fire_wave_damage = 25
fire_wave_price = 10

fire_ball_img = pygame.image.load('Project/img/xl_shot.png')
fire_ball_damage = 50
fire_ball_price = 16

# text section
font_score = pygame.font.SysFont('Bauhaus 93', 30)
text_col = (255, 255, 255)
game_over_color = (255, 0, 0)
font_game_over = pygame.font.SysFont('Bauhaus 93', 70)
win_color = (0, 255, 0)
