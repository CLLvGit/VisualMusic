# VisualMusic
计算机图形学 PJ1 编程实现音乐节奏或旋律的可视化\
吕承亮 16307130144 \
\
**程序说明** 
1. 运行方法 \
    运行./dist目录下的可执行程序 MusicPlayerGUI.exe。在弹出的界面中，点击“选择”按钮，选择一个音乐文件（支持wav/mp3）。点击开始，程序将播放选择的音乐并显示图像。
2. 开发环境 \
    使用python2.7开发 \
    主要的第三方库有：
    1) pydub， wave，用于音频文件的处理
    2) pygame，用于播放音乐
    3) OpenGL，用于渲染图像
3. 程序实现原理
    1) pydub的AudioSegment将音乐文件转换为wav格式，然后使用wave读取文件的声道数以及各采样点数据
    2) 根据声道以及采样点数据，使用OpenGL绘制动态图形，主要根据采样点数值大小，改变圆形图像的半径和颜色
    3) 使用pygame，同步播放音乐