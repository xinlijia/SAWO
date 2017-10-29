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
            # print type(manager.scene)
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


# TODO
# class StageChooseScene

class TitleScene(object):

    def __init__(self, screen):
        super(TitleScene, self).__init__()
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.save = [0, 0, 0]
        self.read_save()
        self.font = pygame.font.SysFont('Arial', 40)
        self.bg = pygame.image.load('image/bg.png').convert_alpha()
        self.stage1 = StageIcon(1, (20, 100), self.save[0])
        self.stage2 = StageIcon(2, (140, 100), self.save[1])
        self.stage3 = StageIcon(3, (260, 100), self.save[2])
        self.stages = [self.stage1, self.stage2, self.stage3]
        self.mouse_interactable = self.stages

    def loop(self):

        text1 = self.font.render('choose stage', True, (255, 255, 255))
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(text1, (65, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.on_mousedown(event)
            elif event.type == pygame.KEYDOWN:
                self.on_keydown(event)


        dt = self.clock.tick(const.FPS) / 1000.0
        update_rects = []

        for stage in self.stages:
            stage.con.clear(self.screen, self.bg)
            stage.con.update(dt)
            update_rects += stage.con.draw(self.screen)

        pygame.display.update(update_rects)


        return True

    def read_save(self):
        with open('save/save') as save_file:
            for i, line in enumerate(save_file):
                if i < 3:
                    self.save[i] = line[:-1]

    def on_keydown(self, event):
        self.scene_manager.go_to(Scene(self.screen))
        self.running = False
    def on_mousedown(self, event):

        for item in self.mouse_interactable:
            if item.rect.collidepoint(event.pos) and isinstance(item, StageIcon):
                self.running = False
                self.scene_manager.go_to(Scene(self.screen, item.stage_id))


class StageIcon(pygame.sprite.Sprite):
    def __init__(self, stage_id, pos, rating):
        pygame.sprite.Sprite.__init__(self)
        self.stage_id = stage_id
        self.pos = list(pos)
        image_rating = pygame.image.load('image/'+str(rating)+'star.png').convert_alpha()
        image_stage = pygame.image.load('image/stage'+str(stage_id)+'.png').convert_alpha()
        self.image = image_stage.copy()
        self.image.blit(image_rating, (0, 35))
        self.rect = self.image.get_rect()
        self.con = pygame.sprite.RenderUpdates(self)

    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])


class Scene(object):

    def __init__(self, screen, stage_id):
        self.screen = screen
        self.running = True
        initial_pos = (const.REAL_WIDTH / 2 - 50, 40)
        self.clock = pygame.time.Clock()
        self.icons = []
        self.mouse_interactable = []
        self.bg = pygame.image.load('image/bg.png').convert_alpha()
        self.move_bar = MoveBar((10, 50))
        self.character_timeline = CharacterTimeline((50, 320))
        self.stage_id = stage_id
        self.rating = 0
        self.character = Character(initial_pos, self)
        self.maze = Maze((80, 30), self, stage_id)
        self.return_layer = ReturnLayer((10, 20))

        self.timeline_pointer = TimelinePointer(self.character, self.character_timeline, self.character_timeline.pos)
        self.win_layer = WinLayer((100, 100), self)

        self.mouse_interactable.append(self.return_layer)
        self.mouse_interactable.append(self.win_layer)

        #self.screen = pygame.surface.Surface((const.REAL_WIDTH, const.REAL_HEIGHT))




    def loop(self):
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
            self.move_bar.con.clear(self.screen, self.bg)
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
            self.move_bar.con.update(dt)
            self.character_timeline.con.update(dt)
            self.timeline_pointer.con.update(dt)
            self.maze.con.update(dt)
            for ob in self.maze.maze:
                ob.con.update(dt)
            self.character.con.update(self.maze, dt)
            self.return_layer.con.update(dt)

            if self.character.out:
                self.win_layer.con.update(dt)


            # draw
            update_rects = []

            update_rects += self.move_bar.con.draw(self.screen)
            update_rects += self.character_timeline.con.draw(self.screen)

            update_rects += self.maze.con.draw(self.screen)
            for ob in self.maze.maze:
                update_rects += ob.con.draw(self.screen)
            update_rects += self.timeline_pointer.con.draw(self.screen)
            update_rects += self.character.con.draw(self.screen)
            for icon in self.icons:
                update_rects += icon.con.draw(self.screen)
            update_rects += self.return_layer.con.draw(self.screen)
            if self.character.out:
                update_rects += self.win_layer.con.draw(self.screen)


            # scaling and updating
            #scaled_update_rects = [pygame.Rect(2*r.left - 4, 2*r.top - 4, 2*r.width + 8, 2*r.height + 8) for r in update_rects]
            #pygame.transform.scale(self.screen, (const.WIDTH, const.HEIGHT), self.screen)
            #pygame.display.update(scaled_update_rects)
            pygame.display.update(update_rects)

            if self.character.out:
                self.save_to_file()
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
            if isinstance(item, MoveIcon):
                if item.is_drag == True:
                    if item.rect.colliderect(self.character_timeline):
                        item.is_drag = False
                        item.off_set_x = 0
                        item.off_set_y = 0
                        item.pos[1] = self.character_timeline.pos[1] \
                        + self.character_timeline.rect.height/2 - item.rect.height/2 # y pos of timeline
                        if item in self.move_bar.icons:
                            self.move_bar.remove_icon(item)
                        elif item in self.character_timeline.moves:
                            self.character_timeline.remove_move(item)
                        self.character_timeline.add_move(item, item.pos[0])
                    elif item.rect.colliderect(self.move_bar):
                        item.is_drag = False
                        item.off_set_x = 0
                        item.off_set_y = 0
                        if item in self.move_bar.icons:
                            self.move_bar.remove_icon(item)
                        elif item in self.character_timeline.moves:
                            self.character_timeline.remove_move(item)
                        self.move_bar.add_icon(item)
                    else:
                        item.is_drag = False
                        item.off_set_x = 0
                        item.off_set_y = 0
                        item.pos = [item.original_pos[0], item.original_pos[1]]

    def on_mousedown(self, event):
        for item in self.mouse_interactable:
            if item.rect.collidepoint(event.pos) and isinstance(item, MoveIcon):
                item.is_drag = True
                item.original_pos= item.pos[0], item.pos[1]
                item.off_set_x = item.rect.x - event.pos[0]
                item.off_set_y = item.rect.y - event.pos[1]
                break
            elif item.rect.collidepoint(event.pos) and isinstance(item, ReturnLayer):
                self.running = False
                self.scene_manager.go_to(TitleScene(self.screen))
            elif item.rect.collidepoint(event.pos) and isinstance(item, WinLayer):
                return_rect = pygame.rect.Rect(item.rect.left + 50 ,item.rect.top + 95, 75, 15)
                if return_rect.collidepoint(event.pos):
                    self.running = False
                    self.scene_manager.go_to(TitleScene(self.screen))

    def save_to_file(self):
        ratings = []
        with open('save/save', 'r') as f:
            for i, line in enumerate(f):
                if i == self.stage_id-1:
                    ratings.append(str(self.rating))
                elif line:
                    ratings.append(line[:-1])

        with open('save/save', 'w') as f:
            for l in ratings:
                f.write(l + '\n')

