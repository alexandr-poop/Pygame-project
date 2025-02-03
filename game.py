import os
import sys

import pygame
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

size = 900, 900
FPS = 50
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
sprite = pygame.display.set_mode(size)
win1 = pygame.display.set_mode(size)


def load_level(level):
    filename = "data/" + level + ".txt"
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["НАЖМИТЕ ЛЮБУЮ КНОПКУ",
                  "После этого введите название уровня из предложенных в консоль пайтон",
                  "ПРАВИЛА",
                  '1. Нужно дойти до клетки с сундуком, избегая ловушек;',
                  '2. Если натупить на ловушку, то игра заканчивается.  ']

    fon = pygame.transform.scale(load_image('fon.png'), (900, 900))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '!':
                Tile('spike', x, y)
            elif level[y][x] == '+':
                Tile('chest', x, y)
    return new_player, x, y


if __name__ == '__main__':
    pygame.init()
    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png'),
        'spike': load_image('spike.png'),
        'chest': load_image('chest.png')
    }
    player_image = load_image('mar.png')
    player = None
    start_screen()
    all_sprites = pygame.sprite.Group()
    fon2 = pygame.transform.scale(load_image('fon.png'), (900, 900))
    win = pygame.transform.scale(load_image('win.png'), (900, 900))
    sprite.blit(fon2, (0, 0))
    win1.blit(win, (0, 0))
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    level = input('Введите название уровня(map,level1,level2,level3):')
    tile_width = tile_height = 50
    level_map = load_level(level)
    max_width = len(level_map[0])
    max_height = len(level_map)
    size = width, height = max_width * tile_width, max_height * tile_height
    screen = pygame.display.set_mode(size)
    player, level_x, level_y = generate_level(level_map)

    pygame.display.set_caption('Game over')

    running = True
    while running:
        all_sprites.update()
        for event in pygame.event.get():
            x, y = player.pos
            if event.type == pygame.QUIT:
                terminate()
            if level_map[y][x] == '!':
                all_sprites.draw(sprite)
                pygame.display.flip()
            if level_map[y][x] == '+':
                all_sprites.draw(win1)
                pygame.display.flip()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if y > 0 and level_map[y - 1][x] != '#':
                        player.move(x, y - 1)
                if event.key == pygame.K_DOWN:
                    if y > 0 and level_map[y + 1][x] != '#':
                        player.move(x, y + 1)
                if event.key == pygame.K_LEFT:
                    if x > 0 and level_map[y][x - 1] != '#':
                        player.move(x - 1, y)
                if event.key == pygame.K_RIGHT:
                    if x > 0 and level_map[y][x + 1] != '#':
                        player.move(x + 1, y)
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()
    pygame.quit()
