from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QImage, QPixmap, qRgb
import ctypes
import sys
import os

if os.name == "nt":
    suffix = ".dll"
else:
    suffix = ".so"

path = os.getcwd() + "\\shared" + suffix
shared = ctypes.CDLL(path)

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    xpos, y_pos, width, height = 300, 300, 600, 600
    win.setGeometry(xpos, y_pos, width, height)
    win.setWindowTitle("Fractal de Mandelbrot")

    img_width, img_height = 300, 300
    img = QImage(img_width, img_height, QImage.Format_RGB32)
    for x in range(img_width):
        for y in range(img_height):
            img.setPixel(x, y, qRgb(0, 0, 255))

    pixmap = QPixmap.fromImage(img)
    imageDisplay = QLabel(win)
    imageDisplay.setGeometry(0, 0, img_width, img_height)
    imageDisplay.setPixmap(pixmap)

    win.show()
    sys.exit(app.exec_())

window()