# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from MusicRead import *
import numpy as np
import math
import pygame
import time
import os
import threading

position = 1000000

N_draw = 5000
draw_step = 25
draw_interval_ms = 1000/10.0

WIN_WIDTH = 500
WIN_HEIGHT = 500

CIRCLE_R = 0.8

N_move = None
music_data_left = None
music_data_right = None


def draw_line():
    global position
    global music_data_left
    global music_data_right
    global N_draw
    global draw_step
    global CIRCLE_R
    glClearColor(0.8, 0.8, 0.8, 0.8)
    glClear(GL_COLOR_BUFFER_BIT)

    glLineWidth(0.2*CIRCLE_R)
    glBegin(GL_LINES)
    glColor4f(0.0, 0.0, 0.0, 0.5)

    theta = 0
    theta_step = float(draw_step * math.pi/N_draw)
    wave_value_left = 1
    wave_value_right = 1

    for i in range(position, position+N_draw, draw_step):
        # 左声道
        L = music_data_right[i]/200000.0
        wave_value_left -= L/8
        kx = -math.sin(theta)
        ky = math.cos(theta)
        if math.pi/2 < theta <= math.pi:
            kx = -math.cos(theta - math.pi/2)
            ky = -math.sin(theta - math.pi/2)
        x0 = kx * CIRCLE_R * wave_value_left
        y0 = ky * CIRCLE_R * wave_value_left
        glVertex2f(x0, y0)
        delta = (L + CIRCLE_R)
        x1 = kx * delta
        y1 = ky * delta
        glVertex2f(x1, y1)

        L = music_data_right[i]/200000.0
        wave_value_right -= L/8
        kx = math.sin(theta)
        ky = math.cos(theta)
        if math.pi/2 < theta <= math.pi:
            kx = math.cos(theta - math.pi/2)
            ky = -math.sin(theta - math.pi/2)
        x0 = kx * CIRCLE_R * wave_value_right
        y0 = ky * CIRCLE_R * wave_value_right
        glVertex2f(x0, y0)
        delta = (L + CIRCLE_R)
        x1 = kx * delta
        y1 = ky * delta
        glVertex2f(x1, y1)

        theta += theta_step

    glEnd()
    glutSwapBuffers()


def on_timer(value):
    global position
    global music_data_left
    global music_data_right
    global N_move
    global draw_interval_ms
    data_length = len(music_data_left)
    position += int(N_move)
    if position > data_length:
        position = 0

    glutPostRedisplay()
    glutTimerFunc(int(draw_interval_ms), on_timer, 0)


def draw_music():
    global draw_interval_ms
    global WIN_WIDTH, WIN_HEIGHT

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(WIN_WIDTH, WIN_HEIGHT)
    glutInitWindowPosition(300, 200)
    glutCreateWindow("music visualization")
    glutDisplayFunc(draw_line)
    glutCloseFunc(stop_play_music())
    glutTimerFunc(int(draw_interval_ms), on_timer, 0)
    glutMainLoop()


def read_music(path):
    global music_data_left
    global music_data_right
    global N_draw
    global N_move
    global draw_interval_ms

    music_time, music_data_left, music_data_right = read_music_data(path)
    nframes = len(music_data_left)  # 总点数
    draw_times = music_time * 1000 / draw_interval_ms  # 动画总帧数
    N_move = nframes / draw_times
    print "draw interval:", draw_interval_ms
    print "draw times", draw_times
    print "N move", N_move


def play_music(path, volume=0.5):
    pygame.mixer.init()  # 初始化音频
    pygame.mixer.music.load(path)  # 加载路径
    pygame.mixer.music.set_volume(volume)  # 设置音量
    pygame.mixer.music.play()  # 播放


def start_music(path):
    read_music(path)
    play_music(path)
    draw_music()


def stop_play_music():
    pygame.mixer.music.stop()


def main():
    path = new_path
    start_music(path)


if __name__ == '__main__':
    main()
