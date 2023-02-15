import pygame
from pygame.locals import *
import pickle
import math

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('От девет планини в десетта')

# load image (move to assets)
sun_img = pygame.image.load('Project/img/sun.png')
sky_img = pygame.image.load('Project/img/sky.png')

# game
tile_size = 50
game_over = 0
lifes = 3
reset_coordinates = (100, screen_height - 130)
menu = True
level = 3
score = 0

# text section
font_score = pygame.font.SysFont('Bauhaus 93', 30)
text_col = (255, 255, 255)
game_over_color = (255, 0, 0)
font_game_over = pygame.font.SysFont('Bauhaus 93', 70)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# draw grid for better understanding
def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line *
                         tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line *
                         tile_size, 0), (line * tile_size, screen_height))


class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.count = 0

        for index in range(1, 5):
            img_right = pygame.image.load(f'Project/img/guy{index}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_left.append(img_left)
            self.images_right.append(img_right)

        self.dead_image = pygame.image.load('Project/img/ghost.png')
        self.image = self.images_right[self.index]
        self.safe_player_img = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.velocity_y = 0
        self.jump = False
        self.walk_cooldown = 7
        self.direction = 0
        self.in_air = False

    def animation(self):
        if self.count >= self.walk_cooldown:
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0

            if self.direction > 0:
                self.image = self.images_right[self.index]
                self.count = 0
            elif self.direction < 0:
                self.image = self.images_left[self.index]
                self.count = 0
        else:
            self.count += 1

    def collision(self, xchange, ychange):
        self.in_air = True
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + xchange, self.rect.y, self.width, self.height):
                xchange = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + ychange, self.width, self.height):
                if self.velocity_y < 0:
                    ychange = tile[1].bottom - self.rect.top
                    self.velocity_y = 0
                elif self.velocity_y >= 0:
                    ychange = tile[1].top - self.rect.bottom
                    self.velocity_y = 0
                    self.in_air = False

        return (xchange, ychange)

    def restart_game(self):
        global lifes, world, world_data, score, level
        score = 0
        lifes = 3
        level = 1
        world_data = []
        blob_grp.empty()
        lava_grp.empty()
        exit_grp.empty()
        coin_grp.empty()
        pickle_in = open(f'Project/level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
        world = World(world_data)
        self.reset()

    def game_over_collisions(self):
        global game_over
        global lifes
        if pygame.sprite.spritecollide(self, blob_grp, False):
            game_over = -1
            lifes -= 1
        elif pygame.sprite.spritecollide(self, lava_grp, False):
            game_over = -1
            lifes -= 1

    def reset(self):
        global game_over
        self.image = self.safe_player_img
        game_over = 0
        self.rect.x, self.rect.y = reset_coordinates
        self.direction = 0

    def game_over_animation(self):
        global lifes
        self.image = self.dead_image

        if self.rect.y > 100:
            self.rect.y -= 5
        elif lifes != 0:
            self.reset()

    def is_coin_picked(self):
        global score
        if pygame.sprite.spritecollide(self, coin_grp, True):
            score += 1

    def level_passed(self):
        global level, world_data, world
        if pygame.sprite.spritecollide(self, exit_grp, False):
            level += 1
            world_data = []
            blob_grp.empty()
            lava_grp.empty()
            exit_grp.empty()
            coin_grp.empty()

            print(level)

            pickle_in = open(f'Project/level{level}_data', 'rb')
            world_data = pickle.load(pickle_in)
            world = World(world_data)
            self.reset()

    def update(self):
        xchange = 0
        ychange = 0

        if game_over == 0:
            # get keys
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                xchange -= 5
                self.direction = -1
                self.animation()
            if key[pygame.K_RIGHT]:
                xchange += 5
                self.direction = 1
                self.animation()
            if key[pygame.K_UP] and self.jump == False:
                # and self.in_air == False:
                self.velocity_y = -15
                self.jumped = True
            if key[pygame.K_UP] == False:
                self.jumped = False
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.count = 0
                self.index = 0
                if self.direction > 0:
                    self.image = self.images_right[self.index]
                elif self.direction < 0:
                    self.image = self.images_left[self.index]

            # gravity
            if self.velocity_y <= 10:
                self.velocity_y += 1

            ychange += self.velocity_y

            # check for collision
            xchange, ychange = self.collision(xchange, ychange)

            # check for enemy or lava collisions
            self.game_over_collisions()
            self.level_passed()
            self.is_coin_picked()
            # update player
            self.rect.x += xchange
            self.rect.y += ychange

        elif game_over == -1:
            self.game_over_animation()

        # draw player
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)


