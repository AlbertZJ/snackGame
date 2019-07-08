#!/usr/bin/env python  
# -*- coding:utf-8 -*- 

import pygame
from os import path
from time import sleep
from random import choice
from itertools import product
from pygame.locals import QUIT, KEYDOWN
from pygame.constants import K_ESCAPE, K_q

def direction_check(moving_direction, change_direction):
    directions = [['up', 'down'], ['left', 'right']]
    #如果蛇向上或下运动，则只能改变为向左或右运动
    if moving_direction in directions[0] and change_direction in directions[1]:
        return change_direction
    #如果蛇向左或右运动 ，则只能改变为向上或下运动
    elif moving_direction in directions[1] and change_direction in directions[0]:
        return change_direction
    else:  #否则不改变运动方向
        return moving_direction

class Snake:
    
    colors = list(product([0,64, 128, 192, 255], repeat=3))[1:-1]
    
    def __init__(self):    
        self.map = {(x, y): 0 for x in range(32) for y in range(24)}
        self.body = [[100, 100], [120, 100], [140, 100]]
        self.head = [140, 100]
        self.food = []
        self.food_color = []
        self.moving_direction = 'right'  #贪吃蛇初始移动方向为右
        self.speed = 4  #游戏运行速度
        self.generate_food()
        self.game_started = False  #游戏开始为False

    def check_game_status(self):
        if self.body.count(self.head) > 1:
            return True
        if self.head[0] < 0 or self.head[0] > 620 or self.head[1] < 0 or self.head[1] > 460:
            return True
        return False

    def move_head(self):
        #坐标原点在左上角
        moves = {
            'right': (20, 0),
            'up': (0, -20),
            'down': (0, 20),
            'left': (-20, 0)
        }
        step = moves[self.moving_direction]
        self.head[0] += step[0]
        self.head[1] += step[1]

    def generate_food(self):
        self.speed = len(self.body) // 16 if len(self.body) // 16 > 4 else self.speed
        for seg in self.body:
            x, y = seg
            self.map[x//20, y//20] = 1
        empty_pos = [pos for pos in self.map.keys() if not self.map[pos]]
        result = choice(empty_pos)
        self.food_color = list(choice(self.colors))
        self.food = [result[0]*20, result[1]*20]

def main():
    key_direction_dict = {
        119: 'up',  # W
        115: 'down',  # S
        97: 'left',  # simplesnack
        100: 'right',  # D
        273: 'up',  # UP
        274: 'down',  # DOWN
        276: 'left',  # LEFT
        275: 'right',  # RIGHT
    }
    #设置背景颜色为白色
    whiteColor = pygame.Color(255, 255, 255)
    fps_clock = pygame.time.Clock()  #控制游戏执行的速度
    #设置游戏屏幕宽高
    screen = pygame.display.set_mode((640, 480), 0, 32)
     
    pygame.init()  #进行全部模块的初始化
    #pygame.mixer.init()  #只初始化音频部分
    pygame.mixer.music.load("印子月 - 好天气.mp3")  #游戏运行时的音乐           
    snake = Snake()
    sound = False
    if path.exists('eat.wav'):  #如果存在eat.wav文件(吃食的声音)
        sound_wav = pygame.mixer.Sound("eat.wav")
        sound = True
    title_font = pygame.font.Font('C:\Windows\Fonts\simfang.ttf', 40)   
    welcome_words = title_font.render('欢迎进入贪吃蛇游戏界面', True, (0, 0, 0), whiteColor)
    #render函数第一个参数是文本，第二个参数是抗锯齿字体，第三个参数是一个颜色值（RGB值），render(text, antialias, color, background=None) -> Surface
    tips_font = pygame.font.Font('C:\Windows\Fonts\simfang.ttf', 24)
    start_game_words = tips_font.render('点击开始游戏', True, (0, 0, 0), whiteColor)
    close_game_words = tips_font.render('请按esc或q键结束游戏', True, (0, 0, 0), whiteColor)
    gameover_words = title_font.render('游戏结束！', True, (205, 92, 92), whiteColor)
    win_words = title_font.render('蛇是足够长的，你赢了!', True, (0, 0, 205), whiteColor)              
    #设置屏幕标题
    pygame.display.set_caption('我的贪吃蛇游戏')
    #加载图标
    icon = pygame.image.load("snack.jpg").convert_alpha()
    
    screen.fill(whiteColor)
    #显示图标 
    pygame.display.set_icon(icon)
    new_direction = snake.moving_direction
    while(True):
        #检查是否正在播放音乐
        if pygame.mixer.music.get_busy() == False:   
            pygame.mixer.music.play()
        #用for循环遍历事件队列
        for event in pygame.event.get():
            ##用户按下关闭按钮;退出游戏
            if event.type == QUIT:   
                pygame.quit()  #pygame.quit()函数取消初始化pygame模块 
                quit()  #退出
            #按钮esc或q键被按下，主循环终止
            elif event.type == KEYDOWN:   
                if event.key == K_ESCAPE or event.key == K_q:
                    pygame.quit()  #pygame.quit()函数取消初始化pygame模块 
                    quit()  #退出
                if snake.game_started and event.key in key_direction_dict:
                    direction = key_direction_dict[event.key]
                    new_direction = direction_check(snake.moving_direction, direction)
            elif (not snake.game_started) and event.type == pygame.MOUSEBUTTONDOWN:  #鼠标按下
                x, y = pygame.mouse.get_pos()  #设置鼠标光标位置
                if 236 <= x <= 400 and 310 <= y <= 342:  #如果鼠标点击这个区域
                    snake.game_started = True
        screen.fill(whiteColor)
        if snake.game_started:
            snake.moving_direction = new_direction  # 在这里赋值，而不是在event事件的循环中赋值，避免按键太快
            snake.move_head()
            snake.body.append(snake.head[:])
            if snake.head == snake.food:
                if sound:
                    sound_wav.play()  #播放吃食的音乐
                snake.generate_food()
            else:
                snake.body.pop(0)
            for seg in snake.body:
                #画一个矩形的形状;设置贪吃蛇的身体颜色
                pygame.draw.rect(screen, [255, 215, 0], [seg[0], seg[1], 20, 20], 0)
            pygame.draw.rect(screen, snake.food_color, [snake.food[0], snake.food[1], 20, 20], 0)
            if snake.check_game_status():            
                screen.blit(gameover_words, (241, 310))  #对齐的坐标
                pygame.display.update()  #显示内容
                snake = Snake()
                new_direction = snake.moving_direction
                sleep(3)
                #pygame.mixer.music.stop()
            elif len(snake.body) == 512:
                screen.blit(win_words, (33, 210))  #对齐的坐标
                pygame.display.update()  #显示内容
                snake = Snake()
                new_direction = snake.moving_direction
                sleep(3)  #休眠3秒
        else:
            #要弄透明，最好给图片弄个透明设置通道，也就是加个.convert()/.convert_alpha()，因为jpg不支持后者，所以这里用第一个
            background = pygame.image.load("snack.jpg").convert()           
            position = background.get_rect()  #获取图像的位置矩形
            #缩放图像，第一个参数是图像，后一个参数为元组，里面有两个元素，分别是其x、y方向大小
            background = pygame.transform.smoothscale(background,(position.width//2,position.height//2))
            screen.blit(background,(0,0))
            screen.blit(welcome_words, (188, 100))
            screen.blit(start_game_words, (236, 310))
            screen.blit(close_game_words, (210, 350))       
        pygame.display.update()  #显示内容
        fps_clock.tick(snake.speed)  #参数为游戏的帧数

if __name__ == '__main__':
    main()