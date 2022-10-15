from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QImage, QPixmap, qRgb
from PyQt5.QtCore import Qt
from ctypes import *
import sys
import os
import time

if sys.platform.startswith("linux"):
    suffix = ".so"
elif sys.platform == "darwin":
    suffix = ".dylib"
else:
    suffix = ".dll"

path = os.getcwd() + "\\shared" + suffix
shared = CDLL(path)

shared.createArray.argtypes = [POINTER((POINTER(c_int))), c_int]
shared.createArray.restype = None

shared.calcArrayMandelbrot.argtypes = [POINTER(c_int), c_double, c_double, c_int, c_double]
shared.calcArrayMandelbrot.restype = None

shared.release.argtypes = [POINTER(c_int)]
shared.release.restype = None


class TelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.modo = True
        x_pos, y_pos, width, height = 300, 300, 600, 600 # manter width = height

        self.setGeometry(x_pos, y_pos, width, height)
        self.setWindowTitle("Fractal de Mandelbrot")

        self.limite_superior, self.limite_inferior = 2, -2
        self.offset_x, self.offset_y = 0, 0

        self.imageDisplay = QLabel(self)
        self.imageDisplay.setGeometry(0, 0, width, height)

        self.img = QImage(width, height, QImage.Format_RGB32)
    
        self.arrayMandelbrot = POINTER(c_int)()
        shared.createArray(self.arrayMandelbrot, width * height)

    def draw(self):
        largura_total = self.limite_superior - self.limite_inferior
        base_x = self.limite_inferior + self.offset_x
        base_y = self.limite_superior + self.offset_y
        size = self.img.height() # largura === altura

        shared.calcArrayMandelbrot(self.arrayMandelbrot, base_x, base_y, size, largura_total)

        for x in range(size):
            for y in range(size):
                val = self.arrayMandelbrot[x * size + y]
                self.img.setPixel(x, y, qRgb(val, val, val))

        pixmap = QPixmap.fromImage(self.img)
        self.imageDisplay.setPixmap(pixmap)
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_W:
            start = time.time()
            self.offset_y += 0.1
            self.draw()
            end = time.time()
            print(end - start)
        elif e.key() == Qt.Key_A:
            start = time.time()
            self.offset_x -= 0.1
            self.draw()
            end = time.time()
            print(end - start)
        elif e.key() == Qt.Key_S:
            start = time.time()
            self.offset_y -= 0.1
            self.draw()
            end = time.time()
            print(end - start)
        elif e.key() == Qt.Key_D:
            start = time.time()
            self.offset_x += 0.1
            self.draw()
            end = time.time()
            print(end - start)
        elif e.key() == Qt.Key_T:
            self.modo = not self.modo
            self.draw()
        elif e.key() == Qt.Key_R:
            self.offset_x, self.offset_y = 0, 0

    def closeEvent(self, event):
        shared.release(self.arrayMandelbrot)
        event.accept()

def main():
    app = QApplication(sys.argv)
    win = TelaPrincipal()
    win.draw()
    win.show()
    sys.exit(app.exec_())

main()