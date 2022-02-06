import pygame.font

from default_commands import *
from pprint import pprint

FPS = 60
WIDTH = 610
HEIGHT = 670
SPACE = 50
FON_WIDTH = WIDTH - SPACE
FON_HEIGHT = HEIGHT - SPACE
COLS = 28
ROWS = 30


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PACMAN")
        pygame.display.set_icon(pygame.image.load("data/icon.png"))
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "start"
        self.score = 0
        self.high_score = 0
        self.pix_w, self.pix_h = FON_WIDTH // COLS, FON_HEIGHT // ROWS
        self.pacman = Pacman(self)

    def run(self):
        while self.running:
            if self.state == "start":
                self.start_screen()
            elif self.state == "game":
                self.game_screen_events()
                self.game_screen_update()
                self.game_screen_draw()
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
        # draw
        self.clear_screen()

        all_sprites = pygame.sprite.Group()

        pic_sprite = pygame.sprite.Sprite(all_sprites)
        pic_sprite_image = load_image("pic1.jpg")
        pic_sprite_width, pic_sprite_height = [i * 0.5 for i in pic_sprite_image.get_size()]
        pic_sprite.image = pygame.transform.scale(pic_sprite_image, (pic_sprite_width,
                                                                     pic_sprite_height))
        pic_sprite.rect = pic_sprite.image.get_rect()
        pic_sprite.rect.x = 160
        pic_sprite.rect.y = 50

        heading_sprite = pygame.sprite.Sprite(all_sprites)
        heading_sprite_image = load_image("heading.png")
        heading_sprite_width, heading_sprite_height = [i * 0.5 for i in heading_sprite_image.get_size()]
        heading_sprite.image = pygame.transform.scale(heading_sprite_image, (heading_sprite_width,
                                                                             heading_sprite_height))
        heading_sprite.rect = heading_sprite.image.get_rect()
        heading_sprite.rect.x = 100
        heading_sprite.rect.y = 230

        start_sprite = pygame.sprite.Sprite(all_sprites)
        start_sprite_image = load_image("start.png")
        start_sprite_width, start_sprite_height = [i * 0.5 for i in start_sprite_image.get_size()]
        start_sprite.image = pygame.transform.scale(start_sprite_image, (start_sprite_width,
                                                                         start_sprite_height))
        start_sprite.rect = start_sprite.image.get_rect()
        start_sprite.rect.x = 260
        start_sprite.rect.y = 360

        controls_sprite = pygame.sprite.Sprite(all_sprites)
        controls_sprite_image = load_image("controls.png")
        controls_sprite_width, controls_sprite_height = [i * 0.5 for i in controls_sprite_image.get_size()]
        controls_sprite.image = pygame.transform.scale(controls_sprite_image, (controls_sprite_width,
                                                                               controls_sprite_height))
        controls_sprite.rect = controls_sprite.image.get_rect()
        controls_sprite.rect.x = 230
        controls_sprite.rect.y = 400

        credit_sprite = pygame.sprite.Sprite(all_sprites)
        credit_sprite_image = load_image("credit.png")
        credit_sprite_width, credit_sprite_height = [i * 0.5 for i in credit_sprite_image.get_size()]
        credit_sprite.image = pygame.transform.scale(credit_sprite_image, (credit_sprite_width,
                                                                           credit_sprite_height))
        credit_sprite.rect = credit_sprite.image.get_rect()
        credit_sprite.rect.x = 255
        credit_sprite.rect.y = 440

        all_sprites.draw(self.screen)

        # events
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
                pygame.display.flip()

    def game_screen_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "pause"
                elif event.key == pygame.K_LEFT:
                    self.pacman.move("left")
                elif event.key == pygame.K_UP:
                    self.pacman.move("up")
                elif event.key == pygame.K_RIGHT:
                    self.pacman.move("right")
                elif event.key == pygame.K_DOWN:
                    self.pacman.move("down")

    def game_screen_update(self):
        self.pacman.update()

    def game_screen_draw(self):
        fon = pygame.transform.scale(load_image("background.png"), (FON_WIDTH, FON_HEIGHT))

        for i in range(COLS):
            pygame.draw.line(fon, (100, 100, 100), (i * self.pix_w, 0),
                             (i * self.pix_w, HEIGHT))
        for i in range(ROWS):
            pygame.draw.line(fon, (100, 100, 100), (0, i * self.pix_h),
                             (WIDTH, i * self.pix_h))

        font = pygame.font.Font(None, 25)
        self.screen.blit(fon, (SPACE / 2, SPACE / 2))
        self.screen.blit(font.render(f"SCORE: {self.score}", True, pygame.Color('white')), (25, 8))
        self.screen.blit(font.render(f"HIGH SCORE: {self.high_score}", True, pygame.Color('white')), (325, 8))

        self.pacman.draw()
        pygame.display.flip()

    def controls_screen(self):
        self.clear_screen()

        all_sprites = pygame.sprite.Group()

        back_btn_sprite = pygame.sprite.Sprite(all_sprites)
        back_btn_image = load_image("back_btn.png")
        back_btn_sprite_width, back_btn_sprite_height = [i * 0.15 for i in back_btn_image.get_size()]
        back_btn_sprite.image = pygame.transform.scale(back_btn_image, (back_btn_sprite_width,
                                                                        back_btn_sprite_height))
        back_btn_sprite.rect = back_btn_sprite.image.get_rect()
        back_btn_sprite.rect.x = 50
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
        back_btn_sprite_width, back_btn_sprite_height = [i * 0.15 for i in back_btn_image.get_size()]
        back_btn_sprite.image = pygame.transform.scale(back_btn_image, (back_btn_sprite_width,
                                                                        back_btn_sprite_height))
        back_btn_sprite.rect = back_btn_sprite.image.get_rect()
        back_btn_sprite.rect.x = 50
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
        back_btn_sprite_width, back_btn_sprite_height = [i * 0.15 for i in back_btn_image.get_size()]
        back_btn_sprite.image = pygame.transform.scale(back_btn_image, (back_btn_sprite_width,
                                                                        back_btn_sprite_height))
        back_btn_sprite.rect = back_btn_sprite.image.get_rect()
        back_btn_sprite.rect.x = 50
        back_btn_sprite.rect.y = 40

        menu_sprite = pygame.sprite.Sprite(all_sprites)
        menu_image = load_image("menu.png")
        menu_sprite_width, menu_sprite_height = [i * 0.5 for i in menu_image.get_size()]
        menu_sprite.image = pygame.transform.scale(menu_image, (menu_sprite_width,
                                                                menu_sprite_height))
        menu_sprite.rect = menu_sprite.image.get_rect()
        menu_sprite.rect.x = 250
        menu_sprite.rect.y = 260

        settings_sprite = pygame.sprite.Sprite(all_sprites)
        settings_image = load_image("settings.png")
        settings_sprite_width, settings_sprite_height = [i * 0.5 for i in settings_image.get_size()]
        settings_sprite.image = pygame.transform.scale(settings_image, (settings_sprite_width,
                                                                        settings_sprite_height))
        settings_sprite.rect = settings_sprite.image.get_rect()
        settings_sprite.rect.x = 210
        settings_sprite.rect.y = 360

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
        back_btn_sprite_width, back_btn_sprite_height = [i * 0.15 for i in back_btn_image.get_size()]
        back_btn_sprite.image = pygame.transform.scale(back_btn_image, (back_btn_sprite_width,
                                                                        back_btn_sprite_height))
        back_btn_sprite.rect = back_btn_sprite.image.get_rect()
        back_btn_sprite.rect.x = 50
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


