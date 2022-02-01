import os
import sys
import pygame

pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)


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


all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite(all_sprites)
sprite.image = load_image("creature.png")
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)
running = True
pygame.mouse.set_visible(False)
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                sprite.rect.x += 10
            elif event.key == pygame.K_LEFT:
                sprite.rect.x -= 10
            elif event.key == pygame.K_DOWN:
                sprite.rect.y += 10
            elif event.key == pygame.K_UP:
                sprite.rect.y -= 10
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
