import sys

from PyQt6 import QtCore
from PyQt6.QtCore import QSize, Qt, QPoint, QRect
from PyQt6.QtGui import QIcon, QAction, QColor, QPixmap, QFont, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, \
    QGraphicsColorizeEffect, QToolBar, QSlider, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog


class Canvas(QLabel):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap(800, 500)
        pixmap.fill(Qt.GlobalColor.white)
        self.setPixmap(pixmap)

        self.last_x, self.last_y = None, None
        self.pen_color = QColor('#000000')
        self.pen_size = 4

    def clear(self):
        pixmap = QPixmap(800, 500)
        pixmap.fill(Qt.GlobalColor.white)
        self.setPixmap(pixmap)

    def set_pen_color(self, c):
        self.pen_color = c

    def mouseMoveEvent(self, e):
        if self.last_x is None:
            self.last_x = e.position().x()
            self.last_y = e.position().y()

        canvas = self.pixmap()
        painter = QPainter(canvas)
        p = painter.pen()
        p.setWidth(self.pen_size)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawLine(int(self.last_x), int(self.last_y), int(e.position().x()), int(e.position().y()))
        painter.end()
        self.setPixmap(canvas)

        self.last_x = e.position().x()
        self.last_y = e.position().y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None

COLORS = [
    '#000000', '#333333', '#666666', '#999999', '#ffffff', '#ff0000', '#ff4500',
    '#ff8c00', '#ffa500', '#ffd700', '#ffff00', '#9acd32', '#32cd32', '#008000',
    '#006400', '#00ced1', '#4682b4', '#0000ff', '#4b0082', '#8a2be2', '#9400d3',
    '#c71585', '#ff1493', '#ff69b4', '#ffc0cb', '#a52a2a', '#8b4513', '#d2691e',
    '#f4a460', '#deb887',
]