class Pacman:
    def __init__(self, game):
        self.game = game
        self.pos = [13, 29]
        self.pix_pos = [(self.pos[0] * self.game.pix_w) + SPACE / 2,
                        (self.pos[1] * self.game.pix_h) + SPACE / 2]
        self.state = None
        self.future_state = None
        self.v = 7
        self.player_sprites = pygame.sprite.Group()
        self.enemies_sprites = pygame.sprite.Group()

        self.left_image_opened = pygame.transform.scale(load_image("player1_left.png"), (self.game.pix_w,
                                                                                         self.game.pix_h))
        self.up_image_opened = pygame.transform.scale(load_image("player1_up.png"), (self.game.pix_w,
                                                                                     self.game.pix_h))
        self.right_image_opened = pygame.transform.scale(load_image("player1_right.png"), (self.game.pix_w,
                                                                                           self.game.pix_h))
        self.down_image_opened = pygame.transform.scale(load_image("player1_down.png"), (self.game.pix_w,
                                                                                         self.game.pix_h))
        self.left_image_closed = pygame.transform.scale(load_image("player2_left.png"), (self.game.pix_w,
                                                                                         self.game.pix_h))
        self.up_image_closed = pygame.transform.scale(load_image("player2_up.png"), (self.game.pix_w,
                                                                                     self.game.pix_h))
        self.right_image_closed = pygame.transform.scale(load_image("player2_right.png"), (self.game.pix_w,
                                                                                           self.game.pix_h))
        self.down_image_closed = pygame.transform.scale(load_image("player2_down.png"), (self.game.pix_w,
                                                                                         self.game.pix_h))

        self.player_sprite = pygame.sprite.Sprite(self.player_sprites)
        self.player_sprite_image = load_image("player2_right.png")
        self.player_sprite.image = self.right_image_closed
        self.player_sprite.rect = self.player_sprite.image.get_rect()
        self.player_sprite.rect.x, self.player_sprite.rect.y = self.pix_pos
        self.player_sprites.draw(self.game.screen)

    def update(self):
        if self.state == "left":
            self.player_sprite.image = self.left_image_closed
            self.pix_pos[0] -= self.game.pix_w / FPS * self.v
        elif self.state == "up":
            self.player_sprite.image = self.up_image_closed
            self.pix_pos[1] -= self.game.pix_h / FPS * self.v
        elif self.state == "right":
            self.player_sprite.image = self.right_image_closed
            self.pix_pos[0] += self.game.pix_w / FPS * self.v
        elif self.state == "down":
            self.player_sprite.image = self.down_image_closed
            self.pix_pos[1] += self.game.pix_h / FPS * self.v
        if self.future_state == "up" or self.future_state == "down":
            if (int(self.pix_pos[0]) - 5) % 20 == 0:
                self.state = self.future_state
        elif self.future_state == "left" or self.future_state == "right":
            if (int(self.pix_pos[1]) - 5) % 20 == 0:
                self.state = self.future_state
                self.future_state = None

    def draw(self):
        self.player_sprite.rect.x, self.player_sprite.rect.y = self.pix_pos
        self.player_sprites.draw(self.game.screen)

    def move(self, direction):
        if direction == "up" or direction == "down" and (int(self.pix_pos[0]) - 5) % 20 == 0:
            self.state = direction
        elif direction == "left" or direction == "right" and (int(self.pix_pos[1]) - 5) % 20 == 0:
            self.state = direction
        else:
            if not self.future_state:
                self.future_state = direction


if __name__ == "__main__":
    app = Game()
    app.run()
    pygame.quit()
    sys.exit()
