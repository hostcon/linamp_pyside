# ==========================================================
# PLAYER COM PYSIDE (MODERNO E MAIS LIVRE)
# Prof. Wagner R. Silva
# ==========================================================

import sys
import os
import pygame
from mutagen.mp3 import MP3

from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QListWidget, QLabel, QFileDialog, QSlider
)
from PySide6.QtCore import Qt, QTimer

pygame.mixer.init()

class Player(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Player PySide")
        self.resize(400, 500)

        self.playlist = []
        self.index = 0
        self.duracao = 0

        layout = QVBoxLayout()

        self.label = QLabel("Nenhuma música")
        layout.addWidget(self.label)

        self.lista = QListWidget()
        self.lista.clicked.connect(self.selecionar)
        layout.addWidget(self.lista)

        self.slider = QSlider(Qt.Horizontal)
        layout.addWidget(self.slider)

        self.btn_load = QPushButton("Carregar")
        self.btn_play = QPushButton("Play")
        self.btn_pause = QPushButton("Pause")

        self.btn_load.clicked.connect(self.carregar)
        self.btn_play.clicked.connect(self.tocar)
        self.btn_pause.clicked.connect(self.pausar)

        layout.addWidget(self.btn_load)
        layout.addWidget(self.btn_play)
        layout.addWidget(self.btn_pause)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar)
        self.timer.start(1000)

    def carregar(self):
        arquivos, _ = QFileDialog.getOpenFileNames(self, "MP3", "", "MP3 (*.mp3)")
        for a in arquivos:
            self.playlist.append(a)
            self.lista.addItem(os.path.basename(a))

    def tocar(self):
        if not self.playlist:
            return

        arquivo = self.playlist[self.index]

        pygame.mixer.music.load(arquivo)
        pygame.mixer.music.play()

        audio = MP3(arquivo)
        self.duracao = int(audio.info.length)

        self.label.setText(os.path.basename(arquivo))
        self.slider.setMaximum(self.duracao)

    def pausar(self):
        pygame.mixer.music.pause()

    def selecionar(self):
        self.index = self.lista.currentRow()
        self.tocar()

    def atualizar(self):
        if pygame.mixer.music.get_busy():
            pos = pygame.mixer.music.get_pos() // 1000
            self.slider.setValue(pos)


app = QApplication(sys.argv)
janela = Player()
janela.show()
sys.exit(app.exec())
