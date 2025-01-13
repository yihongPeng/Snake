import pygame as pg
import sys
sys.path.append('./')
from game_items import *

Bg_color = (232,232,232)

class Game():
    def __init__(self):
        self.main_window = pg.display.set_mode((24*30,24*20))
        pg.display.set_caption('Snake')
        self.clock = pg.time.Clock()
        self.score_Label = Label()
        self.stop_Label = Label(size = 24,is_score = False)

        self.food = Food()
        self.snake = Snake()

        self.is_paused = False
        self.game_over = False
        

    def Start(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return
                    elif event.key == pg.K_SPACE:
                        self.is_paused = not self.is_paused
                        if self.game_over:
                            self.reset_game()
                if not self.is_paused and not self.game_over:
                    if event.type == food_update_event:
                        self.food.get_random_rect()
                    elif event.type == snake_move_event:
                        self.snake.update()
                    elif event.type == pg.KEYDOWN:
                        if event.key in (pg.K_UP,pg.K_DOWN,pg.K_LEFT,pg.K_RIGHT):
                            self.snake.change_dir(event.key)
            if not self.snake.live:
                self.game_over = True
            self.snake.eat_food(self.food)
            self.main_window.fill(Bg_color)
            self.score_Label.draw(self.main_window,f'Scores:{self.snake.score}')
            self.food.draw(self.main_window)
            self.snake.draw(self.main_window)
            if self.game_over:
                self.stop_Label.draw(self.main_window,f'Game over!Snake dies...')
            elif self.is_paused:
                self.stop_Label.draw(self.main_window,f'Game has been paused!Press Space to continue...')
            pg.display.update()
            self.clock.tick(60)
    def reset_game(self):
        self.snake.reset_snake()
        self.food.get_random_rect()
        self.game_over = False
        self.is_paused = False


if __name__ == '__main__':
    pg.init()
    game = Game()
    game.Start()
    pg.quit()