class ToolIcon(pygame.sprite.Sprite):
    def __init__(self, typ):
        pygame.sprite.Sprite.__init__(self)
        self.pos = [0, 0]
        self.image = pygame.image.load("image/tool-" + typ + ".png").convert_alpha()
        self.typ = typ
        self.rect = self.image.get_rect()
        self.is_drag = False
        self.off_set_x = 0
        self.off_set_y = 0
        self.original_pos = [0, 0]
        self.in_move_bar = True
        self.in_timeline = False
        self.con = pygame.sprite.RenderUpdates(self)

class ToolBar(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.image = pygame.image.load("image/tool_bar.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.con = pygame.sprite.RenderUpdates(self)
        self.icons = []

    def add_icon(self, icon):
        self.icons.append(icon)
        for i, icon in enumerate(self.icons):
            icon.pos = [self.pos[0] + 3, self.pos[1] + 10 + 30*i]
        #print self.icons

    def remove_icon(self, icon):
        self.icons.remove(icon)
        for i, icon in enumerate(self.icons):
            icon.pos = [self.pos[0] + 3, self.pos[1] + 10 + 30*i]

    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])

class MoveIcon(pygame.sprite.Sprite):
    def __init__(self, typ):
        pygame.sprite.Sprite.__init__(self)
        self.pos = [0, 0]
        self.image = pygame.image.load("image/move-" + typ + ".png").convert_alpha()
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
        self.rect = self.image.get_rect()
        self.con = pygame.sprite.RenderUpdates(self)
        self.icons = []

    def add_icon(self, icon):
        self.icons.append(icon)
        for i, icon in enumerate(self.icons):
            icon.pos = [self.pos[0] + 3, self.pos[1] + 10 + 30*i]
        #print self.icons

    def remove_icon(self, icon):
        self.icons.remove(icon)
        for i, icon in enumerate(self.icons):
            icon.pos = [self.pos[0] + 3, self.pos[1] + 10 + 30*i]

    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])



    # TODO: change color when mouse drag is on
    # TODO: hide and reveal when mouse approach


class CharacterTimeline(pygame.sprite.Sprite):
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

class WinLayer(pygame.sprite.Sprite):
    def __init__(self, pos, scene):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.scene = scene

        image_rating = pygame.image.load('image/'+str(self.scene.rating)+'star.png').convert_alpha()
        image_win_layer = pygame.image.load('image/win_layer.png').convert_alpha()
        self.image = image_win_layer.copy()
        self.image.blit(image_rating, (45, 55))
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
        # self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos[0], self.pos[1])


