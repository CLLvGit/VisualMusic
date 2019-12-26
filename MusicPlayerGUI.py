# -*- coding: utf-8 -*-
import os
from Tkinter import *
import tkMessageBox
from tkFileDialog import *
import Visualization
import multiprocessing


class MusicPlayerGUI(Frame):
    music_path_sv = None

    def __init__(self, root, **kw):
        Frame.__init__(self, root, **kw)
        self.root = root
        self.music_path_sv = StringVar()
        self.make_main_win()

    def make_main_win(self):
        file_frame = FrameUtil.make_entry_button(self.root, "歌曲(wav/mp3)", "选择", self.music_path_sv,
                                                 lambda: self.fileopen())
        play_button = FrameUtil.make_button(self.root, "播放", self.play_music)

        file_frame.grid(row=0, column=0, sticky=W)
        play_button.grid(row=1, column=0)

    def play_music(self):
        path = self.music_path_sv.get()
        file_type = path.split('.')[-1]
        if not os.path.exists(path):
            tkMessageBox.showerror(u"文件打开失败", u"文件不存在！", parent=self.root)
            return
        if file_type not in ['mp3', 'wav', 'MP3', 'WAV']:
            tkMessageBox.showerror(u"文件类型错误", u"应选择 .wav/.mp3格式文件！", parent=self.root)
            return
        t = multiprocessing.Process(target=Visualization.start_music, args=(path,))
        t.start()

    def fileopen(self):
        file_type = [('music', ('MP3', 'WAV'))]
        self.music_path_sv.set('')
        print "open file:", os.path.pardir + '/MusicResources/'
        file_name = askopenfilename(filetypes=file_type, initialdir=os.path.pardir + '/MusicResources/')
        if file_name:
            self.music_path_sv.set(file_name)


class FrameUtil:

    @staticmethod
    def make_button(root, text, command):
        button = Button(root, width=20, text=text, command=command)
        return button

    @staticmethod
    def make_entry(root, title, sv):
        frame = Frame(root)
        label = Label(frame, width=20, text=title)
        entry = Entry(frame, width=50, textvariable=sv)
        label.grid(row=0, column=0)
        entry.grid(row=0, column=1)
        return frame

    @staticmethod
    def make_entry_button(root, title, button_text, sv, command):
        frame = Frame(root)
        frame_entry = FrameUtil.make_entry(frame, title, sv)
        button = FrameUtil.make_button(frame, button_text, command)
        frame_entry.grid(row=0, column=0)
        button.grid(row=0, column=1)
        return frame


def main():
    multiprocessing.freeze_support()
    root = Tk()
    root.title("播放音乐")
    MusicPlayerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
