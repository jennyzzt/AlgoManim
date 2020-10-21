
from PyQt5.QtCore import Qt, QUrl, QSizeF
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

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Supporting infrastructure to display media player
        video_item = QGraphicsVideoItem()
        video_item.setSize(QSizeF(VIDEO_WIDTH, VIDEO_HEIGHT))
        scene = QGraphicsScene(self)
        scene.addItem(video_item)
        graphics_view = QGraphicsView(scene)

        # Play button
        self.play_button = QPushButton()
        self.play_button.setEnabled(False)
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.clicked.connect(self.play)

        # Video scrubber
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.valueChanged.connect(self.slider_position_changed)

        self.error_label = QLabel()
        self.error_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Wire up media player
        self.media_player.setVideoOutput(video_item)
        self.media_player.stateChanged.connect(self.media_state_changed)
        self.media_player.positionChanged.connect(self.media_position_changed)
        self.media_player.durationChanged.connect(self.media_duration_changed)
        self.media_player.error.connect(self.handle_error)

        # Arrange video controls
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.position_slider)

        # Arrange widget contents
        main_layout = QVBoxLayout()
        main_layout.addWidget(graphics_view)
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.error_label)

        self.setLayout(main_layout)

    def open_video(self):
        self.media_player.setMedia(
            QMediaContent(QUrl.fromLocalFile(str(self.video_fp))))

        # Enable play button and un-grey it
        self.play_button.setEnabled(True)
        self.play_button.setStyleSheet("QPushButton::enabled")

        # Show first scene of video
        self.media_player.play()
        self.media_player.pause()

    def play(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def slider_position_changed(self, position):
        self.media_player.setPosition(position)

    def media_state_changed(self, state):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def media_position_changed(self, position):
        self.position_slider.blockSignals(True)
        self.position_slider.setValue(position)
        self.position_slider.blockSignals(False)

    def media_duration_changed(self, duration):
        self.position_slider.setRange(0, duration)

    def handle_error(self):
        self.play_button.setEnabled(False)
        self.error_label.setText("Error: " + self.media_player.errorString())