# TODO: start, pause buttons, fast forward
class ControlBar(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        # self.image = pygame.image.load("image/control_bar.png").convert_alpha()
        # self.rect = self.image.get_rect()
        self.con = pygame.sprite.RenderUpdates(self)

class StartIcon(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        # self.image = pygame.image.load("image/start_icon.png").convert_alpha()
        # self.rect = self.image.get_rect()
        self.con = pygame.sprite.RenderUpdates(self)

class StopIcon(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        # self.image = pygame.image.load("image/stop_icon.png").convert_alpha()
        # self.rect = self.image.get_rect()
        self.con = pygame.sprite.RenderUpdates(self)

class FastForwardIcon(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        # self.image = pygame.image.load("image/fast_forward_icon.png").convert_alpha()
        # self.rect = self.image.get_rect()
        self.con = pygame.sprite.RenderUpdates(self)

class ResetIcon(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        # self.image = pygame.image.load("image/reset_icon.png").convert_alpha()
        # self.rect = self.image.get_rect()
        self.con = pygame.sprite.RenderUpdates(self)

class TimelinePointer(pygame.sprite.Sprite):
    def __init__(self, character, timeline, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/timeline_pointer.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.original_pos = (pos[0]-self.rect.width/2, pos[1]-self.rect.height)
        self.pos = list(self.original_pos)

        self.con = pygame.sprite.RenderUpdates(self)
        self.character = character
        self.timeline = timeline
        self.running = False
        self.past_move = set()

    def update(self, dt):
        # TODO: modifiable time line scale
        if self.running:
            self.pos[0] += 100 * dt
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

    def toggle_pause(self):
        self.running = not self.running

    def reset(self):
        self.running = False
        self.pos = list(self.original_pos)
        self.past_move = set()


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
                            self.game.character.set_origanal_pos((x, y))
                        elif c == 'e' or c == 'E':
                            new_ob = Exit((x, y))
                            self.exit_index.add(len(self.maze))
                            self.maze.append(new_ob)
                        x += 15
                    x = pos[0]
                    y += 15
                elif i <= 25:
                    if line:
                        if line[0] == '#' or line[:-1] == '':
                            pass
                        else:
                            new_move_icon = MoveIcon(line[:-1])
                            self.game.move_bar.add_icon(new_move_icon)
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
            self.image = pygame.image.load("image/brick.png").convert_alpha()
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
        #self.pos = list(pos)
        self.image = pygame.image.load("image/character.png").convert_alpha()
        self.con = pygame.sprite.RenderUpdates(self)
        self.vel = [0, 0]
        self.rect = self.image.get_rect()
        self.rect.topleft = list(self.original_pos)
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.speed = 120
        self.out = False
        self.running = False


    #def set_rect_pos(self):
        # self.rect.topleft = (self.pos[0] - self.bb_general.x, self.pos[1] - self.bb_general.y)
        #self.rect.topleft = (self.pos[0], self.pos[1])

    def update(self, maze, dt):
        if self.out:
            return
        if self.running:
            self.update_move(maze, dt)



    def move_left(self):
        self.moving_left = True
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def stop_left(self):  self.moving_left = False
    def move_right(self):
        self.moving_right = True
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False


    def stop_right(self): self.moving_right = False
    def move_up(self):
        self.moving_up = True
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False


    def stop_up(self):    self.moving_up = False
    def move_down(self):
        self.moving_right = False
        self.moving_left = False
        self.moving_down = True
        self.moving_up = False

    def stop_down(self):  self.moving_down = False

    def move_single_axis(self, dx, dy, maze):
        self.rect.x += dx
        self.rect.y += dy
        for ob in maze.maze:
            if self.rect.colliderect(ob.rect):
                if isinstance(ob, Exit):
                    self.out = True
                    print 'out'
                else:
                    if dx > 0:
                        self.rect.right = ob.rect.left
                    elif dx < 0:
                        self.rect.left = ob.rect.right
                    if dy > 0:
                        self.rect.bottom = ob.rect.top
                    elif dy < 0:
                        self.rect.top = ob.rect.bottom




    def update_move(self, maze, dt):

        if self.moving_left:
            self.move(maze, -self.speed*dt, 0)
        if self.moving_right:
            self.move(maze, self.speed*dt, 0)
        if self.moving_up:
            self.move(maze, 0, -self.speed*dt)
        if self.moving_down:
            self.move(maze, 0, self.speed*dt)

    def move(self, maze, dx, dy):
        if dx:
            self.move_single_axis(dx, 0, maze)
        if dy:
            self.move_single_axis(0, dy, maze)



    def update_direction(self):
        self.direction = ''
        if self.vel[1] > 0:
            self.direction += 'd'
        elif self.vel[1] < 0:
            self.direction += 'u'
        else:
            if self.vel[0] > 0:
                self.direction += 'r'
            elif self.vel[0] < 0:
                self.direction += 'l'


    def toggle_pause(self):
        if not self.out:
            self.running = not self.running

    def set_origanal_pos(self, pos):
        self.original_pos = pos
        self.rect.topleft = list(pos)


    def reset(self):
        self.rect.topleft = list(self.original_pos)
        self.vel = [0, 0]
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.out = False
        self.running = False


class ReturnLayer(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(pos)
        self.image = pygame.image.load("image/return_layer.png").convert_alpha()
        self.con = pygame.sprite.RenderUpdates(self)
        self.rect = self.image.get_rect()
    def update(self, dt):
        self.rect.topleft = (self.pos[0], self.pos[1])
