from Crypto.Random.random import randrange
from UnityTweakTool.section.spaghetti.gsettings import background
from _pickle import load
import pygame
from pygame.locals import *
from pygame.tests.base_test import pygame_quit
from sys import exit


pygame.init()

font_name = pygame.font.get_default_font()
game_font = pygame.font.SysFont(font_name, 72)

pygame.mixer.pre_init(44100,32,2,4096)
explosion_sound = pygame.mixer.Sound('boom.wav')
explosion_played = False

pygame.display.set_caption('Asteróides')
screen = pygame.display.set_mode((956, 560), 0, 32)
background_filename = 'bg_big.png'
background = pygame.image.load(background_filename).convert()
clock = pygame.time.Clock()

ship = {
    'surface':pygame.image.load('ship.png').convert_alpha(),
    'speed':{
        'x':0,
        'y':0
        },
    'position':[randrange(956),randrange(560)]
    } 

explode_ship = {
    'surface': pygame.image.load('ship_exploded.png').convert_alpha(),
    'position': [],
    'speed': {
        'x':0,
        'y':0
        },
        'rect': Rect(0,0,48,48)
    }

collision_anim_counter = 0

def create_asteroid():
    return{
        'surface':pygame.image.load('asteroid.png').convert_alpha(),
        'position':[randrange(892),-64],
        'speed':randrange(1,11)#evita que se crie asteróides com velocidade 0
        }

def move_asteroids():
    for asteroid in asteroids:
        asteroid['position'][1] += asteroid['speed']
        screen.blit(asteroid['surface'],asteroid['position'])#"imprime" na tela a posição do asteroide

def remove_used_asteroids():
    for asteroid in asteroids:
        if asteroid['position'][1] > 560:
            asteroids.remove(asteroid)

def get_rect(obj):
    return Rect(obj['position'][0],
                obj['position'][1],
                obj['surface'].get_width(),
                obj['surface'].get_height())

def ship_collided():
    ship_rect = get_rect(ship)
    for asteroid in asteroids:
        if ship_rect.colliderect(get_rect(asteroid)):
            return True
        
    return False

collide = False 
        
ticks_asteroid = 60 #velocidade de gerção de asteróides
#a cada 60 gameloops ele reinicia a criação
asteroids = []

while True:
    
    if not ticks_asteroid:
        ticks_asteroid = 60
        asteroids.append(create_asteroid())
    else:
        ticks_asteroid -= 1
        
    ship['speed']= {
    'x':0,
    'y':0
    }
    
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    
    
    pressed_keys = pygame.key.get_pressed()
    
    if pressed_keys[K_UP]:
        ship['speed']['y'] = -5
    elif pressed_keys[K_DOWN]:
        ship['speed']['y'] = 5
    if pressed_keys[K_LEFT]:
        ship['speed']['x'] = -5
    elif pressed_keys[K_RIGHT]:
        ship['speed']['x'] = 5
        
    screen.blit(background, (0, 0))
    move_asteroids()
    
    if not collide:
        collide = ship_collided()    
        ship['position'][0] += ship['speed']['x']
        ship['position'][1] += ship['speed']['y']
        screen.blit(ship['surface'],ship['position'])
    else:
        if not explosion_played:
            explosion_played = True
            explosion_sound.play()
            ship['position'][0] += ship['speed']['x']
            ship['position'][1] += ship['speed']['y']
            
            screen.blit(ship['surface'],ship['position'])
        elif collision_anim_counter == 3:
            text = game_font.render('GAME OVER',True, (255,0,0))
            screen.blit(text,(335,250))
        else:
            explode_ship['rect'].x = collision_anim_counter * 48
            explode_ship['position'] = ship['position']
            screen.blit(explode_ship['surface'],explode_ship['position'],
                        explode_ship['rect'])
            collision_anim_counter += 1
    
    
    pygame.display.update()
    
    time_passed = clock.tick(30)
    
    remove_used_asteroids()
    
#     basicFont = pygame.font.SysFont(None,48)
#     WHITE = (255,255,255)
#     BLUE = (0,0,255)
#     text = basicFont.render("Hello", True, WHITE, BLUE)