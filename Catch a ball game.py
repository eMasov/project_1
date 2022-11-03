import pygame
from pygame.draw import *
from random import randint
import csv

pygame.init()
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))


def balls_quantity(min_quantity=10, max_quantity=15):
    '''
    :return: возвращает случайное число в указанных пределах min_quantity и max_quantity
    '''
    return randint(min_quantity, max_quantity)


def position(n, x=width, y=height):
    '''
    :param n: число шаров
    :param x, y: координаты центра области появления шаров
    :return: возвращает массив координат шаров по осям X, Y
    '''
    delta_x = x // 2
    delta_y = y // 2
    x_coordinates = [randint(x // 2 - delta_x, x // 2 + delta_x) for i in range(n)]
    y_coordinates = [randint(y // 2 - delta_y, y // 2 + delta_y) for i in range(n)]
    return x_coordinates, y_coordinates


def speeds(n):
    '''
    :param n: число шаров
    :param speed_x, speed_y: координаты центра области появления шаров
    :return: возвращает массив скоростей шаров по осям X, Y
    '''
    speeds_x = [randint(width // 120, width // 60) for i in range(n)]
    speeds_y = [randint(height // 120, height // 60) for i in range(n)]
    return speeds_x, speeds_y


def ball_params(n):
    '''
    :param n: число шаров
    :return: возвращает массив с размерами(радиусами шаров и массив с цветами шаров
    '''
    sizes = [randint(40, 60) for i in range(n)]
    colors = [(randint(100, 255), randint(100, 255), randint(100, 255)) for i in range(n)]
    return sizes, colors


def reflection(border, coord, R, speed):
    '''
    отвечате за отражение шара от стенки
    :param border: координата границы стенки, от которой отражается шар
    :param coord: координата центра шара
    :param R: радиус шара
    :param speed: компонента скорости шара, перпендикулярная этой стенке
    :return: возвращает скорость после отражениия
    '''
    if (coord >= border - R and speed > 0) or (coord <= R and speed < 0):
        speed = -1 * randint(border // 120, border // 60) * (speed / abs(speed))
    return speed


def reincarnation():
    '''
    оздает новый шар и вбрасывает его в заданную область
    :return: возвращает массив со новыми координатой, скоростью, цветом шара
    '''
    x = randint(width // 4, 2 * width // 4)
    y = randint(-60, -50)
    speed_x = randint(width // 120, width // 60)
    speed_y = randint(height // 120, width // 60)
    color = ((randint(100, 255), randint(100, 255), randint(100, 255)))
    return x, y, speed_x, speed_y, color


def game(X_, Y_, colors_, sizes_, speeds_x_, speeds_y_, delta_t=30, T=20000):

    '''
    создает поле для игры
    :param X_: координаты шаров по оси х
    :param Y_: координаты шаров по оси у
    :param colors_: цвета шаров
    :param sizes_: размеры (радиусы) шаров
    :param speeds_x_: скорости шаров по оси х
    :param speeds_y_: скорости шаров по оси у
    :param delta_t: время прокрутки кадра
    :param T: время игры
    '''

    time_long = 0 #прошедшее время
    count = 0  # переменная для подсчета очков
    while True and time_long < T:
        screen.fill((0, 0, 0))
        for i in range(q):
            # переобозначение переменных для краткости
            x = X[i]
            y = Y[i]
            color_ = colors[i]
            r = sizes[i]

            circle(screen, color_, (x, y), r)

            # обновление скорости
            speeds_x[i] = reflection(width, x, r, speeds_x[i])
            speeds_y[i] = reflection(height, y, r, speeds_y[i])
            # обновление координат
            X[i] += speeds_x[i]
            Y[i] += speeds_y[i]

        for event in pygame.event.get():
            if event.type == pygame.QUIT or time_long >= T:
                return count
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_x = event.pos[0]
                click_y = event.pos[1]
                #для каждого шара проверим, не кликнули ли по нему
                for i in range(q):
                    x = X[i]
                    y = Y[i]
                    r = sizes[i]
                    if (click_y - y) ** 2 + (click_x - x) ** 2 < r ** 2:
                        X[i], Y[i], speeds_x[i], speeds_y[i], colors[i] = reincarnation()
                        count += 1
        pygame.time.delay(30)
        pygame.display.update()
        time_long += 30 # учет прошедшего промежутка времени
    return count


def enter_nickname(text_color=(255, 255, 255), screen_color=(0, 0, 0), nick_color=(255, 0, 0)):
    '''
    окно для ввода ника пользователя
    text_color, screen_color, nick_color - цвета тексат для ползователя, экрана и ника соответственно
    :return: возвращает ник пользователя
    '''
    font_ = pygame.font.SysFont(None, 100)
    run = True
    user_text = pygame.font.SysFont('Corbel', 35).render('ENTER    YOUR    NICKNAME', True, text_color)
    nickname = ''
    while run:
        screen.fill(screen_color)
        screen.blit(user_text, (600, 400))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return nickname
                elif event.key == pygame.K_BACKSPACE:
                    nickname = nickname[:-1]
                else:
                    nickname += event.unicode
        screen.fill(0)
        text_surf = font_.render(nickname, True, nick_color)
        screen.blit(text_surf, text_surf.get_rect(center=screen.get_rect().center))
        screen.blit(user_text, (400, 300, 120, 40))
        instruction = pygame.font.SysFont('Corbel', 35).render('Click on balls to get the score.', True, text_color)
        screen.blit(instruction, (400, 500, 120, 40))
        instruction = pygame.font.SysFont('Corbel', 35).render('After you click enter you will have 20 seconds for the game', True, text_color)
        screen.blit(instruction, (230, 550, 120, 40))
        pygame.display.flip()
        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(30)
    clock.tick(1000)
    return nickname


def add_result(file_name, gamer, score):
    '''
    добавляет игрока в таблицу результатов
    :param file_name: имя csv файла
    :param gamer: имя игрока
    :param score: сумма очков игрока
    '''
    with open(file_name, 'a+', newline='') as file:
        csv_writer = csv.writer(file)
        if gamer == '':
            csv_writer.writerow(['Noname', score])
        else:
            csv_writer.writerow([gamer, score])


while True:
    # определяем количество и параметры шаров:
    q = balls_quantity()
    X, Y = position(n=q)[0], position(n=q)[0]
    speeds_x, speeds_y = speeds(n=q)[0], speeds(n=q)[1]
    sizes, colors = ball_params(n=q)[0], ball_params(n=q)[1]

    nick = enter_nickname() # узнаем ник пользователя
    score = game(X, Y, colors, sizes, speeds_x, speeds_y,) # запускаем игру
    add_result('Result table - Лист1.csv', nick, score)
    pygame.quit()
    exit()
