import pygame.font

from default_commands import *


FPS = 50
WIDTH = 915
HEIGHT = 1005


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PACMAN")
        pygame.display.set_icon(pygame.image.load("data/icon.png"))
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "start"

    def run(self):
        while self.running:
            if self.state == "start":
                self.start_screen()
            elif self.state == "game":
                self.game_screen()
            elif self.state == "controls":
                self.controls_screen()
            elif self.state == "credit":
                self.credit_screen()
            self.clock.tick(FPS)
        terminate()

    def clear_screen(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def start_screen(self):
        self.clear_screen()

        all_sprites = pygame.sprite.Group()

        pic_sprite = pygame.sprite.Sprite(all_sprites)
        pic_sprite_width, pic_sprite_height = [i * 0.8 for i in load_image("pic1.jpg").get_size()]
        pic_sprite.image = pygame.transform.scale(load_image("pic1.jpg"), (pic_sprite_width,
                                                                           pic_sprite_height))
        pic_sprite.rect = pic_sprite.image.get_rect()
        pic_sprite.rect.x = 230
        pic_sprite.rect.y = 60

        heading_sprite = pygame.sprite.Sprite(all_sprites)
        heading_sprite_width, heading_sprite_height = [i * 0.8 for i in load_image("heading.png").get_size()]
        heading_sprite.image = pygame.transform.scale(load_image("heading.png"), (heading_sprite_width,
                                                                                  heading_sprite_height))
        heading_sprite.rect = heading_sprite.image.get_rect()
        heading_sprite.rect.x = 130
        heading_sprite.rect.y = 330

        start_sprite = pygame.sprite.Sprite(all_sprites)
        start_sprite.image = load_image("start.png")
        start_sprite.rect = start_sprite.image.get_rect()
        start_sprite.rect.x = 370
        start_sprite.rect.y = 530

        controls_sprite = pygame.sprite.Sprite(all_sprites)
        controls_sprite.image = load_image("controls.png")
        controls_sprite.rect = controls_sprite.image.get_rect()
        controls_sprite.rect.x = 320
        controls_sprite.rect.y = 590

        credit_sprite = pygame.sprite.Sprite(all_sprites)
        credit_sprite.image = load_image("credit.png")
        credit_sprite.rect = credit_sprite.image.get_rect()
        credit_sprite.rect.x = 360
        credit_sprite.rect.y = 650

        all_sprites.draw(self.screen)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    cords = event.pos
                    if is_in(cords, start_sprite.rect):
                        print('start')
                        self.state = "game"
                        return
                    if is_in(cords, controls_sprite.rect):
                        print('controls')
                        self.state = "controls"
                        return
                    if is_in(cords, credit_sprite.rect):
                        print('credit')
                        self.state = "credit"
                        return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print('start')
                        self.state = "game"
                        return

    def game_screen(self):
        self.clear_screen()

        fon = pygame.transform.scale(load_image("background.png"), (WIDTH - 100, HEIGHT - 100))
        self.screen.blit(fon, (50, 80))

        font = pygame.font.Font(None, 60)
        self.screen.blit(font.render("HIGH SCORE", True, pygame.Color('white')), (60, 25))
        self.screen.blit(font.render("0", True, pygame.Color('white')), (446, 25))
        self.screen.blit(font.render("0", True, pygame.Color('white')), (680, 25))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

    def controls_screen(self):
        self.clear_screen()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

    def credit_screen(self):
        self.clear_screen()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
