import pygame
from pygame.locals import *
from pygame import mixer
import pickle
import math
from constants import *
from sprites import *
from world import *
from buttons import *

clock = pygame.time.Clock()

pygame.display.set_caption('От девет планини в десетта')


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
        self.shot_img = fire_shot_img
        self.shot_dmg = fire_shot_damage

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

    def plaform_collision(self, xchange, ychange):
        collision = 20
        for platform in platform_grp:
            if platform.rect.colliderect(self.rect.x + xchange, self.rect.y, self.width, self.height):
                xchange = 0
            if platform.rect.colliderect(self.rect.x, self.rect.y + ychange, self.width, self.height):
                if abs((self.rect.top + ychange) - platform.rect.bottom) < collision:
                    self.velocity_y = 0
                    ychange = platform.rect.bottom - self.rect.top
                elif abs(self.rect.bottom + ychange - platform.rect.top) < collision:
                    self.rect.bottom = platform.rect.top - 1
                    self.in_air = False
                    ychange = 0
                if platform.move_x:
                    self.rect.x += platform.direction

        return (xchange, ychange)

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
        platform_grp.empty()

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
            game_over_fx.play()
        elif lifes != 0:
            self.reset()

    def is_coin_picked(self):
        global score
        if pygame.sprite.spritecollide(self, coin_grp, True):
            coin_fx.play()
            score += 1

    def level_passed(self):
        global level, world_data, world, weapon_menu
        if pygame.sprite.spritecollide(self, exit_grp, False):
            level += 1
            world_data = []
            blob_grp.empty()
            lava_grp.empty()
            exit_grp.empty()
            coin_grp.empty()
            coin_grp.add(dummy_coin)
            platform_grp.empty()

            if level == final_level:
                weapon_menu = True

            pickle_in = open(f'Project/level{level}_data', 'rb')
            world_data = pickle.load(pickle_in)
            world = World(world_data)
            self.reset()

    def update(self):
        global level, shot_damage
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
            if key[pygame.K_UP] and self.jump == False and self.in_air == False:
                jump_fx.play()
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
                shot = Shot(self.shot_img,
                            self.shot_dmg, self.rect.x, self.rect.y, self.direction)

                shot_grp.add(shot)
                shooting_fx.play()
                self.shot_counter = 0
                shot_damage = self.shot_dmg

            self.shot_counter += 1

            # gravity
            if self.velocity_y <= 10:
                self.velocity_y += 1

            ychange += self.velocity_y

            # check for collision
            xchange, ychange = self.collision(xchange, ychange)
            xchange, ychange = self.plaform_collision(xchange, ychange)
            # check for enemy or lava collisions
            self.game_over_collisions()

            # check for collision with boss
            if level == final_level:
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
        self.sound_counter = 0

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
                boss_jump_fx.play()
                self.velocity_x = self.pos_towards_player(player.rect)
                if self.velocity_x > 0:
                    self.velocity_x = self.velocity_x / 3
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


life = Life()

player = Player(reset_coordinates[0], reset_coordinates[1])
boss = Boss(reset_coordinates[0] + 650, reset_coordinates[1])

run = True


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

        if weapon_menu:
            draw_text('Choose your weapon:', font_game_over, game_over_color,
                      screen_width // 2 - 350, screen_height // 2 - 200)

            if weapon_menu_text:
                draw_text('Not enough coins!', font_game_over, game_over_color,
                          screen_width // 2 - 280, screen_height // 2 + 200)
            if small_shot_card.draw():
                if score < fire_shot_price:
                    weapon_menu_text = True
                else:
                    score -= fire_shot_price
                    player.shot_img = fire_shot_img
                    player.shot_dmg = fire_shot_damage
                    weapon_menu = False
                    weapon_menu_text = False
            if medium_shot_card.draw():
                if score < fire_blast_price:
                    weapon_menu_text = True
                else:
                    score -= fire_blast_price
                    player.shot_img = fire_blast_img
                    player.shot_dmg = fire_blast_damage
                    weapon_menu = False
                    weapon_menu_text = False
            if large_shot_card.draw():
                if score < fire_wave_price:
                    weapon_menu_text = True
                else:
                    score -= fire_wave_price
                    player.shot_img = fire_wave_img
                    player.shot_dmg = fire_wave_damage
                    weapon_menu = False
                    weapon_menu_text = False
            if xl_shot_card.draw():
                if score < fire_ball_price:
                    weapon_menu_text = True
                else:
                    score -= fire_ball_price
                    player.shot_img = fire_ball_img
                    player.shot_dmg = fire_ball_damage
                    weapon_menu = False
                    weapon_menu_text = False
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
        platform_grp.update()
        platform_grp.draw(screen)

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
