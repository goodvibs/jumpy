# Jumpy! - platformer
import pygame as pg
import random
from Settings import *
from Sprites import *
from os import path


class Game:
    def __init__(self):
        # Initialize PyGame and create game window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.waiting = True
        self.font1_name = pg.font.match_font("arial")

        # Load high score
        with open(path.join(THIS_FILE_dir, HIGH_SCORE_f), "r") as f:
            self.high_score = int(f.read())

        # Load spritesheet
        self.spritesheet = Spritesheet(path.join(SPRITESHEETS_dir, SPRITESHEET_f))

        self.score = None
        self.all_sprites = None
        self.platforms = None
        self.player = None
        self.playing = True
        self.final_position = None

    def new(self):
        # Start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for platform in PLATFORM_LIST:
            p = Platform(*platform)
            self.all_sprites.add(p)
            self.platforms.add(p)

        # Game loop
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        # Game loop - events
        for event in pg.event.get():
            # Check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def update(self):
        # Game loop - update
        self.all_sprites.update()
        # Check if player hits a platform while falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top + 1
                self.player.vel.y = 0
                if AUTO_JUMP:
                    self.player.jump()
        # Vertical scrolling if player moves to top 1/4 of the screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for platform in self.platforms:
                platform.rect.y += abs(self.player.vel.y)
                # Kill platforms off-screen
                if platform.rect.top >= HEIGHT:
                    platform.kill()
                    self.score += 10
        # When player dies
        if self.player.rect.bottom > HEIGHT:
            # self.final_velocity = 0
            # self.final_velocity += self.player.vel.y
            self.final_position = 0
            self.final_position += self.player.pos.x
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False
        # Spawn new platforms to maintain platform count
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            p = Platform(random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30),
                         width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def draw(self):
        # Game loop - draw
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), self.font1_name, 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()

    def show_start_screen(self):
        # Start screen
        while self.waiting:
            self.screen.fill(BG_COLOR)
            self.draw_text(TITLE, self.font1_name, 48, WHITE, WIDTH / 2, HEIGHT / 4)
            self.draw_text("ARROW KEYS or W and D to move", self.font1_name, 22, WHITE, WIDTH / 2, HEIGHT / 2)
            self.draw_text("Press any key to play", self.font1_name, 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
            self.draw_text("High score: " + str(self.high_score), self.font1_name, 22, WHITE, WIDTH / 2, 15)
            self.wait_for_key()
            pg.display.flip()

    def show_go_screen(self):
        # Game over screen
        if not self.running:
            return
        self.player.pos = vec(0, 0)
        self.player.pos.x += self.final_position
        self.player.vel = vec(0, 5)
        self.waiting = True
        while self.waiting:
            self.screen.fill(BG_COLOR)
            if self.player.pos.y > HEIGHT:
                self.player.kill()
            self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            self.draw_text("GAME OVER", self.font1_name, 48, WHITE, WIDTH / 2, HEIGHT / 4)
            self.draw_text("Score: " + str(self.score), self.font1_name, 22, WHITE, WIDTH / 2, HEIGHT / 2)
            self.draw_text("Press any key to play again", self.font1_name, 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
            if self.score >= self.high_score:
                self.high_score = self.score
                self.draw_text("NEW HIGH SCORE!", self.font1_name, 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
                with open(path.join(THIS_FILE_dir, HIGH_SCORE_f), "w") as f:
                    f.write(str(self.score))
            else:
                self.draw_text("High score: " + str(self.high_score), self.font1_name, 22, WHITE, WIDTH / 2,
                               HEIGHT / 2 + 40)
            self.wait_for_key()
            pg.display.flip()

    def wait_for_key(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.waiting = False
                self.running = False
            if event.type == pg.KEYUP:
                self.waiting = False

    def draw_text(self, text, fname, fsize, fcolor, x, y):
        font = pg.font.Font(fname, fsize)
        text_surface = font.render(text, True, fcolor)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
