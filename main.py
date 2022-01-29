import pygame
import sys
import os


FPS = 50
WIDTH = 1000
HEIGHT = 1000
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def is_in(cords, rect_cords):
    x1, y1 = cords
    x2, y2, w, h = rect_cords
    return x2 <= x1 <= x2 + w and y2 <= y1 <= y2 + h


def start_screen():
    # fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    # screen.blit(fon, (0, 0))

    screen.fill((0, 0, 0))
    pygame.display.flip()

    all_sprites = pygame.sprite.Group()

    pic_sprite = pygame.sprite.Sprite(all_sprites)
    pic_sprite_width, pic_sprite_height = [i * 0.8 for i in load_image("pic1.jpg").get_size()]
    pic_sprite.image = pygame.transform.scale(load_image("pic1.jpg"), (pic_sprite_width,
                                                                       pic_sprite_height))
    pic_sprite.rect = pic_sprite.image.get_rect()
    pic_sprite.rect.x = 270
    pic_sprite.rect.y = 60

    heading_sprite = pygame.sprite.Sprite(all_sprites)
    heading_sprite_width, heading_sprite_height = [i * 0.8 for i in load_image("heading.png").get_size()]
    heading_sprite.image = pygame.transform.scale(load_image("heading.png"), (heading_sprite_width,
                                                                              heading_sprite_height))
    heading_sprite.rect = heading_sprite.image.get_rect()
    heading_sprite.rect.x = 170
    heading_sprite.rect.y = 320

    start_sprite = pygame.sprite.Sprite(all_sprites)
    start_sprite.image = load_image("start.png")
    start_sprite.rect = start_sprite.image.get_rect()
    start_sprite.rect.x = 410
    start_sprite.rect.y = 510

    controls_sprite = pygame.sprite.Sprite(all_sprites)
    controls_sprite.image = load_image("controls.png")
    controls_sprite.rect = controls_sprite.image.get_rect()
    controls_sprite.rect.x = 360
    controls_sprite.rect.y = 560

    credit_sprite = pygame.sprite.Sprite(all_sprites)
    credit_sprite.image = load_image("credit.png")
    credit_sprite.rect = credit_sprite.image.get_rect()
    credit_sprite.rect.x = 400
    credit_sprite.rect.y = 610

    all_sprites.draw(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                cords = event.pos
                if is_in(cords, start_sprite.rect):
                    print('start')
                    return  # начинаем игру
                if is_in(cords, controls_sprite.rect):
                    print('controls')
                if is_in(cords, credit_sprite.rect):
                    print('credit')

        pygame.display.flip()
        clock.tick(FPS)


def game_screen():
    screen.fill((0, 0, 0))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()


start_screen()
game_screen()
