import pygame as pg
import random

score_color = (192,192,192)
tip_color = (64,64,64)
bg_color = (232,232,232)

screen_size = pg.Rect(0,0,24*30,24*20)
cell_size = 24

food_update_event = pg.USEREVENT
snake_move_event = pg.USEREVENT + 1

ho_dir = (pg.K_LEFT,pg.K_RIGHT)
ve_dir = (pg.K_UP,pg.K_DOWN)

class Label():
    def __init__(self,size=48,is_score=True):
        self.font = pg.font.SysFont('simhei',size=size)
        self.is_score = is_score
    def draw(self,window,text):
        text_surface = self.font.render(text,True,score_color if self.is_score else tip_color)
        window_rect = window.get_rect()
        text_rect = text_surface.get_rect()
        if self.is_score:
            text_rect.bottomleft = window_rect.bottomleft
        else:
            text_rect.center = window_rect.center
        window.blit(text_surface,text_rect)

class Food():
    def __init__(self):
        self.color = (255,0,0)
        self.score = 10
        self.rect = None
        self.get_random_rect()
    def get_random_rect(self):
        self.rect = pg.Rect(random.randint(0,screen_size.w // cell_size -1)*cell_size,random.randint(0,screen_size.h // cell_size -1)*cell_size,cell_size,cell_size)
        self.rect.inflate_ip(-cell_size,-cell_size)
        pg.time.set_timer(food_update_event,15000)

    def draw(self,window):
        if self.rect.w < cell_size:
            self.rect.inflate_ip(2,2)
        pg.draw.ellipse(window,self.color,self.rect)
        
class Snake():
    def __init__(self):
        self.speed = 24
        self.color = (0,0,0)
        self.body_list = []
        self.dir = pg.K_RIGHT
        self.time_interval = 250
        self.score = 0
        self.live = True
        self.reset_snake()

        self.eat_now = False
    def reset_snake(self):
        self.live = True
        self.dir = pg.K_RIGHT
        self.body_list = []
        for _ in range(3):
            self.add_node()
        self.rect = self.body_list[0]
        self.score = 0
        pg.time.set_timer(snake_move_event,self.time_interval)
    def add_node(self):
        if self.body_list:
            head = self.body_list[0].copy()
        else:
            head = pg.Rect(-cell_size,0,cell_size,cell_size)
        if self.dir == pg.K_RIGHT:
            head.x += cell_size
        if self.dir == pg.K_LEFT:
            head.x -= cell_size
        if self.dir == pg.K_UP:
            head.y -= cell_size
        if self.dir == pg.K_DOWN:
            head.y += cell_size
        self.body_list.insert(0,head)
        self.rect = self.body_list[0]
    def change_dir(self,to_dir):
        if (self.dir in ho_dir and to_dir in ho_dir) or (self.dir in ve_dir and to_dir in ve_dir):
            return
        else:
            self.dir = to_dir
    def eat_food(self,food):
        if self.rect.contains(food.rect):
            self.eat_now = True
            food.get_random_rect()
            self.score += 1
            self.time_interval -= 5
    def draw(self,window):
        for i,node in enumerate(self.body_list):
            pg.draw.rect(window,self.color,node.inflate(-2,-2),2 if i == 0 else 0 )
    def update(self):
        end_body = self.body_list.copy()
        
        self.add_node()
        if not self.eat_now:
            self.body_list.pop()
        self.eat_now = False

        if self.is_dead():
            self.live = False
            self.body_list = end_body
            return

        pg.time.set_timer(snake_move_event,self.time_interval)
    def is_dead(self):
        if not screen_size.contains(self.rect):
            return True
        for node in self.body_list[1:]:
            if node.contains(self.rect):
                return True
        return False
