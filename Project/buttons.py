from constants import *


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