class QPaletteButton(QPushButton):
    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QSize(24, 24))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Picasso")
        # Создание меню
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu("File")
        # Создание действий для меню
        new_img_action = QAction(QIcon("icons/new-image.png"), "New", self)
        open_action = QAction(QIcon("icons/open-image.png"), "Open", self)
        save_action = QAction(QIcon("icons/save-image.png"), "Save", self)

        file_menu.addAction(new_img_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        # Устанавливаем размер окна
        self.setFixedSize(QSize(800, 600))

        self.canvas = Canvas()
        w = QWidget()
        l = QVBoxLayout()
        w.setLayout(l)
        l.addWidget(self.canvas)
        self.setCentralWidget(w)

        self.setFixedSize(QSize(800, 600))

        palette = QHBoxLayout()
        self.add_palette_buttons(palette)
        l.addLayout(palette)

        # Привязка действий меню к функциям
        new_img_action.triggered.connect(self.new_img)
        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_img)

        # Создание панели инструментов
        self.fileToolbar = QToolBar(self)
        self.fileToolbar.setIconSize(QSize(16, 16))
        self.fileToolbar.setObjectName("fileToolbar")
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.fileToolbar)

        self.sliderToolbar = QToolBar(self)
        self.sliderToolbar.setIconSize(QtCore.QSize(16, 16))
        self.sliderToolbar.setObjectName("sliderToolbar")
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.sliderToolbar)

        self.drawingToolbar = QToolBar(self)
        self.drawingToolbar.setIconSize(QtCore.QSize(16, 16))
        self.drawingToolbar.setObjectName("drawingToolbar")
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.drawingToolbar)

        # Создание значка и ползунка (слайдера)
        sizeicon = QLabel()
        sizeicon.setPixmap(QPixmap('icons/border-weight.png'))
        self.sliderToolbar.addWidget(sizeicon)
        self.sizeselect = QSlider()
        self.sizeselect.setRange(10, 70)
        self.sizeselect.setOrientation(Qt.Orientation.Horizontal)
        self.sliderToolbar.addWidget(self.sizeselect)

        self.sizeselect.valueChanged.connect(self.change_pen_size)

        pen_icon = QIcon()
        pen_icon.addPixmap(QPixmap('icons/paint-brush.png'))

        self.brushButton =QPushButton()
        self.brushButton.setIcon(pen_icon)
        self.brushButton.setCheckable(True)
        self.drawingToolbar.addWidget(self.brushButton)

        can_icon = QIcon()
        can_icon.addPixmap(QPixmap('icons/paint-can.png'))

        self.canButton = QPushButton()
        self.canButton.setIcon(can_icon)
        self.canButton.setCheckable(True)
        self.drawingToolbar.addWidget(self.canButton)

        eraser_icon = QIcon()
        eraser_icon.addPixmap(QPixmap('icons/eraser.png'))

        self.eraserButton = QPushButton()
        self.eraserButton.setIcon(eraser_icon)
        self.eraserButton.setCheckable(True)
        self.drawingToolbar.addWidget(self.eraserButton)

        new_file_icon = QIcon()
        new_file_icon.addPixmap(QPixmap('icons/new-image.png'))

        self.newFileButton = QPushButton()
        self.newFileButton.setIcon(new_file_icon)
        self.newFileButton.setObjectName("newFileButton")
        self.fileToolbar.addWidget(self.newFileButton)

        open_file_icon = QIcon()
        open_file_icon.addPixmap(QPixmap('icons/open-image.png'))

        self.openFileButton = QPushButton()
        self.openFileButton.setIcon(open_file_icon)
        self.openFileButton.setObjectName("openFileButton")
        self.fileToolbar.addWidget(self.openFileButton)

        save_file_icon = QIcon()
        save_file_icon.addPixmap(QPixmap('icons/save-image.png'))

        self.saveFileButton = QPushButton()
        self.saveFileButton.setIcon(save_file_icon)
        self.saveFileButton.setObjectName("saveFileButton")
        self.fileToolbar.addWidget(self.saveFileButton)

        copy_file_icon = QIcon()
        copy_file_icon.addPixmap(QPixmap('icons/copy-image.png'))

        self.copyFileButton = QPushButton()
        self.copyFileButton.setIcon(copy_file_icon)
        self.copyFileButton.setObjectName("copyFileButton")
        self.fileToolbar.addWidget(self.copyFileButton)

        self.newFileButton.clicked.connect(self.new_img)
        self.openFileButton.clicked.connect(self.open_file)
        self.saveFileButton.clicked.connect(self.save_img)
        self.copyFileButton.clicked.connect(self.copy_to_clipboard)

    def add_palette_buttons(self, layout):
        for color in COLORS:
            b = QPaletteButton(color)
            b.pressed.connect(lambda c=color: self.canvas.set_pen_color(QColor(c)))
            layout.addWidget(b)

    def change_pen_size(self, s):
        self.canvas.pen_size = s

    def change_color(self, color):
        color_effect = QGraphicsColorizeEffect()
        color_effect.setColor(QColor(color))
        self.label.setGraphicsEffect(color_effect)

    def new_img(self):
        self.canvas.clear()

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                              "PNG image files (*.png); JPEG image files (*jpg); All files (*.*)")

        if path:
            pixmap = QPixmap()
            pixmap.load(path)

            iw, ih = pixmap.width(), pixmap.height()

            cw, ch = 800, 500

            if iw / cw < ih / ch:
                pixmap = pixmap.scaledToWidth(cw)
                hoff = (pixmap.height() - ch) // 2
                pixmap = pixmap.copy(
                    QRect(QPoint(0, hoff), QPoint(cw, pixmap.height() - hoff))
                )

            elif iw / cw > ih / ch:
                pixmap = pixmap.scaledToHeight(ch)
                woff = (pixmap.width() - cw) // 2
                pixmap = pixmap.copy(
                    QRect(QPoint(woff, 0), QPoint(pixmap.width() - woff, ch))
                )
            self.canvas.setPixmap(pixmap)

    def save_img(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save File', "", "PNG Image file (*.png)")
        if path:
            pixmap = self.canvas.pixmap()
            pixmap.save(path, "PNG")

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(self.canvas.pixmap())

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
