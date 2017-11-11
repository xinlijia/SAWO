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
        self.image = pygame.image.load('image/'+ self.typ +'_icon.png').convert_alpha()
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*0.03*const.SCALE), int(h*0.03*const.SCALE)))
        self.con = pygame.sprite.RenderUpdates(self)
        self.rect = self.image.get_rect()
    def update(self, dt, mouse_pos):
        self.rect.topleft = (self.pos[0], self.pos[1])
        #mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = pygame.image.load('image/'+ self.typ +'_icon_p.png').convert_alpha()
        else:
            self.image = pygame.image.load('image/'+ self.typ +'_icon.png').convert_alpha()
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*0.03*const.SCALE), int(h*0.03*const.SCALE)))


    def toggle(self):
        if self.typ == 'start':
            self.typ = 'pause'
        elif self.typ == 'pause':
            self.typ = 'start'

        elif self.typ == 'fast_ward_s':
            self.typ == 'fast_ward_r'
        self.image = pygame.image.load('image/'+ self.typ +'_icon.png').convert_alpha()
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*0.03*const.SCALE), int(h*0.03*const.SCALE)))

    def reset(self):
        self.typ = 'start'
        self.image = pygame.image.load('image/'+ self.typ +'_icon.png').convert_alpha()
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*0.03*const.SCALE), int(h*0.03*const.SCALE)))


class HelpLayer(pygame.sprite.Sprite):
    def __init__(self, pos, scene):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.scene = scene
        self.con = pygame.sprite.RenderUpdates(self)
        #self.image
        #self.rect = Rect(1,1,0,0)
        pass

    def update(self, dt):
        pass



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
        self.running = False
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
            self.running = not self.running
    def reset(self):
        self.out = False
        self.running = 0
        self.pos = list(self.original_pos)
        self.past_move = set()
        self.speed = 100

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
        self.control_dic = {'}':'{', ']':'[', '>':'<'}
        self.control_pairs = {}
        self.teleport_pairs = {}
        with open('maze/s{0}'.format(maze_id), 'r') as f:
            this_line = []
            x, y = pos[0], pos[1]
            for i, line in enumerate(f):
                if i <= 15:
                    for j, c in enumerate(line):
                        if c == ' ':
                            pass
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
                        elif c in ('{', '[', '<'):
                            new_ob = ControlPannel((x, y), c)
                            self.maze.append(new_ob)
                        elif c in ('}', ']', '>'):
                            tag = self.control_dic[c]
                            new_ob = ControlDoor((x, y), tag)
                            self.maze.append(new_ob)
                            if tag in self.control_pairs:
                                self.control_pairs[tag].append(new_ob)
                            else:
                                self.control_pairs[tag] = [new_ob]
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
                            print line[:-1]

                            new_tool_icon = ToolIcon(line[:-1])
                            self.scene.tool_bar.add_icon(new_tool_icon)
                            self.scene.move_icons.append(new_tool_icon)
                            self.scene.mouse_interactable.append(new_tool_icon)



    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])

    def reset(self):
        for ob in self.maze:
            if isinstance(ob, ControlDoor):
                ob.reset()

    def add_tool(self, tool):
        self.remove_tool(tool)
        if tool.typ == 'teleportA':
            self.teleport_pairs['teleportB'] = tool
        elif tool.typ == 'teleportB':
            self.teleport_pairs['teleportA'] = tool
        self.tools.append(tool)
    def remove_tool(self, tool):

        if tool in self.tools:
            self.tools.remove(tool)
            if tool.typ == 'teleportA':
                del self.teleport_pairs['teleportB']
            elif tool.typ == 'teleportB':
                del self.teleport_pairs['teleportA']


class ControlPannel(pygame.sprite.Sprite):
    def __init__(self, pos, tag):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.image = pygame.image.load("image/control_panel_{0}.png".format(tag)).convert_alpha()
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))
        self.tag = tag
        self.con = pygame.sprite.RenderUpdates(self)
        self.rect = self.image.get_rect()
        self.doors = []

    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])

    def add_door(self, door):
        self.doors.append(door)


class ControlDoor(pygame.sprite.Sprite):
    def __init__(self, pos, tag):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.tag = tag

        self.image = pygame.image.load("image/control_door_{0}.png".format(tag)).convert_alpha()
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))
        self.con = pygame.sprite.RenderUpdates(self)
        self.is_open = False
        self.rect = self.image.get_rect()

    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])

    def toggle(self):
        if not self.is_open:
            self.is_open = True
            self.image = pygame.image.load("image/control_door_{0}_open.png".format(self.tag)).convert_alpha()
        else:
            self.is_open = False
            self.image = pygame.image.load("image/control_door_{0}.png".format(self.tag)).convert_alpha()
        w,h = self.image.get_size()

        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))

    def reset(self):
        self.is_open = False
        self.image = pygame.image.load("image/control_door_{0}.png".format(self.tag)).convert_alpha()
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))


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
        if icon in self.icons:
            self.icons.remove(icon)
            for i, icon in enumerate(self.icons):
                icon.pos = [self.pos[0] - icon.rect.width/2 + self.rect.width/2,
                            self.pos[1] + 10*const.SCALE +(icon.rect.height + 10*const.SCALE)*i]

    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])

class WinLayer(pygame.sprite.Sprite):
    def __init__(self, pos, scene):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.scene = scene

        image_rating = pygame.image.load('image/{0}star.png'.format(self.scene.rating)).convert_alpha()
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
        image_rating = pygame.image.load('image/{0}star.png'.format(self.scene.rating)).convert_alpha()
        image_win_layer = pygame.image.load('image/win_layer.png').convert_alpha()
        self.image = image_win_layer.copy()
        self.image.blit(image_rating, (45, 55))
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))
        self.rect.topleft = (self.pos[0], self.pos[1])


class HelpLayer(pygame.sprite.Sprite):
    def __init__(self, pos, scene):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.scene = scene
        self.con = pygame.sprite.RenderUpdates(self)
        font = pygame.font.SysFont('Arial', 20)
        move_help_dic = {'left':'go left', 'right':'go right', 'up':'go up', 'down':'go down'}
        tool_help_dic = {'u-turn':'turn back', 'teleportA': 'teleport to panelB', 'teleportB': 'teleport to panelA'}
        image_help_layer = pygame.image.load('image/help_layer.png').convert_alpha()
        self.image = image_help_layer.copy()
        w,h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w*const.SCALE), int(h*const.SCALE)))

        i = 0
        for move in scene.move_bar.icons:
            text = font.render('{0}: {1}'.format(move.typ, move_help_dic[move.typ]), True, (255, 255, 255))
            self.image.blit(text, (45, 25 + i))
            icon = pygame.image.load("image/move-" + move.typ + ".png").convert_alpha()
            w,h = icon.get_size()
            icon = pygame.transform.scale(icon, (int(w*const.SCALE/2), int(h*const.SCALE/2)))
            self.image.blit(icon, (15, 25 + i))
            i += 30
        for tool in scene.tool_bar.icons:
            text = font.render('{0}: {1}'.format(tool.typ, tool_help_dic[tool.typ]), True, (255, 255, 255))
            self.image.blit(text, (45, 25 + i))
            icon = pygame.image.load("image/tool-" + tool.typ + ".png").convert_alpha()
            w,h = icon.get_size()
            icon = pygame.transform.scale(icon, (int(w*const.SCALE/2), int(h*const.SCALE/2)))
            self.image.blit(icon, (15, 25 + i))
            i += 30

        self.rect = self.image.get_rect()
        self.con = pygame.sprite.RenderUpdates(self)

    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])
