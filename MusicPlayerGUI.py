# -*- coding: utf-8 -*-
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
        file_frame = FrameUtil.make_entry_button(self.root, "歌曲", "选择", self.music_path_sv,
                                    lambda: FrameUtil.fileopen(self.music_path_sv))
        play_button = FrameUtil.make_button(self.root, "播放", self.play_music)

        file_frame.grid(row=0, column=0, sticky=W)
        play_button.grid(row=1, column=0)

    def play_music(self):
        path = self.music_path_sv.get()
        t = multiprocessing.Process(target=Visualization.start_music, args=(path,))
        t.start()


class FrameUtil:
    @staticmethod
    def make_text(root, title):
        frame = Frame(root)
        label = Label(frame, text=title)
        text = Text(frame)
        label.grid(row=0, column=0, stick=W)
        text.grid(row=1, column=0)
        return frame, text

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

    @staticmethod
    def make_value_choose(root, title, values, sv, init):
        frame = Frame(root)
        label = Label(frame, width=20, text=title)
        label.grid(row=0, column=0)
        sv.set(init)
        i = 1
        for t, n in values:
            rb = Radiobutton(frame, text=t, value=n, variable=sv)
            rb.grid(row=0, column=i)
            i += 1
        return frame

    @staticmethod
    def fileopen(sv):
        sv.set('')
        file_name = askopenfilename()
        if file_name:
            sv.set(file_name)


def main():
    root = Tk()
    root.title("播放音乐")
    MusicPlayerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()