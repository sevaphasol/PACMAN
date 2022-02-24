import pygame.font

from default_commands import *
from random import choice

FPS = 60
WIDTH = 610
HEIGHT = 670
SPACE = 50
FON_WIDTH = WIDTH - SPACE
FON_HEIGHT = HEIGHT - SPACE
COLS = 28
ROWS = 30


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

    def change_direction(self, direction):
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
    def __init__(self, game, pos, num):
        self.game = game
        self.num = num
        self.pos = pos
        self.pix_pos = [(self.pos[0] * self.game.pix_w) + SPACE // 2,
                        (self.pos[1] * self.game.pix_h) + SPACE // 2]
        self.state = None
        self.v = num + 1
        self.target = None
        self.stage = 1
        self.paths = [{"right": [13, 13], "up": [13, 11], "left": [12, 11]},
                      {"left": [14, 13], "up": [14, 11], "right": [15, 11]},
                      {"right": [13, 15], "up": [13, 11], "left": [12, 11]},
                      {"left": [14, 15], "up": [14, 11], "right": [15, 11]}]
        self.path = self.paths[num - 1]
        self.directions = {"left": (0, -self.game.pix_w / FPS * self.v,),
                           "up": (1, -self.game.pix_h / FPS * self.v,),
                           "right": (0, self.game.pix_w / FPS * self.v,),
                           "down": (1, self.game.pix_h / FPS * self.v,),
                           None: (0, 0)}
        self.vector_directions = {(-1, 0): "left", (0, 1): "up", (1, 0): "right", (0, -1): "down"}
        self.home_cords = [[11, 13], [12, 13], [13, 13], [14, 13], [15, 13], [16, 13], [11, 14], [12, 14], [13, 14],
                           [14, 14], [15, 14], [16, 14], [11, 15], [12, 15], [13, 15], [14, 15], [15, 15], [16, 15],
                           [13, 12], [14, 12], [12, 11], [13, 11], [14, 11], [15, 11], [13, 10], [11, 11], [12, 10]]
        self.ghost_sprite = pygame.sprite.Sprite(self.game.ghost_sprites)
        ghost_sprite_image = load_image(f"ghost{num}.png")
        ghost_sprite_width, ghost_sprite_height = [i * 0.04 for i in ghost_sprite_image.get_size()]
        self.ghost_sprite.image = pygame.transform.scale(ghost_sprite_image, (ghost_sprite_width,
                                                                              ghost_sprite_height))
        self.ghost_sprite.rect = self.ghost_sprite.image.get_rect()
        self.ghost_sprite.rect.x, self.ghost_sprite.rect.y = self.pix_pos
        self.game.ghost_sprites.draw(self.game.screen)

    def update(self):
        if self.stage != 4:
            self.go_out_of_the_home()
        else:
            if not self.able_to_move(self.pos, self.state):
                self.change_direction()
        axis, step = self.directions[self.state]
        self.pix_pos[axis] += step
        self.pos = [int((int(self.pix_pos[0]) - SPACE // 2) // self.game.pix_w),
                    int((int(self.pix_pos[1]) - SPACE // 2) // self.game.pix_h)]
        self.draw()

    def draw(self):
        self.ghost_sprite.rect.x, self.ghost_sprite.rect.y = self.pix_pos
        self.game.ghost_sprites.draw(self.game.screen)

    def go_out_of_the_home(self):
        time = pygame.time.get_ticks() // 1000 - self.game.start_time
        if self.num == 1 and time > 1:
            if self.stage == 1:
                if self.pos != [13, 13]:
                    self.state = "right"
                else:
                    self.stage = 2
            elif self.stage == 2:
                if self.pos != [13, 10]:
                    self.state = "up"
                else:
                    if (round(self.pix_pos[1], 2) + SPACE // 2 - 10) % self.game.pix_h == 0:
                        self.stage = 3
            elif self.stage == 3:
                if self.pos != [12, 10]:
                    self.state = "left"
                else:
                    if (round(self.pix_pos[0], 2) + SPACE // 2 - 10) % self.game.pix_w == 0:
                        self.stage = 4
                        self.state = None
                        self.pos = [12, 11]
                        self.pix_pos = [(self.pos[0] * self.game.pix_w) + SPACE // 2,
                                        (self.pos[1] * self.game.pix_h) + SPACE // 2]

        elif self.num == 2 and time > 3:
            if self.stage == 1:
                if self.pos != [13, 13]:
                    self.state = "left"
                else:
                    self.stage = 2
            elif self.stage == 2:
                if self.pos != [13, 11]:
                    self.state = "up"
                else:
                    if (round(self.pix_pos[1], 2) + SPACE // 2 - 10) % self.game.pix_h == 0:
                        self.stage = 3
            elif self.stage == 3:
                if self.pos != [15, 10]:
                    self.state = "right"
                else:
                    if (round(self.pix_pos[0], 2) + SPACE // 2 - 10) % self.game.pix_w == 0:
                        self.stage = 4
                        self.state = None
                        self.pos = [15, 11]
                        self.pix_pos = [(self.pos[0] * self.game.pix_w) + SPACE // 2,
                                        (self.pos[1] * self.game.pix_h) + SPACE // 2]

        elif self.num == 3 and time > 7:
            if self.stage == 1:
                if self.pos != [13, 15]:
                    self.state = "right"
                else:
                    self.stage = 2
            elif self.stage == 2:
                if self.pos != [13, 11]:
                    self.state = "up"
                else:
                    if (round(self.pix_pos[1], 2) + SPACE // 2 - 10) % self.game.pix_h == 0:
                        self.stage = 3
            elif self.stage == 3:
                if self.pos != [11, 10]:
                    self.state = "left"
                else:
                    if (round(self.pix_pos[0], 2) + SPACE // 2 - 10) % self.game.pix_w == 0:
                        self.stage = 4
                        self.state = None
                        self.pos = [12, 11]
                        self.pix_pos = [(self.pos[0] * self.game.pix_w) + SPACE // 2,
                                        (self.pos[1] * self.game.pix_h) + SPACE // 2]

        elif self.num == 4 and time > 11:
            if self.stage == 1:
                if self.pos != [13, 15]:
                    self.state = "left"
                else:
                    self.stage = 2
            elif self.stage == 2:
                if self.pos != [13, 10]:
                    self.state = "up"
                else:
                    if (round(self.pix_pos[1], 2) + SPACE // 2 - 10) % self.game.pix_h == 0:
                        self.stage = 3
            elif self.stage == 3:
                if self.pos != [14, 10]:
                    self.state = "right"
                else:
                    if (round(self.pix_pos[0], 2) + SPACE // 2 - 10) % self.game.pix_w == 0:
                        self.stage = 4
                        self.state = None
                        self.pos = [15, 11]
                        self.pix_pos = [(self.pos[0] * self.game.pix_w) + SPACE // 2,
                                        (self.pos[1] * self.game.pix_h) + SPACE // 2]
                        self.game.walls.extend(self.game.doors)
                        border = pygame.sprite.Sprite(self.game.borders)
                        border.image = pygame.transform.scale(load_image("border2.png"), (self.game.pix_w,
                                                                                          self.game.pix_h))
                        border.rect = border.image.get_rect()
                        border.rect.x = 12 * self.game.pix_w + SPACE // 2
                        border.rect.y = 11 * self.game.pix_h + SPACE // 2
                        self.game.borders.draw(self.game.fon)

    def able_to_move(self, pos, direction):
        if not self.state:
            return False
        x, y = pos
        hits = pygame.sprite.spritecollide(self.ghost_sprite, self.game.borders, False)
        if hits:
            if direction == "left":
                x += 1
            elif direction == "up":
                y += 1
            self.pix_pos = [(x * self.game.pix_w) + SPACE // 2,
                            (y * self.game.pix_h) + SPACE // 2]
            return False
        return True

    def change_direction(self):
        self.state = choice(["left", "up", "right", "down"])

    def set_target(self):
        return self.game.pacman.pos

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        x = next_cell[0] - self.pos[0]
        y = next_cell[1] - self.pos[1]
        return self.vector_directions[(x, y)]

    def find_next_cell_in_path(self, target):
        path = self.bfs([int(self.pos[0]), int(self.pos[1])], [
                        int(target[0]), int(target[1])])
        return path[1]

    def bfs(self, start, target):
        grid = [[0 for _ in range(28)] for _ in range(30)]
        for cell in self.game.walls:
            if cell[0] < 28 and cell[1] < 30:
                grid[int(cell[1])][int(cell[0])] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if len(grid[0]) > neighbour[0] + current[0] >= 0:
                        if len(grid) > neighbour[1] + current[1] >= 0:
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PACMAN")
        pygame.display.set_icon(pygame.image.load("data/icon.png"))
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.start_time = None
        self.running = True
        self.state = "start"
        self.player_start_pos = None
        self.ghost_poses = []
        self.score = 0
        self.high_score = 0
        self.pix_w, self.pix_h = FON_WIDTH // COLS, FON_HEIGHT // ROWS
        self.walls = []
        self.doors = []
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
                    elif value in ["1", "2", "3", "4"]:
                        self.ghost_poses.append([x, y])
                    elif value == "D":
                        pygame.draw.rect(self.fon, (0, 0, 0), (x*self.pix_w, y*self.pix_h, self.pix_w, self.pix_h))
                        self.doors.append([x, y])
        self.pacman = Pacman(self)
        self.ghosts = []
        self.ghost_sprites = pygame.sprite.Group()
        self.make_ghosts()
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
                if not self.start_time:
                    self.start_time = pygame.time.get_ticks() // 1000
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

    def make_ghosts(self):
        for i in range(len(self.ghost_poses)):
            self.ghosts.append(Ghost(self, self.ghost_poses[i], i + 1))

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
                    self.pacman.change_direction("left")
                elif event.key == pygame.K_UP:
                    self.pacman.change_direction("up")
                elif event.key == pygame.K_RIGHT:
                    self.pacman.change_direction("right")
                elif event.key == pygame.K_DOWN:
                    self.pacman.change_direction("down")
                elif event.key == pygame.K_SPACE:
                    self.pacman.stop()

    def game_screen_update(self):
        self.pacman.update()
        for ghost in self.ghosts:
            ghost.update()

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
        for ghost in self.ghosts:
            ghost.draw()
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


if __name__ == "__main__":
    app = Game()
    app.run()
    pygame.quit()
    sys.exit()
