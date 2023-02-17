from sprites import *
import pickle


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
                if tile == 4:
                    platform = Plaftorm(col_count * tile_size,
                                        row_count * tile_size, 1, 0)
                    platform_grp.add(platform)
                if tile == 5:
                    platform = Plaftorm(col_count * tile_size,
                                        row_count * tile_size, 0, 1)
                    platform_grp.add(platform)
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


pickle_in = open(f'Project/level{level}_data', 'rb')
world_data = pickle.load(pickle_in)
world = World(world_data)