class Boss():
    def __init__(self, x, y):
        img_right = pygame.image.load('Project/img/FinalBoss.png')
        self.img_right = pygame.transform.scale(img_right, (200, 300))
        self.img_left = pygame.transform.flip(self.img_right, True, False)
        self.rect = self.img_left.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.cooldown = 15
        self.speed = 2
        self.velocity_y = 0
        self.width = self.img_right.get_width()
        self.height = self.img_right.get_height()

    def pos_towards_player(self, player_rect):
        c = math.sqrt((player_rect.x - self.rect.x) ** 2 +
                      (player_rect.y - self.rect.y - 300) ** 2)
        try:
            x = (player_rect.x - self.rect.x) / c
            y = ((player_rect.y - self.rect.y) / c)
            # - self.distance_above_player)
        except ZeroDivisionError:
            return False
        return (x, 0)

    def update(self):
        global screen_height
        position = self.pos_towards_player(player.rect)

        if position:
            new_post = self.collision(position[0], position[1])
            self.rect.x = self.rect.x + new_post[0] * self.speed
            self.rect.y = screen_height - 340

        screen.blit(self.img_left, self.rect)

    def collision(self, xchange, ychange):
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + ychange, self.width, self.height):
                if self.velocity_y < 0:
                    ychange = tile[1].bottom - self.rect.top
                    self.velocity_y = 0
                elif self.velocity_y >= 0:
                    print(f"self bottom {self.rect.bottom}")
                    print(f"tile top {tile[1].top}")
                    ychange = tile[1].top - self.rect.bottom
                    self.velocity_y = 0

        print(ychange)
        return (xchange, ychange)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Project/img/blob.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.distance = 50
        self.counter = 0

    def update(self):
        self.rect.x += self.direction
        self.counter += 1

        if abs(self.counter >= 50):
            self.counter *= -1
            self.direction *= -1


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('Project/img/lava.png')
        self.image = pygame.transform.scale(image, (tile_size, tile_size//2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('Project/img/exit.png')
        self.image = pygame.transform.scale(
            image, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('Project/img/coin.png')
        self.image = pygame.transform.scale(
            image, (tile_size//2, tile_size//2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Life:
    def __init__(self):
        full_heart = pygame.image.load('Project/img/heart.png')
        empty_heart = pygame.image.load('Project/img/empty_heart.png')
        self.full_heart_img = pygame.transform.smoothscale(
            full_heart, (50, 50))
        self.empty_heart_img = pygame.transform.smoothscale(
            empty_heart, (50, 50))

    def update(self):
        global lifes

        positionX = 60
        positionY = 50
        total_lifes = 3
        for index in range(0, lifes):
            screen.blit(self.full_heart_img, (positionX, positionY))
            positionX += 70

        for index in range(0, total_lifes - lifes):
            screen.blit(self.empty_heart_img, (positionX, positionY))
            positionX += 70


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        global lifes, game_over
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                # lifes = 3
                # player.reset()
                return True

        screen.blit(self.image, self.rect)
        return False


class World:
    def __init__(self, data):
        self.tile_list = []

        dirt_img = pygame.image.load('Project/img/dirt.png')
        grass_img = pygame.image.load('Project/img/grass.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(
                        dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                if tile == 2:
                    img = pygame.transform.scale(
                        grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                if tile == 3:
                    blob = Enemy(col_count * tile_size,
                                 row_count * tile_size + 15)
                    blob_grp.add(blob)
                if tile == 6:
                    lava = Lava(col_count * tile_size,
                                row_count * tile_size + (tile_size // 2))
                    lava_grp.add(lava)
                if tile == 7:
                    coin = Coin(col_count * tile_size + (tile_size // 2),
                                row_count * tile_size + (tile_size // 2))
                    coin_grp.add(coin)

                if tile == 8:
                    exit = Exit(col_count * tile_size,
                                row_count * tile_size - tile_size // 2)
                    exit_grp.add(exit)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


blob_grp = pygame.sprite.Group()
lava_grp = pygame.sprite.Group()
exit_grp = pygame.sprite.Group()
coin_grp = pygame.sprite.Group()

dummy_coin = Coin(tile_size//2, tile_size//2)
coin_grp.add(dummy_coin)

pickle_in = open(f'Project/level{level}_data', 'rb')
world_data = pickle.load(pickle_in)
world = World(world_data)

player = Player(reset_coordinates[0], reset_coordinates[1])
boss = Boss(reset_coordinates[0] + 700, reset_coordinates[1])
life = Life()
restart_button = Button(screen_width//2 - 50, screen_height //
                        2 + 100, pygame.image.load('Project/img/restart_btn.png'))
start_button = Button(screen_width // 2 - 350, screen_height //
                      2, pygame.image.load('Project/img/start_btn.png'))
exit_button = Button(screen_width // 2 - 20, screen_height //
                     2, pygame.image.load('Project/img/exit_btn.png'))


run = True

previous = 0

while run:

    clock.tick(fps)

    screen.blit(sky_img, (0, 0))
    screen.blit(sun_img, (100, 120))

    if menu:
        if exit_button.draw():
            run = False
        if start_button.draw():
            menu = False
    elif level == 3:
        world.draw()

        life.update()
        player.update()
        boss.update()
    else:
        world.draw()

        life.update()
        blob_grp.update()
        blob_grp.draw(screen)
        lava_grp.draw(screen)
        exit_grp.draw(screen)
        coin_grp.draw(screen)

        player.update()

        if lifes == 0:
            draw_text('Game Over', font_game_over, game_over_color,
                      screen_width // 2 - 140, screen_height // 2)
            if restart_button.draw():
                player.restart_game()

        draw_text('X ' + str(score), font_score, text_col, tile_size - 10, 10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()
