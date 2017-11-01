import pygame
from pygame.locals import *
import const



class MoveIcon(pygame.sprite.Sprite):
    def __init__(self, typ):
        pygame.sprite.Sprite.__init__(self)
        self.pos = [0, 0]
        self.image = pygame.image.load("image/move-" + typ + ".png").convert_alpha()
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))
        self.rect = self.image.get_rect()
        self.typ = typ
        self.rect = self.image.get_rect()
        self.is_drag = False
        self.off_set_x = 0
        self.off_set_y = 0
        self.original_pos = [0, 0]
        self.in_move_bar = True
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

class MoveBar(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.image = pygame.image.load("image/move_bar.png").convert_alpha()
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))
        self.rect = self.image.get_rect()
        self.con = pygame.sprite.RenderUpdates(self)
        self.icons = []

    def add_icon(self, icon):
        self.icons.append(icon)
        for i, icon in enumerate(self.icons):
            icon.pos = [self.pos[0] + 3*const.SCALE, self.pos[1] + 10*const.SCALE + 30*const.SCALE*i]
        #print self.icons

    def remove_icon(self, icon):
        self.icons.remove(icon)
        for i, icon in enumerate(self.icons):
            icon.pos = [self.pos[0] + 3*const.SCALE, self.pos[1] + 10*const.SCALE + 30*const.SCALE*i]

    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])



    # TODO: change color when mouse drag is on
    # TODO: hide and reveal when mouse approach

class ClickIcon(pygame.sprite.Sprite):
    def __init__(self, pos, typ):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.typ = typ
        self.image = pygame.image.load('image/'+ typ +'_icon.png').convert_alpha()
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))
        self.con = pygame.sprite.RenderUpdates(self)
        self.rect = self.image.get_rect()
    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])

    def toggle(self):
        if self.typ == 'start':
            self.typ = 'fast_forward'
        elif self.typ == 'fast_forward':
            self.typ = 'pause'
        elif self.typ == 'pause':
            self.typ = 'start'
        self.image = pygame.image.load('image/'+ self.typ +'_icon.png').convert_alpha()
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))

    def reset(self):
        self.typ = 'start'
        self.image = pygame.image.load('image/'+ self.typ +'_icon.png').convert_alpha()
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))

class HelpIcon(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.image = pygame.image.load("image/help_icon.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.con = pygame.sprite.RenderUpdates(self)
class HelpLayer(pygame.sprite.Sprite):
    def __init__(self, pos, scene):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.scene = scene
        pass

    def update(self, dt):
        pass

# TODO: start, pause buttons, fast forward



class CharacterTimeline(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.image = pygame.image.load("image/character_timeline.png").convert_alpha()
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))
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

class TimelinePointer(pygame.sprite.Sprite):
    def __init__(self, character, timeline, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/timeline_pointer.png").convert_alpha()

        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))

        self.rect = self.image.get_rect()
        self.original_pos = (pos[0]-self.rect.width/2, pos[1]-self.rect.height)
        self.pos = list(self.original_pos)

        self.con = pygame.sprite.RenderUpdates(self)
        self.character = character
        self.timeline = timeline
        self.running = 0
        self.past_move = set()
        self.out = False
        self.speed = 100

    def update(self, dt):
        # TODO: modifiable time line scale
        if self.out:
            return
        if self.running:
            self.pos[0] += self.speed * dt
        if self.pos[0] > self.timeline.pos[0] + self.timeline.rect.width - self.rect.width/2:
            self.pos[0] = self.timeline.pos[0] + self.timeline.rect.width - self.rect.width/2
        self.rect.topleft = (self.pos[0], self.pos[1])
        for move in self.timeline.moves:
            if self.timeline.moves[move] <= self.pos[0] and move not in self.past_move:
                print move.typ
                if move.typ == 'up':
                    self.character.move_up()
                elif move.typ == 'left':
                    self.character.move_left()
                elif move.typ == 'down':
                    self.character.move_down()
                elif move.typ == 'right':
                    self.character.move_right()
                self.past_move.add(move)
        self.out = self.character.out

    def toggle_pause(self):
        if not self.out:
            print self.running
            if not self.running:
                self.running = 1
            elif self.running == 1:
                self.running = 2
                self.speed *= 2
            elif self.running == 2:
                self.running = 0
                self.speed /= 2

    def reset(self):
        self.out = False
        self.running = 0
        self.pos = list(self.original_pos)
        self.past_move = set()


