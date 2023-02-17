from constants import *


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


class Plaftorm(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('Project/img/platform.png')
        self.image = pygame.transform.scale(image, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.distance = 50
        self.counter = 0
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        if self.move_x:
            self.rect.x += self.direction
        elif self.move_y:
            self.rect.y += self.direction

        self.counter += 1

        if abs(self.counter >= 50):
            self.counter *= -1
            self.direction *= -1


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


blob_grp = pygame.sprite.Group()
lava_grp = pygame.sprite.Group()
exit_grp = pygame.sprite.Group()
coin_grp = pygame.sprite.Group()
shot_grp = pygame.sprite.Group()
platform_grp = pygame.sprite.Group()

dummy_coin = Coin(tile_size//2, tile_size//2)
coin_grp.add(dummy_coin)
