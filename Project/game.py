import pygame
from pygame.locals import *

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
reset_coordinates = (100, screen_height - 130)

world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

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

        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.velocity_y = 0
        self.jump = False
        self.jump_count = 0
        self.walk_cooldown = 7
        self.direction = 0

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

        return (xchange, ychange)

    def game_over_collisions(self):
        global game_over
        if pygame.sprite.spritecollide(self, blob_grp, False):
            game_over += 1
        elif pygame.sprite.spritecollide(self, lava_grp, False):
            game_over += 1

    def update(self):
        xchange = 0
        ychange = 0

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
        if key[pygame.K_UP] and self.jump == False and self.jump_count < 2:
            self.velocity_y = -15
            self.jump_count += 1
            self.jumped = True
        if key[pygame.K_UP] == False:
            self.jumped = False
            self.jump_count = 0
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

        # update player
        self.rect.x += xchange
        self.rect.y += ychange

        # draw player
        screen.blit(self.image, self.rect)


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
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


blob_grp = pygame.sprite.Group()
lava_grp = pygame.sprite.Group()
world = World(world_data)
player = Player(reset_coordinates[0], reset_coordinates[1])

run = True

previous = 0

while run:

    clock.tick(fps)

    screen.blit(sky_img, (0, 0))
    screen.blit(sun_img, (100, 120))
    world.draw()

    blob_grp.update()
    blob_grp.draw(screen)
    lava_grp.draw(screen)

    player.update()

    if game_over != previous:
        player.rect.x, player.rect.y = reset_coordinates
        # fix dying animation
        # img_holder = player.image.copy()
        # alpha = 128
        # player.image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGB_MULT)
        # screen.blit(player.image, player.rect)
        #player.image = player.dead_img
        previous = game_over

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()
