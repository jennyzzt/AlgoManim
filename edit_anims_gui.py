
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
import sys

from pathlib import Path
from argparse import Namespace
import manimlib.config
import manimlib.constants
from manimlib.extract_scene import get_scene_classes_from_module, get_scenes_to_render

VIDEO_NAME = Path().absolute() / "media/videos/bubblesort/480p15/BubbleSortScene.mp4"

def extract_scene(file_path, scene_name):
    args = Namespace(color=None, file=file_path, file_name=None,
        high_quality=False, leave_progress_bars=False, low_quality=True, media_dir=None,
        medium_quality=False, preview=True, quiet=False, resolution=None, save_as_gif=False,
        save_last_frame=False, save_pngs=False, scene_names=[scene_name],
        show_file_in_finder=False, sound=False, start_at_animation_number=None,
        tex_dir=None, transparent=False, video_dir=None, video_output_dir=None,
        write_all=False, write_to_movie=False)
    config = manimlib.config.get_configuration(args)
    manimlib.constants.initialize_directories(config)

    module = config["module"]
    all_scene_classes = get_scene_classes_from_module(module)
    scene_class = get_scenes_to_render(all_scene_classes, config)[0]

    scene_kwargs = dict([
        (key, config[key])
        for key in [
            "camera_config",
            "file_writer_config",
            "skip_animations",
            "start_at_animation_number",
            "end_at_animation_number",
            "leave_progress_bars",
        ]
    ])

    return scene_class(**scene_kwargs)

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        # render scene programmatically first
        scene = extract_scene('algomanim/bubblesort.py', 'BubbleSortScene')

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

    def position_changed(self, position):
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
