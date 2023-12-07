import sys
import time
import os

import cv2
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QSlider,
)


class VideoPlayer(QWidget):
    __TICK_INTERVAL = 200
    __FRAME_RATE = 30

    def __init__(self, file_path: str, start_frame: int):
        super().__init__()
        self.start_frame = start_frame
        self.file_path = file_path
        self.total_frames = VideoPlayer.__total_video_frames(file_path)
        self.video_name = os.path.basename(file_path)  # Get video name
        print(f"Total Frames: {self.total_frames}")
        print(f"Start Frame: {self.start_frame}")
        print(f"Video Name: {self.video_name}")
        print(self.total_frames)
        self.__initUI()

    def __initUI(self):

        # Set the window title and size
        self.setWindowTitle("Video Player")
        self.setGeometry(200, 200, 850, 850)

        # Video display
        self.label = QLabel(self)
        # Main layout
        self.vbox = QVBoxLayout()

        # Change 2: Adding labels for start frame and video name
        self.info_label = QLabel(f"Start Frame: {self.start_frame} | Video: {self.video_name}", self)
        self.vbox.addWidget(self.info_label)

        self.vbox.addWidget(self.label)
        self.setLayout(self.vbox)

        self.video = QVideoWidget()
        # self.video.move(0, 0)
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.video)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.file_path)))
        self.player.setPosition(VideoPlayer.__frame_to_ms(self.start_frame))
        self.video.show()
        self.player.play()
        time.sleep(0.001)
        self.player.pause()
        self.vbox.addWidget(self.video)

        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_slider.setMinimum(0)
        self.seek_slider.setMaximum(self.total_frames)
        self.seek_slider.setValue(self.start_frame)
        # self.seek_slider.sliderMoved.connect(self.__seek_move)
        self.seek_slider.sliderReleased.connect(self.__seek)
        #self.seek_slider.sliderPressed.connect(self.__seek)
        self.vbox.addWidget(self.seek_slider)

        # Buttons
        self.bbox = QHBoxLayout()
        self.play_button = QPushButton("Play", self)
        self.pause_button = QPushButton("Pause", self)
        self.reset_button = QPushButton("Reset", self)

        self.bbox.addWidget(self.play_button)
        self.bbox.addWidget(self.pause_button)
        self.bbox.addWidget(self.reset_button)

        self.vbox.addLayout(self.bbox)

        self.play_button.clicked.connect(self.__play)
        self.pause_button.clicked.connect(self.__pause)
        self.reset_button.clicked.connect(self.__reset)

        self.play_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.reset_button.setEnabled(True)

        self.timer = QTimer(self)
        self.timer.setInterval(self.__TICK_INTERVAL)
        self.timer.timeout.connect(self.__update_timer)
        self.timer.start()

    def __play(self):
        self.player.play()
        self.play_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.timer.start()

    def __pause(self):
        self.player.pause()
        self.pause_button.setEnabled(False)
        self.play_button.setEnabled(True)
        self.timer.stop()

    def __reset(self):
        self.player.setPosition(VideoPlayer.__frame_to_ms(0))
        self.seek_slider.setValue(0)
        self.play_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.player.pause()

    def __seek(self):
        new_frame = self.seek_slider.value()
        new_position_ms = self.__frame_to_ms(new_frame)
        self.seek_slider.setValue(new_frame)
        self.player.setPosition(new_position_ms)

    def __update_timer(self):
        frames_per_tick = int((self.__FRAME_RATE / 1000) * self.__TICK_INTERVAL)
        current_position_ms = self.player.position()
        current_frame = int((current_position_ms / 1000) * self.__FRAME_RATE)
        new_frame = current_frame + frames_per_tick
        self.seek_slider.setValue(new_frame)

    @staticmethod
    def __total_video_frames(file_path: str):
        video = cv2.VideoCapture(file_path)
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
        return int(frame_count)

    @staticmethod
    def __frame_to_ms(frame_number: int):
        return frame_number // 30 * 1000


def play_video(file_path, start_frame):
    app = QApplication(sys.argv)
    v = VideoPlayer(file_path, start_frame)
    v.show()
    app.exec_()
    
# The following part is only executed if this script is run as the main script,
# not when it's imported as a module in another script
if __name__ == '__main__':
    file_path = sys.argv[1]
    start_frame = int(sys.argv[2])
    play_video(file_path, start_frame)