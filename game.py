import pygame
from pygame.locals import *
import sys
import const
from scenes import TitleScene

# TODO
# add more tools and moves
# add more maze obstacles
# rewrite frame update logic
# merge different icons

class GameWindow(object):

    def __init__(self, fullscreen=False):
        pygame.display.set_caption('SAWO')
        self.screen = pygame.display.set_mode((const.WIDTH*const.WSCALE, const.HEIGHT*const.HSCALE))
        self.game()

    def game(self):

        restart = True
        while restart:
            game = Game(self, self.screen)
            restart = game.loop()
        self.quit()

    def quit(self):
        pygame.quit()

class Game(object):
    def __init__(self, window, screen):
        self.window = window
        self.screen = screen
        self.restart = True
        self.timer = pygame.time.Clock()

    def loop(self):
        running = True
        manager = SceneMananger(self.screen)
        while(True):
            #self.timer.tick(60)
            # print type(manager.scene)
            if pygame.event.get(QUIT):
                running = False
                return
            running = manager.scene.loop()


class SceneMananger(object):
    def __init__(self, screen):
        #self.screen = screen
        self.go_to(TitleScene(screen))
        #self.go_to(StageChooseScene(screen))

    def go_to(self, scene):
        self.scene = scene
        self.scene.scene_manager = self
