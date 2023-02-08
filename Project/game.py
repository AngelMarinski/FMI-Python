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

        # update player
        self.rect.x += xchange
        self.rect.y += ychange

        if self.rect.bottom > screen_height - 40:
            self.rect.bottom = screen_height - 40
            ychange = 0

        # draw player
        screen.blit(self.image, self.rect)


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

                col_count += 1
            row_count += 1

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 2:
                    img = pygame.transform.scale(
                        grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


world = World(world_data)
player = Player(100, screen_height - 130)

run = True

while run:

    clock.tick(fps)

    screen.blit(sky_img, (0, 0))
    screen.blit(sun_img, (100, 120))

    world.draw()
    player.update()

#    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()
