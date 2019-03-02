import sys
import pygame
import math
import time

from agym.items import Block, Ball, Platform
from agym.enums import MenuS, GameS



def check_keydown_game_events(event, arg):
    if event.key == pygame.K_RIGHT or event.key == 196:
        arg.platform.moving_right = True
    elif event.key == pygame.K_LEFT or event.key == 207:
        arg.platform.moving_left = True
    elif event.key == pygame.K_SPACE:
        if not arg.ball.thrown:
            arg.ball.throw()
    elif event.key == pygame.K_ESCAPE:
        arg.id_menu = 1
        arg.state_flag = MenuS

    if arg.stats.cheat_mode:
        if event.key == pygame.K_r:
            arg.ball.restart()
        elif event.key == pygame.K_b:
            restart(arg)
        elif event.key == pygame.K_KP_PLUS:
            arg.ball.alpha_velocity += 1
        elif event.key == pygame.K_KP_MINUS:
            arg.ball.alpha_velocity -= 1
    else:
        print("CheatMode не включен")


def check_keyup_game_events(event, arg):
    if event.key == pygame.K_RIGHT or event.key == 196:
        arg.platform.moving_right = False
    elif event.key == pygame.K_LEFT or event.key == 207:
        arg.platform.moving_left = False


def check_keydown_menu_events(event, arg):
    cur_menu = arg.menu[arg.id_menu]
    print(event.key)

    if event.key == pygame.K_ESCAPE:
        cur_menu.func_for_escape(arg)
    if event.key == pygame.K_UP or event.key == 204:
        cur_menu.n_selected = (cur_menu.n_selected - 1 + 
                               cur_menu.n_buttons) % cur_menu.n_buttons
    if event.key == pygame.K_DOWN or event.key == 207:
        cur_menu.n_selected = (cur_menu.n_selected + 1) % cur_menu.n_buttons
    # Не нашёл в pygame заготовленный код для Enter-а
    if event.key == 13:
        print(cur_menu.buttons[cur_menu.n_selected].text)
        cur_menu.buttons[cur_menu.n_selected].func(arg)


def check_keyup_menu_events(event, arg):
    pass


def check_events(arg):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_game(arg)

        if event.type == pygame.KEYDOWN and event.key == 222:
            close_game(arg)

        if arg.state_flag == GameS:
            if event.type == pygame.KEYDOWN:
                check_keydown_game_events(event, arg)

            elif event.type == pygame.KEYUP:
                check_keyup_game_events(event, arg)

        elif arg.state_flag == MenuS:
            if event.type == pygame.KEYDOWN:
                check_keydown_menu_events(event, arg)

            elif event.type == pygame.KEYUP:
                check_keyup_menu_events(event, arg)
                

def collide_circle_rect(circle, rect, radius):
    coll_point = [-1, -1]

    if rect.left < circle[0] < rect.right:
        if math.fabs(circle[1] - rect.top) < radius:
            coll_point = [circle[0], rect.top]
        elif math.fabs(circle[1] - rect.bottom) < radius:
            coll_point = [circle[0], rect.bottom]
    elif rect.top < circle[1] < rect.bottom:
        if math.fabs(circle[0] - rect.left) < radius:
            coll_point = [rect.left, circle[1]]
        elif math.fabs(circle[0] - rect.right) < radius:
            coll_point = [rect.right, circle[1]]
    else:
        temp_func = lambda circle, point: True if (
            ((circle[0] - point[0])**2 + (circle[1] - point[1])**2) ** 0.5 < radius 
        ) else False

        for side_1 in [rect.left, rect.right]:
            for side_2 in [rect.top, rect.bottom]:
                if temp_func(circle, (side_1, side_2)):
                    coll_point = [side_1, side_2]

    return coll_point


def blit_screen(arg):
    # Выводим стену заднего фона на экран
    arg.screen.blit(arg.wall, arg.wall.get_rect())

    # Выводим разнообразые информациооные поля
    arg.fps_score.blit()

    if arg.state_flag == GameS:
        arg.speed_score.blit()

        # Вы водим все необходимые игровые данные на главный экран
        arg.score_table.blit()
        arg.best_score_table.blit()
        arg.lives_table.blit()
        arg.level_table.blit()
        arg.time_table.blit()
    elif arg.state_flag == MenuS:
        pass

    arg.game_area.blit(arg)


    # Отрисовываем всё на экране
    pygame.display.flip()


def update_state(arg):
    # arg.fps_score.update()
    arg.game_area.update(arg)

    if arg.state_flag == GameS:
        # arg.tm.write_down("1")
        arg.speed_score.update()

        arg.score_table.update()
        arg.best_score_table.update()
        arg.lives_table.update()
        # arg.level_table.update()
        # arg.time_table.update()
        # arg.tm.write_down("2")
    elif arg.state_flag == MenuS:
        pass


def make_target_wall(arg):
    number_in_row = (arg.settings.ga_width - 4)//arg.settings.target_width
    side_space = (arg.settings.ga_width - number_in_row * arg.settings.target_width)//2


    for i in range(arg.settings.width_target_wall):
        x_pos, y_pos = side_space, arg.settings.space_target + i * arg.settings.target_height

        while(x_pos + arg.settings.target_width <= arg.game_area.rect.width - side_space):
            arg.top_space, arg.left_space = y_pos, x_pos
            arg.blocks.add(Block(arg))

            x_pos += arg.settings.target_width



def restart(arg):
    arg.blocks.empty()
    make_target_wall(arg)

    arg.platform.restart(arg)
    arg.ball.restart(arg)


def new_game(arg):
    # arg.wasted = False
    restart(arg)
    arg.stats.restart(arg)


def next_level(arg):
    # print(1)
    restart(arg)
    arg.stats.increase_difficulty(arg)


def wasted(arg):
    #print('wasted')
    arg.stats.lives -= 1

    if arg.stats.training_flag:
        # arg.population.end_game(arg)
        new_game(arg)
    else:
        new_game(arg)



def close_game(arg):
    arg.stats.save_cur_session(arg)
    # arg.population.save_cur_session(arg)
    exit()
