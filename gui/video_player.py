
from PyQt5.QtCore import QDir, Qt, QUrl, QSizeF
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt5.QtWidgets import *

# 16:9 ratio
VIDEO_WIDTH = 480
VIDEO_HEIGHT = 270


class VideoPlayerWidget(QWidget):
    def __init__(self, video_fp, parent=None):
        super(VideoPlayerWidget, self).__init__(parent)

        self.video_fp = video_fp

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Supporting infrastructure to display media player
        video_item = QGraphicsVideoItem()
        video_item.setSize(QSizeF(VIDEO_WIDTH, VIDEO_HEIGHT))
        scene = QGraphicsScene(self)
        scene.addItem(video_item)
        graphics_view = QGraphicsView(scene)

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

        # Wire up media player
        self.mediaPlayer.setVideoOutput(video_item)
        self.mediaPlayer.stateChanged.connect(self.media_state_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.mediaPlayer.error.connect(self.handle_error)

        # Arrange video controls
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.addWidget(self.playButton)
        control_layout.addWidget(self.positionSlider)

        # Arrange widget contents
        main_layout = QVBoxLayout()
        main_layout.addWidget(graphics_view)
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.errorLabel)

        self.setLayout(main_layout)

    def open_video(self):
        file = QDir.current().filePath(str(self.video_fp))
        self.mediaPlayer.setMedia(
            QMediaContent(QUrl.fromLocalFile(file)))

        # Enable play button and un-grey it
        self.playButton.setEnabled(True)
        self.playButton.setStyleSheet("QPushButton::enabled")

        # Show first scene of video
        self.mediaPlayer.play()
        self.mediaPlayer.pause()

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

    def position_changed(self, position):
        self.positionSlider.setValue(position)

    def duration_changed(self, duration):
        self.positionSlider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def handle_error(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())
