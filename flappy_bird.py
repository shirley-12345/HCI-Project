
import random
import sys

import cv2
import pygame
from pygame.locals import *
import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect


window_width = 600
window_height = 480
BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
score = 0

# set height and width
window = pygame.display.set_mode((window_width, window_height))
elevation = window_height * 0.8
game_images = {}
game_sounds = {}
framepersecond = 32

# picture path
pipeimage = 'images/pipe.png'
background_image = 'images/background.png'
birdplayer_image = 'images/bird.png'
hit_sound = 'sound/hit.wav'
point_sound = 'sound/point.wav'
fly_sound = 'sound/fly.wav'


# start game
def flappygame(score):
    initBirdhorizontal = int(window_width / 2)
    initBirdvertical = int(window_width / 2)
    tempheight = 100

    # create pipe
    pipe1 = createRandomPipe()
    pipe2 = createRandomPipe()

    # list of down pipe
    downPipes = [
        {'x': window_width + 300 - tempheight,
         'y': pipe1[1]['y']},
        {'x': window_width + 300 - tempheight + (window_width / 2),
         'y': pipe2[1]['y']},
    ]

    # list of up pipe
    upperPipes = [
        {'x': window_width + 300 - tempheight,
         'y': pipe1[0]['y']},
        {'x': window_width + 200 - tempheight + (window_width / 2),
         'y': pipe2[0]['y']},
    ]

    # velocity
    pipeX = -4

    # bird velocity
    birdY = -15
    birdMaxY = 10
    birdAccY = 1

    bird_flap_velocity = -8
    flappy = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if initBirdvertical > 0:
                    game_sounds['fly'].play()
                    birdY = bird_flap_velocity
                    flappy = True

        # detect crash
        crash = isCrash(initBirdhorizontal, initBirdvertical, upperPipes, downPipes)
        if crash:
            return

        # score update
        birdPosition = initBirdhorizontal + game_images['flappybird'].get_width() / 2
        for pipe in upperPipes:
            pipMid = pipe['x'] + game_images['pipeimage'][0].get_width() / 2
            if pipMid <= birdPosition < pipMid + 4:
                score = score + 1
                game_sounds['point'].play()


        if birdY < birdMaxY and not flappy:
            birdY += birdAccY

        if flappy:
            flappy = False
        birdHeight = game_images['flappybird'].get_height()
        initBirdvertical = initBirdvertical +  min(birdY, elevation - initBirdvertical - birdHeight)


        for upperPipe, lowerPipe in zip(upperPipes, downPipes):
            upperPipe['x'] += pipeX
            lowerPipe['x'] += pipeX


        if 0 < upperPipes[0]['x'] and upperPipes[0]['x']< 5:
            pipe = createRandomPipe()
            upperPipes.append(pipe[0])
            downPipes.append(pipe[1])


        if upperPipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            upperPipes.pop(0)
            downPipes.pop(0)


        window.blit(pygame.transform.scale(game_images['background'], (window_width, window_height)),(0,0))
        for upperPipe, lowerPipe in zip(upperPipes, downPipes):
            window.blit(game_images['pipeimage'][0],
                        (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipeimage'][1],
                        (lowerPipe['x'], lowerPipe['y']))


        window.blit(game_images['flappybird'], (initBirdhorizontal, initBirdvertical))


        numbers = [int(x) for x in list(str(score))]
        width = 0

        # find picture
        for i in numbers:
            width += game_images['number_images'][i].get_width()
        Xoffset = (window_width - width) / 1.1

        # Blitting picture
        for i in numbers:
            window.blit(game_images['number_images'][i],
                        (Xoffset, window_width * 0.02))
            Xoffset += game_images['number_images'][i].get_width()


        pygame.display.update()
        framepersecond_clock.tick(framepersecond)


# function detect crash
def isCrash(initBirdhorizontal, initBirdvertical, upperPipes, downPipes):

    # Collision with upper pipes
    for pipe in upperPipes:
        pipe_Height = game_images['pipeimage'][0].get_height()
        if (initBirdvertical < pipe_Height + pipe['y'] and abs(initBirdhorizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            game_sounds['hit'].play()
            return True

    # Collision with lower pipe
    for pipe in downPipes:
        if (initBirdvertical + game_images['flappybird'].get_height() > pipe['y']) and abs(initBirdhorizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            game_sounds['hit'].play()
            return True

    # collision with boundary
    if initBirdvertical > elevation - 25 or initBirdvertical < 0:
        game_sounds['hit'].play()
        return True

    return False


def createRandomPipe():
    offset = window_height / 3
    pipe_Height = game_images['pipeimage'][0].get_height()
    y2 = offset + random.randrange(0, int(window_height - 1.5 * offset))
    # print(pipe_Height)
    # print(int(window_height - 1.5 * offset))
    # print(y2)
    pipeX = window_width + 10
    y1 = pipe_Height - y2 + offset
    pipe = [
        # upper Pipe
        {'x': pipeX, 'y': -y1},

        # lower Pipe
        {'x': pipeX, 'y': y2}
    ]
    return pipe



if __name__ == "__main__":
    pygame.init()
    framepersecond_clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')

    # load picture
    game_images['number_images'] = (
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha()
    )
    game_images['flappybird'] = pygame.image.load(birdplayer_image).convert_alpha()
    game_images['background'] = pygame.image.load(background_image).convert_alpha()
    game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load(pipeimage).convert_alpha(), 180),
                                pygame.image.load(pipeimage).convert_alpha())
    game_sounds['hit'] = pygame.mixer.Sound(hit_sound)
    game_sounds['point'] = pygame.mixer.Sound(point_sound)
    game_sounds['fly'] = pygame.mixer.Sound(fly_sound)


    while True:
        initBirdhorizontal = int(window_width / 2.3)
        initBirdvertical = int(
            (window_height - game_images['flappybird'].get_height()) / 3)
        ground = 0

        while True:
            for event in pygame.event.get():
                # quit event
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    # jump event
                    game_sounds['fly'].play()
                    flappygame(score)


                else:
                    # build image
                    window.blit(pygame.transform.scale(game_images['background'], (window_width, window_height)),(0,0))
                    window.blit(game_images['flappybird'],
                                (initBirdhorizontal, window_height // 2+25))

                    # menu
                    white = (255, 255, 255)
                    black = (0, 0, 0)
                    yellow = (183, 128, 55)
                    X = 400
                    Y = 400
                    font = pygame.font.Font('freesansbold.ttf', 25)
                    welcomefont = pygame.font.Font('freesansbold.ttf', 25)

                    welcome = welcomefont.render('Welcome to play Flappy Game', True, yellow)
                    start = font.render('Start (Five Figures)', True, yellow)
                    end = font.render('End (Three Figures)', True, yellow)

                    welcometextRect = start.get_rect()
                    starttextRect = start.get_rect()
                    endtextRect = start.get_rect()

                    welcometextRect.center = ((window_width // 2 - 70), window_height // 2 - 100)
                    starttextRect.center = (window_width // 2 , window_height // 2 - 50)
                    endtextRect.center = (window_width // 2, (window_height // 2))

                    window.blit(welcome,welcometextRect)
                    window.blit(start, starttextRect)
                    window.blit(end, endtextRect)


                    pygame.display.update()
                    framepersecond_clock.tick(framepersecond)
    main()