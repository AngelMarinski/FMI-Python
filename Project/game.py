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
boss_coordinates = (reset_coordinates[0] + 650, 650)
menu = True
wepon_menu = True
level = 3
final_level = 3
score = 0
shot_damage = 100
is_won = False

# text section
font_score = pygame.font.SysFont('Bauhaus 93', 30)
text_col = (255, 255, 255)
game_over_color = (255, 0, 0)
font_game_over = pygame.font.SysFont('Bauhaus 93', 70)
win_color = (0, 255, 0)


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
        self.direction = 1
        self.in_air = False
        self.shot_cooldown = 30
        self.shot_counter = 30

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

    def boss_collision(self):
        global game_over, lifes
        if boss.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height) or boss.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height):
            game_over = -1
            lifes = 0

    def restart_game(self):
        global lifes, world, world_data, score, level, is_won
        score = 0
        lifes = 3
        level = 1
        world_data = []
        blob_grp.empty()
        lava_grp.empty()
        exit_grp.empty()
        coin_grp.empty()

        dummy_coin = Coin(tile_size//2, tile_size//2)
        coin_grp.add(dummy_coin)

        boss.rect.x, boss.rect.y = boss_coordinates
        boss.target_health = 500
        boss.current_health = 500
        is_won = False

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
        global level
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
            if key[pygame.K_SPACE] and level == final_level and self.shot_counter >= self.shot_cooldown:
                shot = Shot(pygame.image.load('Project/img/xl_shot.png'),
                            10, self.rect.x, self.rect.y, self.direction)

                shot_grp.add(shot)
                self.shot_counter = 0

            self.shot_counter += 1

            # gravity
            if self.velocity_y <= 10:
                self.velocity_y += 1

            ychange += self.velocity_y

            # check for collision
            xchange, ychange = self.collision(xchange, ychange)

            # check for enemy or lava collisions
            self.game_over_collisions()

            # check for collision with boss
            self.boss_collision()

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
        image_jump = pygame.image.load('Project/img/finalBossJump.png')
        self.image_jump_right = pygame.transform.scale(image_jump, (225, 325))
        self.image_jump_left = pygame.transform.flip(
            self.image_jump_right, True, False)
        self.image = self.img_left
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 650
        self.cooldown = 40
        self.counter = 0
        self.speed = 6
        self.velocity_y = 0
        self.velocity_x = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.in_air = False
        # health bar
        self.max_health = 500
        self.current_health = 500
        self.target_health = 500
        self.health_bar_length = 400
        self.health_bar_ration = self.max_health / self.health_bar_length
        self.health_change_speed = 5
        self.health_counter = 0

    def get_damage(self):
        global shot_damage, is_won
        if pygame.sprite.spritecollide(self, shot_grp, True):
            self.target_health -= shot_damage
            if self.target_health <= 0:
                self.target_health = 0
                is_won = True

    def advanced_health(self):
        global screen_width
        transition_width = 0
        transition_color = (255, 0, 0)

        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int(
                (self.target_health - self.current_health) / self.health_bar_ration)
            transition_color = (255, 255, 0)

        health_bar_rect = pygame.Rect(
            screen_width // 2 - 200, 70, self.current_health / self.health_bar_ration, 25)
        transition_bar_rect = pygame.Rect(
            health_bar_rect.right, 70, transition_width, 25)

        pygame.draw.rect(screen, (255, 0, 0), health_bar_rect)
        pygame.draw.rect(screen, transition_color, transition_bar_rect)
        pygame.draw.rect(screen, (255, 255, 255),
                         (screen_width // 2 - 200, 70, self.health_bar_length, 25), 4)

    def pos_towards_player(self, player_rect):
        c = math.sqrt((player_rect.x - 200 - self.rect.x) ** 2)
        try:
            x = (player_rect.x - self.rect.x) / c
        except ZeroDivisionError:
            return False
        return x

    def update(self):
        global screen_height
        dx, dy = 0, 0

        if self.pos_towards_player(player.rect) >= 0:
            if self.in_air:
                self.image = self.image_jump_right
            else:
                self.image = self.img_right
        else:
            if self.in_air:
                self.image = self.image_jump_left
            else:
                self.image = self.img_left

        if self.cooldown <= self.counter:
            if self.in_air == False:
                self.velocity_x = self.pos_towards_player(player.rect)
                self.velocity_y -= 20
                self.in_air = True
            if self.velocity_y <= 25:
                self.velocity_y += 0.2
            if self.rect.y == 650:
                self.in_air = False

            dy += self.velocity_y
            new_post = self.collision(self.velocity_x * self.speed, dy)
            dx = new_post[0]
            if new_post[2] == True:
                self.counter = 0
                dx = 0

            self.rect.x = self.rect.x + dx
            self.rect.y += new_post[1]
        else:
            self.counter += 1

        self.get_damage()
        self.advanced_health()
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

    def collision(self, xchange, ychange):
        landed = False
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + xchange, self.rect.y, self.width, self.height):
                xchange = 0
                self.velocity_x = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + ychange, self.width, self.height):
                if self.velocity_y >= 0:
                    ychange = tile[1].top - self.rect.bottom
                    if tile[1].top - self.rect.bottom <= 50:
                        landed = True
                    self.velocity_y = 0
                if self.velocity_y < 0:
                    ychange = tile[1].bottom - self.rect.top
                    self.velocity_y = 0

        return (xchange, ychange, landed)


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


class Shot(pygame.sprite.Sprite):
    def __init__(self, img, damage, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image_right = img
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.rect = self.image_right.get_rect()
        self.damage = damage
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.speed = 20

    def update(self):
        if self.direction > 0:
            self.image = self.image_right
        else:
            self.image = self.image_left

        self.rect.x += self.direction * self.speed


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
shot_grp = pygame.sprite.Group()

dummy_coin = Coin(tile_size//2, tile_size//2)
coin_grp.add(dummy_coin)

pickle_in = open(f'Project/level{level}_data', 'rb')
world_data = pickle.load(pickle_in)
world = World(world_data)

player = Player(reset_coordinates[0], reset_coordinates[1])
boss = Boss(reset_coordinates[0] + 650, reset_coordinates[1])
life = Life()
restart_button = Button(screen_width//2 - 50, screen_height //
                        2 + 100, pygame.image.load('Project/img/restart_btn.png'))
start_button = Button(screen_width // 2 - 350, screen_height //
                      2, pygame.image.load('Project/img/start_btn.png'))
exit_button = Button(screen_width // 2 - 20, screen_height //
                     2, pygame.image.load('Project/img/exit_btn.png'))

small_shot_card = Button(70, screen_height // 2 - 100,
                         pygame.image.load('Project/img/small_shot_card.png'))
medium_shot_card = Button(300, screen_height // 2 - 100,
                          pygame.image.load('Project/img/medium_shot_card.png'))
large_shot_card = Button(530, screen_height // 2 - 100,
                         pygame.image.load('Project/img/large_shot_card.png'))
xl_shot_card = Button(760, screen_height // 2 - 100,
                      pygame.image.load('Project/img/xl_shot_card.png'))


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
    elif level == final_level:
        world.draw()
        draw_text('X ' + str(score), font_score,
                  text_col, tile_size - 10, 10)
        coin_grp.draw(screen)

        if wepon_menu:
            small_shot_card.draw()
            medium_shot_card.draw()
            large_shot_card.draw()
            xl_shot_card.draw()
        else:
            if is_won == False:

                player.update()
                shot_grp.update()
                shot_grp.draw(screen)

                boss.update()

            elif lifes != 0:
                draw_text('YOU WIN!', font_game_over, win_color,
                          (screen_width // 2) - 140, screen_height // 2)
                if restart_button.draw():
                    player.restart_game()
    else:
        world.draw()

        life.update()
        blob_grp.update()
        blob_grp.draw(screen)
        lava_grp.draw(screen)
        exit_grp.draw(screen)
        coin_grp.draw(screen)

        player.update()

        draw_text('X ' + str(score), font_score, text_col, tile_size - 10, 10)

    if lifes == 0:
        draw_text('Game Over', font_game_over, game_over_color,
                  screen_width // 2 - 140, screen_height // 2)
        if restart_button.draw():
            player.restart_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()
