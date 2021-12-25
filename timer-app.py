import sys
import datetime

from PyQt5.QtCore import QTimer, Qt, QTime, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, \
    QTimeEdit, QFileDialog


class Timer(QWidget):
    WIDTH = 300
    HEIGHT = 400
    BUTTON_MARGIN = 10
    BUTTON_HEIGHT = 100
    BUTTON_WIDTH = (WIDTH - 4 * BUTTON_MARGIN) // 3
    TIMER_LABEL_WIDTH = 50

    def __init__(self):
        super().__init__()
        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle('Timer')
        self._init_ui()
        self._init_timer()
        self.player = QMediaPlayer()
        self.player.setVolume(50)
        self.show()

    def _init_ui(self):
        self._init_buttons()
        self._init_label()
        self._init_timer_edit()

    def _init_buttons(self):
        self.choose_file = QPushButton('Set Sound', self)
        self.start_button = QPushButton('Start', self)
        self.pause_button = QPushButton('Pause', self)
        self.stop_button = QPushButton('Stop', self)
        self.start_button.clicked.connect(self._start_timer)
        self.pause_button.clicked.connect(self._pause_timer)
        self.stop_button.clicked.connect(self._stop_timer)
        self.choose_file.clicked.connect(self._open_music_file_dialog)
        self.start_button.resize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.start_button.move(self.BUTTON_MARGIN,
                               self.HEIGHT - self.BUTTON_HEIGHT - self.BUTTON_MARGIN)
        self.pause_button.resize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.pause_button.move(self.BUTTON_MARGIN * 2 + self.BUTTON_WIDTH,
                               self.HEIGHT - self.BUTTON_HEIGHT - self.BUTTON_MARGIN)
        self.stop_button.resize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.stop_button.move(self.BUTTON_MARGIN * 3 + self.BUTTON_WIDTH * 2,
                              self.HEIGHT - self.BUTTON_HEIGHT - self.BUTTON_MARGIN)

    def _init_label(self):
        self.timer_label = QLabel('SET TIME', self)
        self.timer_label.resize(self.TIMER_LABEL_WIDTH, 100)
        self.timer_label.move((self.WIDTH - self.TIMER_LABEL_WIDTH) // 2, 100)
        self.timer_label.setAlignment(Qt.AlignHCenter)

    def _init_timer_edit(self):
        self.timer_edit = QTimeEdit(self)
        self.timer_edit.setDisplayFormat('hh:mm:ss')
        self.timer_edit.move((self.WIDTH - self.TIMER_LABEL_WIDTH) // 2, 150)
        self.timer_edit.setAlignment(Qt.AlignCenter)
        self.is_paused = False
        self.is_started = False

    def _start_timer(self):
        if not self.is_paused:
            self.remaining_time = self.timer_edit.time()
        self._refresh_time_on_ui()
        self.is_started = True
        self.is_paused = False

    def _pause_timer(self):
        if self.is_started:
            self.is_paused = True
        self.is_started = False

    def _stop_timer(self):
        self.is_paused = False
        self.is_started = False
        self.remaining_time = QTime(0, 0, 0)
        self._refresh_time_on_ui()
        self.player.stop()

    def _refresh_time_on_ui(self):
        self.timer_label.setText(
            self.remaining_time.toPyTime().strftime("%H:%M:%S"))

    def _init_timer(self):
        self.is_started = False
        self.remaining_time: QTime = self.timer_edit.time()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._show_time)
        self.timer.start(1000)

    def _show_time(self):
        if self.is_started and self.remaining_time != QTime(0, 0, 0):
            self.remaining_time = self.remaining_time.addSecs(-1)
            if self.remaining_time == QTime(0, 0, 0):
                self._timeout_event()
            self._refresh_time_on_ui()

    def _timeout_event(self):
        self.is_started = False
        self.player.play()

    def _open_music_file_dialog(self):
        file = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',
                                            "Music files (*.mp3 *.ogg *.wav)")
        if file:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file[0])))
            return


def fromSeconds(seconds: int):
    return str(datetime.timedelta(seconds=seconds))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    timer = Timer()
    sys.exit(app.exec_())
