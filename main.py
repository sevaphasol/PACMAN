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
        self.player_start_pos = None
        self.score = 0
        self.high_score = 0
        self.pix_w, self.pix_h = FON_WIDTH // COLS, FON_HEIGHT // ROWS
        self.walls = []
        self.coins = []
        self.borders = pygame.sprite.Group()
        self.fon = pygame.transform.scale(load_image("background.png"), (FON_WIDTH, FON_HEIGHT))
        with open(file="walls.txt", mode='r') as f:
            for y, string in enumerate(f):
                for x, value in enumerate(string):
                    if value == "#":
                        self.walls.append([x, y])
                    elif value == "*":
                        self.coins.append([x, y])
                    elif value == "P":
                        self.player_start_pos = [x, y]
        self.pacman = Pacman(self)
        self.enemies = []
        for cords in self.walls:
            x, y = cords
            # pygame.draw.rect(fon, (255, 255, 255), (x * self.pix_w, y * self.pix_h, self.pix_w, self.pix_h), 2)
            border = pygame.sprite.Sprite(self.borders)
            border.image = pygame.transform.scale(load_image("border.png"), (self.pix_w, self.pix_h))
            border.rect = border.image.get_rect()
            border.rect.x = x * self.pix_w + SPACE//2
            border.rect.y = y * self.pix_h + SPACE//2
        self.borders.draw(self.screen)

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

    def make_enemies(self):
        pass

    def clear_screen(self):
        self.screen.fill((0, 0, 0))

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
                elif event.key == pygame.K_SPACE:
                    self.pacman.stop()

    def game_screen_update(self):
        self.pacman.update()

    def game_screen_draw(self):
        self.clear_screen()
        for i in range(COLS):
            pygame.draw.line(self.fon, (100, 100, 100), (i * self.pix_w, 0),
                             (i * self.pix_w, HEIGHT))
        for i in range(ROWS):
            pygame.draw.line(self.fon, (100, 100, 100), (0, i * self.pix_h),
                             (WIDTH, i * self.pix_h))

        font = pygame.font.Font(None, 25)
        self.screen.blit(self.fon, (SPACE / 2, SPACE / 2))
        self.screen.blit(font.render(f"SCORE: {self.pacman.current_score}", True, pygame.Color('white')), (25, 8))
        self.screen.blit(font.render(f"HIGH SCORE: {self.high_score}", True, pygame.Color('white')), (325, 8))

        self.coin_draw()
        self.pacman.draw()
        pygame.display.flip()

    def coin_draw(self):
        for cords in self.coins:
            x, y = cords
            pygame.draw.circle(self.screen, (167, 179, 34),
                               (x * self.pix_w + 10 + SPACE / 2, y * self.pix_h + 10 + SPACE / 2), 3)

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
        self.pos = self.game.player_start_pos
        self.pix_pos = [(self.pos[0] * self.game.pix_w) + SPACE // 2,
                        (self.pos[1] * self.game.pix_h) + SPACE // 2]
        self.state = None
        self.before_state = None
        self.future_state = None
        self.can_move = True
        self.v = 5
        self.current_score = 0

        self.start_time = pygame.time.get_ticks() // 100

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
        self.stop_image_closed = self.left_image_closed
        self.stop_image_opened = self.left_image_opened

        self.player_sprite = pygame.sprite.Sprite(self.player_sprites)
        self.player_sprite_image = load_image("player2_right.png")
        self.player_sprite.image = self.right_image_closed
        self.player_sprite.rect = self.player_sprite.image.get_rect()
        self.player_sprite.rect.x, self.player_sprite.rect.y = self.pix_pos
        self.player_sprites.draw(self.game.screen)

        self.directions = {"left": (0, -self.game.pix_w / FPS * self.v,
                                    [self.left_image_closed, self.left_image_opened]),
                           "up": (1, -self.game.pix_h / FPS * self.v,
                                  [self.up_image_closed, self.up_image_opened]),
                           "right": (0, self.game.pix_w / FPS * self.v,
                                     [self.right_image_closed, self.right_image_opened]),
                           "down": (1, self.game.pix_h / FPS * self.v,
                                    [self.down_image_closed, self.down_image_opened]),
                           None: (0, 0, [self.stop_image_closed, self.stop_image_opened])}

    def update(self):
        self.pos = [int((int(self.pix_pos[0]) - SPACE // 2) // self.game.pix_w),
                    int((int(self.pix_pos[1]) - SPACE // 2) // self.game.pix_h)]
        if self.on_coin():
            self.take_coin()
        axis, step, image = self.directions[self.state]
        self.pix_pos[axis] += step
        if (pygame.time.get_ticks() // 100 - self.start_time) % 3 == 0:
            self.player_sprite.image = image[0]
        else:
            self.player_sprite.image = image[1]
        if self.future_state:
            if (round(self.pix_pos[0], 2) + SPACE//2 - 10) % self.game.pix_w == 0:
                if self.future_state == "up" or self.future_state == "down":
                    self.state = self.future_state
                    self.can_move = self.able_to_move(self.pos, self.state)
                    if not self.can_move:
                        self.state = None
                        self.future_state = None

            if (round(self.pix_pos[1], 2) + SPACE//2 - 10) % self.game.pix_h == 0:
                if self.future_state == "right" or self.future_state == "left":
                    self.state = self.future_state
                    self.can_move = self.able_to_move(self.pos, self.state)
                    if not self.can_move:
                        self.state = None
                        self.future_state = None

    def draw(self):
        self.player_sprite.rect.x, self.player_sprite.rect.y = self.pix_pos
        self.player_sprites.draw(self.game.screen)

    def on_coin(self):
        if self.pos in self.game.coins:
            return True
        return False

    def take_coin(self):
        self.game.coins.remove(self.pos)
        self.current_score += 1

    def move(self, direction):
        self.future_state = direction

    def able_to_move(self, pos, direction):
        x, y = pos
        hits = pygame.sprite.spritecollide(self.player_sprite, self.game.borders, False)
        if hits:
            if direction == "left":
                x += 1
            elif direction == "up":
                y += 1
            self.pix_pos = [(x * self.game.pix_w) + SPACE // 2,
                            (y * self.game.pix_h) + SPACE // 2]
            return False
        return True

    def stop(self):
        if self.state:
            self.before_state = self.state
            self.pix_pos = [(self.pos[0] * self.game.pix_w) + SPACE // 2,
                            (self.pos[1] * self.game.pix_h) + SPACE // 2]
            self.state = False
        else:
            self.state = self.before_state


    class Ghost:
        pass


if __name__ == "__main__":
    app = Game()
    app.run()
    pygame.quit()
    sys.exit()
