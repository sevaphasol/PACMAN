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
            elif self.state == "pause":
                self.pause_screen()
            elif self.state == "settings":
                self.settings_screen()
            self.clock.tick(FPS)
        terminate()

    def clear_screen(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def start_screen(self):
        self.clear_screen()

        all_sprites = pygame.sprite.Group()

        pic_sprite = pygame.sprite.Sprite(all_sprites)
        pic_sprite_image = load_image("pic1.jpg")
        pic_sprite_width, pic_sprite_height = [i * 0.8 for i in pic_sprite_image.get_size()]
        pic_sprite.image = pygame.transform.scale(pic_sprite_image, (pic_sprite_width,
                                                                     pic_sprite_height))
        pic_sprite.rect = pic_sprite.image.get_rect()
        pic_sprite.rect.x = 230
        pic_sprite.rect.y = 60

        heading_sprite = pygame.sprite.Sprite(all_sprites)
        heading_sprite_image = load_image("heading.png")
        heading_sprite_width, heading_sprite_height = [i * 0.8 for i in heading_sprite_image.get_size()]
        heading_sprite.image = pygame.transform.scale(heading_sprite_image, (heading_sprite_width,
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
                        self.state = "game"
                        return
                    elif is_in(cords, controls_sprite.rect):
                        self.state = "controls"
                        return
                    elif is_in(cords, credit_sprite.rect):
                        self.state = "credit"
                        return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.state = "game"
                        return

    def game_screen(self):
        self.clear_screen()

        fon = pygame.transform.scale(load_image("background.png"), (WIDTH - 100, HEIGHT - 100))
        self.screen.blit(fon, (50, 80))

        font = pygame.font.Font(None, 60)
        self.screen.blit(font.render("SCORE: 0", True, pygame.Color('white')), (60, 25))
        self.screen.blit(font.render("HIGH SCORE: 0", True, pygame.Color('white')), (450, 25))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "pause"
                        return

    def controls_screen(self):
        self.clear_screen()

        all_sprites = pygame.sprite.Group()

        back_btn_sprite = pygame.sprite.Sprite(all_sprites)
        back_btn_image = load_image("back_btn.png")
        back_btn_sprite_width, back_btn_sprite_height = [i * 0.2 for i in back_btn_image.get_size()]
        back_btn_sprite.image = pygame.transform.scale(back_btn_image, (back_btn_sprite_width,
                                                                        back_btn_sprite_height))
        back_btn_sprite.rect = back_btn_sprite.image.get_rect()
        back_btn_sprite.rect.x = 60
        back_btn_sprite.rect.y = 40

        all_sprites.draw(self.screen)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    cords = event.pos
                    if is_in(cords, back_btn_sprite.rect):
                        self.state = "start"
                        return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "start"
                        return

    def credit_screen(self):
        self.clear_screen()

        all_sprites = pygame.sprite.Group()

        back_btn_sprite = pygame.sprite.Sprite(all_sprites)
        back_btn_image = load_image("back_btn.png")
        back_btn_sprite_width, back_btn_sprite_height = [i * 0.2 for i in back_btn_image.get_size()]
        back_btn_sprite.image = pygame.transform.scale(back_btn_image, (back_btn_sprite_width,
                                                                        back_btn_sprite_height))
        back_btn_sprite.rect = back_btn_sprite.image.get_rect()
        back_btn_sprite.rect.x = 60
        back_btn_sprite.rect.y = 40

        all_sprites.draw(self.screen)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    cords = event.pos
                    if is_in(cords, back_btn_sprite.rect):
                        self.state = "start"
                        return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "start"
                        return

    def pause_screen(self):
        self.clear_screen()

        all_sprites = pygame.sprite.Group()

        back_btn_sprite = pygame.sprite.Sprite(all_sprites)
        back_btn_image = load_image("back_btn.png")
        back_btn_sprite_width, back_btn_sprite_height = [i * 0.2 for i in back_btn_image.get_size()]
        back_btn_sprite.image = pygame.transform.scale(back_btn_image, (back_btn_sprite_width,
                                                                        back_btn_sprite_height))
        back_btn_sprite.rect = back_btn_sprite.image.get_rect()
        back_btn_sprite.rect.x = 60
        back_btn_sprite.rect.y = 40

        menu_sprite = pygame.sprite.Sprite(all_sprites)
        menu_image = load_image("menu.png")
        menu_sprite_width, menu_sprite_height = [i * 0.8 for i in menu_image.get_size()]
        menu_sprite.image = pygame.transform.scale(menu_image, (menu_sprite_width,
                                                                menu_sprite_height))
        menu_sprite.rect = menu_sprite.image.get_rect()
        menu_sprite.rect.x = 360
        menu_sprite.rect.y = 380

        settings_sprite = pygame.sprite.Sprite(all_sprites)
        settings_image = load_image("settings.png")
        settings_sprite_width, settings_sprite_height = [i * 0.8 for i in settings_image.get_size()]
        settings_sprite.image = pygame.transform.scale(settings_image, (settings_sprite_width,
                                                                        settings_sprite_height))
        settings_sprite.rect = settings_sprite.image.get_rect()
        settings_sprite.rect.x = 300
        settings_sprite.rect.y = 520

        all_sprites.draw(self.screen)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    cords = event.pos
                    if is_in(cords, back_btn_sprite.rect):
                        self.state = "game"
                        return
                    elif is_in(cords, menu_sprite.rect):
                        self.state = "start"
                        return
                    elif is_in(cords, settings_sprite.rect):
                        self.state = "settings"
                        return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "game"
                        return

    def settings_screen(self):
        self.clear_screen()

        all_sprites = pygame.sprite.Group()

        back_btn_sprite = pygame.sprite.Sprite(all_sprites)
        back_btn_image = load_image("back_btn.png")
        back_btn_sprite_width, back_btn_sprite_height = [i * 0.2 for i in back_btn_image.get_size()]
        back_btn_sprite.image = pygame.transform.scale(back_btn_image, (back_btn_sprite_width,
                                                                        back_btn_sprite_height))
        back_btn_sprite.rect = back_btn_sprite.image.get_rect()
        back_btn_sprite.rect.x = 60
        back_btn_sprite.rect.y = 40

        all_sprites.draw(self.screen)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    cords = event.pos
                    if is_in(cords, back_btn_sprite.rect):
                        self.state = "pause"
                        return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "pause"
                        return


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
