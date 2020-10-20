
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
import sys

from pathlib import Path
from custom_renderer import custom_renderer

VIDEO_NAME = Path().absolute() / "media/videos/bubblesort/480p15/BubbleSortScene.mp4"

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        # render scene programmatically first
        self.anims = custom_renderer('algomanim/bubblesort.py', 'BubbleSortScene')
        # self.anims = [{'start_index': x, 'end_index': x + 3 if x == 1 else x, 'action_pairs': [],
        #    'run_time': 1 if x % 2 == 0 else 0.5, 'start_time': x} for x in range(10)]

        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("AlgoManimHelper")

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        video_widget = QVideoWidget()

        # Play button
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        # Video scrubber
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.set_position)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Animation Scrubber
        animListLayout = QHBoxLayout()
        self.animLbls = []
        for anim in self.anims:
            desc = f'Animation\n{anim["start_index"] + 1}' if anim['start_index'] == anim['end_index'] \
                else f'Animation\n{anim["start_index"] + 1} - {anim["end_index"] + 1}'
            animLbl = QLabel(desc)
            animLbl.setStyleSheet("background-color: white; color: black")
            animLbl.setAlignment(Qt.AlignCenter)
            animLbl.setWordWrap(True)
            animLbl.setFixedHeight(60)
            width = max(int(150 * anim['run_time']), 80)
            animLbl.setFixedWidth(width)
            self.animLbls.append(animLbl)
            animListLayout.addWidget(animLbl)
        animListBox = QGroupBox()
        animListBox.setLayout(animListLayout)
        self.animListScroll = QScrollArea()
        self.animListScroll.setWidget(animListBox)
        self.animListScroll.setFixedHeight(100)

        # Widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Layouts to place inside widget
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.addWidget(self.playButton)
        control_layout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(video_widget)
        layout.addLayout(control_layout)
        layout.addWidget(self.animListScroll)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(video_widget)
        self.mediaPlayer.stateChanged.connect(self.media_state_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.mediaPlayer.error.connect(self.handle_error)

        # open file
        file = QDir.current().filePath(str(VIDEO_NAME))
        self.mediaPlayer.setMedia(
            QMediaContent(QUrl.fromLocalFile(file)))
        self.playButton.setEnabled(True)

    def exit_call(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def media_state_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def set_active_lbl(self, index):
        self.animLbls[index].setStyleSheet("background-color: #2980b9; color: white")

    def set_inactive_lbl(self, index):
        self.animLbls[index].setStyleSheet("background-color: white; color: black")

    def position_changed(self, position):
        for (i, anim) in enumerate(self.anims):
            start_time = anim['start_time'] * 1000
            end_time = (anim['start_time'] + anim['run_time']) * 1000
            if position >= start_time and position <= end_time:
                self.set_active_lbl(i)
                self.animListScroll.ensureWidgetVisible(self.animLbls[i])
            else:
                self.set_inactive_lbl(i)

        self.positionSlider.setValue(position)

    def duration_changed(self, duration):
        self.positionSlider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def handle_error(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())
