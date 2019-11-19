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

position = 0

N_draw = 5000
draw_step = 10
draw_interval_ms = 1000/10.0

WIN_WIDTH = 600
WIN_HEIGHT = 600

CIRCLE_R = 0.35

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
    global WIN_WIDTH, WIN_HEIGHT
    glClearColor(0.3, 0.3, 0.3, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    WIN_SIZE = WIN_HEIGHT * WIN_WIDTH / 300000.0
    glLineWidth(WIN_SIZE*CIRCLE_R)
    glBegin(GL_LINES)
    glColor4f(0.2, 1, 0, 1)

    theta = 0
    theta_step = float(draw_step * math.pi/N_draw)
    wave_value_left = 1
    wave_value_right = 1

    volume_L = max(music_data_left[position:position+N_draw])/40000.0
    volume_L_1 = min(music_data_left[position:position+N_draw])/40000.0
    if abs(volume_L_1) > volume_L:
        volume_L = volume_L_1

    volume_R = max(music_data_right[position:position+N_draw])/40000.0
    volume_R_1 = min(music_data_right[position:position+N_draw])/40000.0
    if abs(volume_R_1) > volume_R:
        volume_R = volume_R_1

    CIRCLE_R_L = CIRCLE_R + np.mean([abs(a) for a in music_data_left[position:position+N_draw]])/50000
    CIRCLE_R_R = CIRCLE_R + np.mean([abs(a) for a in music_data_right[position:position+N_draw]])/50000
    for i in range(position, position+N_draw, draw_step):
        if i >= len(music_data_left):
            break

        # 左声道
        if volume_L > 0:
            glColor4f(0.5 + volume_L, 1 - volume_L, 0, 1)
        else:
            glColor4f(1, 1 + volume_L, -volume_L, 1)

        # L = music_data_right[i]/200000.0
        L = pow(abs(music_data_left[i]), 0.4)/800.0
        if music_data_left[i] < 0:
            L = -L
        wave_value_left -= L/20
        kx = -math.sin(theta)
        ky = math.cos(theta)
        if math.pi/2 < theta <= math.pi:
            kx = -math.cos(theta - math.pi/2)
            ky = -math.sin(theta - math.pi/2)
        x0 = kx * CIRCLE_R_L * wave_value_left
        y0 = ky * CIRCLE_R_L * wave_value_left
        glVertex2f(x0, y0)
        delta = (L + CIRCLE_R_L)
        x1 = kx * delta * wave_value_left
        y1 = ky * delta * wave_value_left
        glVertex2f(x1, y1)

        if volume_R > 0:
            glColor4f(0.5 + volume_R, 1 - volume_R, 0, 1)
        else:
            glColor4f(0.5, 1 + volume_R, -volume_R, 1)

        # L = music_data_right[i]/200000.0
        L = pow(abs(music_data_right[i]), 0.4)/800.0
        if music_data_right[i] < 0:
            L = -L
        wave_value_right -= L/20
        kx = math.sin(theta)
        ky = math.cos(theta)
        if math.pi/2 < theta <= math.pi:
            kx = math.cos(theta - math.pi/2)
            ky = -math.sin(theta - math.pi/2)
        x0 = kx * CIRCLE_R_R * wave_value_right
        y0 = ky * CIRCLE_R_R * wave_value_right
        glVertex2f(x0, y0)
        delta = (L + CIRCLE_R_R)
        x1 = kx * delta * wave_value_right
        y1 = ky * delta * wave_value_right
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
        return

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
    glutTimerFunc(int(draw_interval_ms), on_timer, 0)
    glutMainLoop()


def read_music(path):
    global music_data_left
    global music_data_right
    global N_draw
    global N_move
    global draw_interval_ms

    music_path, music_time, music_data_left, music_data_right = read_music_data(path)
    nframes = len(music_data_left)  # 总点数
    draw_times = music_time * 1000 / draw_interval_ms  # 动画总帧数
    N_move = nframes / draw_times
    print "draw interval:", draw_interval_ms
    print "draw times", draw_times
    print "N move", N_move
    return music_path


def play_music(path, volume=5):
    pygame.init()
    pygame.mixer.init()  # 初始化音频
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    sound.play()
    return sound


def start_music(path):
    music_path = read_music(path)
    play_music(music_path)
    draw_music()


def stop_play_music():
    print "click to close"

def main():
    path = new_path
    start_music(path)


if __name__ == '__main__':
    main()
