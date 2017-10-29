import pygame
from pygame.locals import *

import sys
import const
class GameWindow(object):

    def __init__(self, fullscreen=False):
        pygame.display.set_caption('SAWO')
        self.screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
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
            print type(manager.scene)
            if pygame.event.get(QUIT):
                running = False
                return
            running = manager.scene.loop()


class SceneMananger(object):
    def __init__(self, screen):
        self.screen = screen
        self.go_to(TitleScene(screen))

    def go_to(self, scene):
        self.scene = scene
        self.scene.scene_manager = self



class TitleScene(object):

    def __init__(self, screen):
        super(TitleScene, self).__init__()
        self.screen = screen
        self.running = True
        self.font = pygame.font.SysFont('Arial', 56)
        self.bg = pygame.image.load('image/bg.png').convert_alpha()

    def loop(self):

        text1 = self.font.render('123', True, (255, 255, 255))
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(text1, (50, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.on_keydown(event)
        pygame.display.flip()


        return True

    def update(self):
        pass

    def on_keydown(self, event):
        self.scene_manager.go_to(Scene(self.screen))
        self.running = False




class Scene(object):

    def __init__(self, screen):
        # self.window = window
        self.real_screen = screen
        self.running = True
        initial_pos = (const.REAL_WIDTH / 2 - 50, 40)
        self.clock = pygame.time.Clock()
        self.icons = []
        # self.scene_manager = scene_manager
        self.mouse_interactable = []

        self.icon_bar = Icon_bar((10, 20))
        self.character_timeline = Character_timeline((50, 300))


        self.character = Character(initial_pos, self)
        self.maze = Maze((80, 30), self, 1)
        self.return_layer = Return_layer((40, 40))

        self.mouse_interactable.append(self.return_layer)


        self.timeline_pointer = Timeline_pointer(self.character, self.character_timeline)


        self.screen = pygame.surface.Surface((const.REAL_WIDTH, const.REAL_HEIGHT))




    def loop(self):
        self.bg = pygame.image.load('image/bg.png').convert_alpha()
        self.screen.blit(self.bg, (0, 0))

        while self.running:

            # event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.on_keydown(event)
                elif event.type == pygame.KEYUP:
                    self.on_keyup(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_mousedown(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.on_mouseup(event)

            # render

            # clear

            for icon in self.icons:
                icon.con.clear(self.screen, self.bg)
            self.icon_bar.con.clear(self.screen, self.bg)
            self.character_timeline.con.clear(self.screen, self.bg)
            self.timeline_pointer.con.clear(self.screen, self.bg)
            self.maze.con.clear(self.screen, self.bg)
            for ob in self.maze.maze:
                ob.con.clear(self.screen, self.bg)
            self.character.con.clear(self.screen, self.bg)
            self.return_layer.con.clear(self.screen, self.bg)
            # update

            dt = self.clock.tick(const.FPS) / 1000.0

            for icon in self.icons:
                icon.con.update(dt)
            self.icon_bar.con.update(dt)
            self.character_timeline.con.update(dt)
            self.timeline_pointer.con.update(dt)
            self.maze.con.update(dt)
            for ob in self.maze.maze:
                ob.con.update(dt)
            self.character.con.update(self.maze, dt)
            self.return_layer.con.update(dt)


            # draw
            update_rects = []

            update_rects += self.icon_bar.con.draw(self.screen)
            update_rects += self.character_timeline.con.draw(self.screen)

            update_rects += self.maze.con.draw(self.screen)
            for ob in self.maze.maze:
                update_rects += ob.con.draw(self.screen)
            update_rects += self.timeline_pointer.con.draw(self.screen)
            update_rects += self.character.con.draw(self.screen)
            for icon in self.icons:
                update_rects += icon.con.draw(self.screen)
            update_rects += self.return_layer.con.draw(self.screen)

            # scaling and updating
            #scaled_update_rects = [pygame.Rect(2*r.left - 4, 2*r.top - 4, 2*r.width + 8, 2*r.height + 8) for r in update_rects]
            pygame.transform.scale(self.screen, (const.WIDTH, const.HEIGHT), self.real_screen)
            #pygame.display.update(scaled_update_rects)
            pygame.display.update(update_rects)

        return self.running

    def on_keyup(self, event):
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.character.stop_left()
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.character.stop_right()
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.character.stop_up()
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.character.stop_down()


    def on_keydown(self, event):
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.character.move_left()
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.character.move_right()

        elif event.key == pygame.K_SPACE:
            self.timeline_pointer.toggle_pause()
            self.character.toggle_pause()

        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.character.move_up()
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.character.move_down()
        elif event.key == pygame.K_r:
            self.character_timeline.reset()
            self.timeline_pointer.reset()
            self.maze.reset()
            self.character.reset()



    def on_mouseup(self, event):
        for item in self.mouse_interactable:
            if isinstance(item, Move_icon):
                if item.is_drag == True:
                    if item.rect.colliderect(self.character_timeline):
                        item.is_drag = False
                        item.off_set_x = 0
                        item.off_set_y = 0
                        item.pos[1] = 300 # y pos of timeline
                        if item in self.icon_bar.icons:
                            self.icon_bar.remove_icon(item)
                        elif item in self.character_timeline.moves:
                            self.character_timeline.remove_move(item)
                        self.character_timeline.add_move(item, item.pos[0])
                    elif item.rect.colliderect(self.icon_bar):
                        item.is_drag = False
                        item.off_set_x = 0
                        item.off_set_y = 0
                        if item in self.icon_bar.icons:
                            self.icon_bar.remove_icon(item)
                        elif item in self.character_timeline.moves:
                            self.character_timeline.remove_move(item)
                        self.icon_bar.add_icon(item)
                    else:
                        item.is_drag = False
                        item.off_set_x = 0
                        item.off_set_y = 0
                        item.pos = [item.original_pos[0], item.original_pos[1]]


    def on_mousedown(self, event):
        for item in self.mouse_interactable:
            if item.rect.collidepoint(event.pos) and isinstance(item, Move_icon):
                item.is_drag = True
                item.original_pos= item.pos[0], item.pos[1]
                item.off_set_x = item.rect.x - event.pos[0]
                item.off_set_y = item.rect.y - event.pos[1]
                break
            elif item.rect.collidepoint(event.pos) and isinstance(item, Return_layer):
                self.running = False
                self.scene_manager.go_to(TitleScene(self.real_screen))
                print 1

class Move_icon(pygame.sprite.Sprite):
    def __init__(self, typ):
        pygame.sprite.Sprite.__init__(self)
        self.pos = [0, 0]
        self.image = pygame.image.load("image/" + typ + ".png").convert_alpha()
        self.typ = typ
        self.rect = self.image.get_rect()
        self.is_drag = False
        self.off_set_x = 0
        self.off_set_y = 0
        self.original_pos = [0, 0]
        self.in_icon_bar = True
        self.in_timeline = False
        self.con = pygame.sprite.RenderUpdates(self)



    def set_rect_pos(self):
        self.rect.topleft = (self.pos[0],  self.pos[1])

    def update(self, dt):
        if self.is_drag:
            mouse_pos = pygame.mouse.get_pos()
            self.pos[0] = mouse_pos[0] + self.off_set_x
            self.pos[1] = mouse_pos[1] + self.off_set_y

        self.set_rect_pos()



class Icon_bar(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.image = pygame.image.load("image/icon_bar.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.con = pygame.sprite.RenderUpdates(self)

        self.icons = set()

    def add_icon(self, icon):
        self.icons.add(icon)
        for i, icon in enumerate(self.icons):
            icon.pos = [13, 30 + 30*i]
        #print self.icons

    def remove_icon(self, icon):
        self.icons.remove(icon)
        for i, icon in enumerate(self.icons):
            icon.pos = [13, 30 + 30*i]

    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])



    # TODO: change color when mouse drag is on
    # TODO: hide and reveal when mouse approach

class Character_timeline(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.image = pygame.image.load("image/character_timeline.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.con = pygame.sprite.RenderUpdates(self)
        self.moves = {} # key move, value time

    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])

    def add_move(self, move, time):
        self.moves[move] = time
        #print self.moves
    def remove_move(self, move):
        del self.moves[move]

    def reset(self):
        pass




# TODO: start, pause buttons
# class Control_bar(pygame.sprite.Sprite):

class Timeline_pointer(pygame.sprite.Sprite):
    def __init__(self, character, timeline):
        self.original_pos = (50-8, 300-16)
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(self.original_pos)
        self.image = pygame.image.load("image/timeline_pointer.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.con = pygame.sprite.RenderUpdates(self)
        self.character = character
        self.timeline = timeline
        self.running = False

    def update(self, dt):
        if self.running:
            self.pos[0] += 100 * dt
        if self.pos[0] > 300-8:
            self.pos[0] = 300-8
        self.rect.topleft = (self.pos[0], self.pos[1])
        before, after = self.pos[0],self.pos[0] + 100 * dt
        for move in self.timeline.moves:
            if before <= self.timeline.moves[move]\
            and self.timeline.moves[move] <= after:
                if move.typ == 'up':
                    self.character.move_up()
                elif move.typ == 'left':
                    self.character.move_left()
                elif move.typ == 'down':
                    self.character.move_down()
                elif move.typ == 'right':
                    self.character.move_right()

    def toggle_pause(self):
        self.running = not self.running

    def reset(self):
        self.running = False
        self.pos = list(self.original_pos)



class Maze(pygame.sprite.Sprite):
    def __init__(self, pos, game, maze_id):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.pos = list(pos)
        self.con = pygame.sprite.RenderUpdates(self)
        self.image = pygame.image.load("image/maze.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.maze = []
        self.exit_index = set()

        with open('maze/s' + str(maze_id), 'r') as f:
            this_line = []
            x, y = pos[0], pos[1]
            for i, line in enumerate(f):
                if i <= 15:
                    for j, c in enumerate(line):
                        if c == '|':
                            new_ob = Brick((x, y), True)
                            self.maze.append(new_ob)
                        elif c == '-':
                            new_ob = Brick((x, y), False)
                            self.maze.append(new_ob)
                        elif c == 'p' or c == 'P':
                            self.game.character.set_origanal_pos((x+5, y))
                        elif c == 'e' or c == 'E':
                            new_ob = Exit((x, y))
                            self.exit_index.add(len(self.maze))
                            self.maze.append(new_ob)

                        if j == len(line) - 3 and i == 15:
                            y -= 10
                        elif j == 0 and i == 15:
                            y += 10
                        if j == len(line) - 1:
                            x += 10
                        elif j != 0:
                            x += 15
                    x = pos[0]
                    y += 15
                elif i <= 25:
                    if line:
                        if line[0] == '#':
                            pass
                        else:
                            new_move_icon = Move_icon(line[:-1])
                            self.game.icon_bar.add_icon(new_move_icon)
                            self.game.icons.append(new_move_icon)
                            self.game.mouse_interactable.append(new_move_icon)



    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])

    def reset(self):
        pass

class Exit(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.image = pygame.image.load("image/exit.png").convert_alpha()
        self.con = pygame.sprite.RenderUpdates(self)
        self.rect = self.image.get_rect()

    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])



class Brick(pygame.sprite.Sprite):
    def __init__(self, pos, v):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        if v:
            self.image = pygame.image.load("image/brick_v.png").convert_alpha()
        else:
            self.image = pygame.image.load("image/brick.png").convert_alpha()

        self.con = pygame.sprite.RenderUpdates(self)
        self.rect = self.image.get_rect()

    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])


class Character(pygame.sprite.Sprite):
    """
    docstring for Character.
    """
    def __init__(self, pos, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.original_pos = pos
        self.pos = list(pos)
        self.image = pygame.image.load("image/character.png").convert_alpha()
        self.con = pygame.sprite.RenderUpdates(self)
        self.vel = [0, 0]
        self.rect = self.image.get_rect()
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.speed = 120
        self.out = False
        self.running = False


    def set_rect_pos(self):
        # self.rect.topleft = (self.pos[0] - self.bb_general.x, self.pos[1] - self.bb_general.y)
        self.rect.topleft = (self.pos[0], self.pos[1])

    def update(self, maze, dt):
        if self.out:
            # TODO text layer win message
            return
        if self.running:
            self.update_move(maze, dt)
            self.pos[0] += self.vel[0] * dt
            self.pos[1] += self.vel[1] * dt

        self.set_rect_pos()

    def move_left(self):  self.moving_left = True
    def stop_left(self):  self.moving_left = False
    def move_right(self): self.moving_right = True
    def stop_right(self): self.moving_right = False
    def move_up(self):    self.moving_up = True
    def stop_up(self):    self.moving_up = False
    def move_down(self):  self.moving_down = True
    def stop_down(self):  self.moving_down = False



    def update_move(self, maze, dt):

        if self.moving_left:
            self.vel[0] = -self.speed
        elif self.moving_right:
            self.vel[0] = self.speed
        else:
            self.vel[0] = 0

        if self.moving_up:
            self.vel[1] = -self.speed
        elif self.moving_down:
            self.vel[1] = self.speed
        else:
            self.vel[1] = 0


        self.update_direction()
        new_rect = Rect((self.rect.left + dt*self.vel[0],\
             self.rect.top + dt*self.vel[1]),\
             (self.rect.width, self.rect.height))

        coll = new_rect.collidelist(maze.maze)
        if coll in maze.exit_index:
            self.out = True
            print 'out'
        elif coll != -1:
            self.pos = [self.pos[0] - self.vel[0]*dt, self.pos[1] - self.vel[1]*dt]
            new_rect_ud = Rect((self.rect.left,\
                 self.rect.top + dt*self.vel[1]),\
                 (self.rect.width, self.rect.height))
            new_rect_lr = Rect((self.rect.left + dt*self.vel[0],\
                 self.rect.top),\
                 (self.rect.width, self.rect.height))
            coll_ud = new_rect_ud.collidelist(maze.maze)
            coll_lr = new_rect_lr.collidelist(maze.maze)
            if coll_ud != -1:
                self.stop_up()
                self.stop_down()
            if coll_lr != -1:
                self.stop_left()
                self.stop_right()
            if coll_lr == -1 and coll_ud == -1:
                self.stop_up()
                self.stop_down()
                self.stop_left()
                self.stop_right()


    def update_direction(self):
        if self.vel[0] > 0:
            self.direction = 'r'
        elif self.vel[0] < 0:
            self.direction = 'l'


    def toggle_pause(self):
        if not self.out:
            self.running = not self.running

    def set_origanal_pos(self, pos):
        self.original_pos = pos
        self.pos = list(pos)


    def reset(self):
        self.pos = list(self.original_pos)
        self.vel = [0, 0]
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.out = False
        self.running = False

class Return_layer(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.image = pygame.image.load("image/return_layer.png").convert_alpha()
        self.con = pygame.sprite.RenderUpdates(self)
        self.rect = self.image.get_rect()
    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])