class Maze(pygame.sprite.Sprite):
    def __init__(self, pos, scene, maze_id):
        pygame.sprite.Sprite.__init__(self)
        self.scene = scene
        self.pos = list(pos)
        self.con = pygame.sprite.RenderUpdates(self)
        self.image = pygame.image.load("image/maze.png").convert_alpha()

        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))


        self.rect = self.image.get_rect()
        self.maze = []
        self.exit_index = set()
        self.tools = []

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
                            self.scene.character.set_origanal_pos((x, y))
                        elif c == 'e' or c == 'E':
                            new_ob = Exit((x, y))
                            self.exit_index.add(len(self.maze))
                            self.maze.append(new_ob)
                        x += 15*const.SCALE
                    x = pos[0]
                    y += 15*const.SCALE
                elif i <= 20:
                    if line:
                        if line[0] == '#' or line[:-1] == '':
                            pass
                        else:
                            new_move_icon = MoveIcon(line[:-1])
                            self.scene.move_bar.add_icon(new_move_icon)
                            self.scene.move_icons.append(new_move_icon)
                            self.scene.mouse_interactable.append(new_move_icon)
                elif i <= 25:
                    if line:
                        if line[0] == '#' or line[:-1] == '':
                            pass
                        else:
                            new_tool_icon = ToolIcon(line[:-1])
                            self.scene.tool_bar.add_icon(new_tool_icon)
                            self.scene.move_icons.append(new_tool_icon)
                            self.scene.mouse_interactable.append(new_tool_icon)



    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])

    def reset(self):
        pass

class Exit(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.image = pygame.image.load("image/exit.png").convert_alpha()
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))


        self.con = pygame.sprite.RenderUpdates(self)
        self.rect = self.image.get_rect()

    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])

class Brick(pygame.sprite.Sprite):
    def __init__(self, pos, v):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        if v:
            self.image = pygame.image.load("image/brick.png").convert_alpha()
        else:
            self.image = pygame.image.load("image/brick.png").convert_alpha()
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))

        self.con = pygame.sprite.RenderUpdates(self)
        self.rect = self.image.get_rect()

    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])

class ToolIcon(pygame.sprite.Sprite):
    def __init__(self, typ):
        pygame.sprite.Sprite.__init__(self)
        self.pos = [0, 0]
        self.image = pygame.image.load("image/tool-" + typ + ".png").convert_alpha()
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))
        self.typ = typ
        self.rect = self.image.get_rect()
        self.is_drag = False
        self.off_set_x = 0
        self.off_set_y = 0
        self.original_pos = [0, 0]
        self.in_move_bar = True
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

class ToolBar(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.image = pygame.image.load("image/tool_bar.png").convert_alpha()
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))
        self.rect = self.image.get_rect()
        self.con = pygame.sprite.RenderUpdates(self)
        self.icons = []

    def add_icon(self, icon):
        self.icons.append(icon)
        for i, icon in enumerate(self.icons):
            icon.pos = [self.pos[0] - icon.rect.width/2 + self.rect.width/2,
                        self.pos[1] + 10*const.SCALE +(icon.rect.height + 10*const.SCALE)*i]
        #print self.icons

    def remove_icon(self, icon):
        self.icons.remove(icon)
        for i, icon in enumerate(self.icons):
            icon.pos = [self.pos[0] + 3*const.SCALE, self.pos[1] + 10*const.SCALE + 30*const.SCALE*i]

    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])

class WinLayer(pygame.sprite.Sprite):
    def __init__(self, pos, scene):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.scene = scene

        image_rating = pygame.image.load('image/'+str(self.scene.rating)+'star.png').convert_alpha()
        image_win_layer = pygame.image.load('image/win_layer.png').convert_alpha()
        self.image = image_win_layer.copy()
        self.image.blit(image_rating, (45, 55))
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))
        self.rect = self.image.get_rect()
        self.con = pygame.sprite.RenderUpdates(self)

    def update(self, dt):
        points = 1000
        if points > 900:
            self.scene.rating = 3
        else:
            self.scene.rating = points//300
        image_rating = pygame.image.load('image/'+str(self.scene.rating)+'star.png').convert_alpha()
        image_win_layer = pygame.image.load('image/win_layer.png').convert_alpha()
        self.image = image_win_layer.copy()
        self.image.blit(image_rating, (45, 55))
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos[0], self.pos[1])
