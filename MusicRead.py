# -*- coding: utf-8 -*-
import array
import os
import wave
import numpy as np
import pygame
import sys
from pydub import AudioSegment

old_path = "MusicResources/RISE.mp3"
new_path = "MusicResources/RISE.wav"


def trans_mp3_to_wav(filepath):
    song = AudioSegment.from_mp3(filepath)
    song.export(new_path, format="wav")


def read_music_data(music_path):
    music_name, music_type = os.path.splitext(music_path)
    file_path = music_path
    if music_type != '.wav':  # 将音乐转换为wav格式
        print 'try ', music_type, 'to wav'
        song = AudioSegment.from_file(music_path, music_type[1:])
        file_path = music_name+'.wav'
        song.export(file_path, format='wav')

    # 读取音乐数据
    music_wave = wave.open(file_path, 'rb')
    music_params = music_wave.getparams()
    print music_params
    nchannels, samp_width, framerate, nframes = music_params[:4]
    str_data = music_wave.readframes(nframes)
    music_wave.close()

    wave_data = np.fromstring(str_data, dtype=np.short)
    wave_data.shape = -1, 2
    wave_data = wave_data.T
    music_time = nframes * 1/framerate
    print 0.5*50*200
    return file_path, music_time, wave_data[0], wave_data[1]


def main():
    read_music_data(new_path)


if __name__ == '__main__':
    main()
