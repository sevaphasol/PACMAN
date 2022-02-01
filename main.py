from default_commands import *


FPS = 50
WIDTH = 1000
HEIGHT = 1000


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

    def start_screen(self):
        self.screen.fill((0, 0, 0))
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
        heading_sprite.rect.y = 330

        start_sprite = pygame.sprite.Sprite(all_sprites)
        start_sprite.image = load_image("start.png")
        start_sprite.rect = start_sprite.image.get_rect()
        start_sprite.rect.x = 410
        start_sprite.rect.y = 530

        controls_sprite = pygame.sprite.Sprite(all_sprites)
        controls_sprite.image = load_image("controls.png")
        controls_sprite.rect = controls_sprite.image.get_rect()
        controls_sprite.rect.x = 360
        controls_sprite.rect.y = 590

        credit_sprite = pygame.sprite.Sprite(all_sprites)
        credit_sprite.image = load_image("credit.png")
        credit_sprite.rect = credit_sprite.image.get_rect()
        credit_sprite.rect.x = 400
        credit_sprite.rect.y = 650

        all_sprites.draw(self.screen)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
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

    def game_screen(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

    def controls_screen(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

    def credit_screen(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
