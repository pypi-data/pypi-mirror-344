import subprocess
import os

MAIN_CONTENT ='''import pygame as pg
from settings import *
from utils import *
import sys

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        self.clock = pg.time.Clock()
        self.running = True

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def update(self):
        pg.display.flip()
        self.clock.tick(FPS)

    def render(self):
        self.screen.fill(BLACK)

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.render()
        pg.quit()
        sys.exit()



if __name__ == '__main__':
    app = Game()
    app.run()
'''

SETTINGS_CONTENT = '''TITLE = 'Game'
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
FPS = 60
'''

UTILS_CONTENT = 'BLACK = (0, 0, 0)'

def make_file(filename:str, content:str):
    with open(filename, 'w', encoding='UTF-8') as file:
        file.write(content)

def init_files():
    os.makedirs('assets', exist_ok=True)
    os.makedirs('assets/fonts', exist_ok=True)
    os.makedirs('assets/images', exist_ok=True)
    os.makedirs('assets/sounds', exist_ok=True)

    os.makedirs('src', exist_ok=True)
    os.makedirs('src/scenes', exist_ok=True)
    os.makedirs('src/scripts', exist_ok=True)
    os.makedirs('src/ui', exist_ok=True)

    make_file('src/main.py', MAIN_CONTENT)
    make_file('src/settings.py', SETTINGS_CONTENT)
    make_file('src/utils.py', UTILS_CONTENT)

def init_packages(packages:list):
    command = ['pip', 'install'] + packages
    try:
        subprocess.run(command, check=True)
        print(f"\nSuccessfully installed: {', '.join(packages)}\n")
    except subprocess.CalledProcessError as e:
        print(f"\nError installing packages: {', '.join(packages)}\n")
        print(e)