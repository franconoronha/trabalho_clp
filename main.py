from turtle import shearfactor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QImage, QPixmap, qRgb
from PyQt5.QtCore import Qt
from ctypes import *
import math
import sys
import os
import time

if os.name == "nt": #acho que tem que usar plaftorm.platform() pra mac??
    suffix = ".dll"
else:
    suffix = ".so"

path = os.getcwd() + "\\shared" + suffix
shared = CDLL(path)
shared.findMandelbrot.argtypes = [c_double, c_double, c_int]
shared.findMandelbrot.restype = c_int

shared.testeArray.argtypes = [POINTER(POINTER(c_int))]
shared.testeArray.restype = None
shared.release.argtypes = [POINTER(c_int)]
shared.release.restype = None

p = POINTER(c_int)()
shared.testeArray(p, 10)
for i in range(10):
    print(p[i])

shared.release(p)

def mandelbrot_set(ponto):
    # https://www.youtube.com/watch?v=6z7GQewK-Ks copiei desse video talvez tenha coisas melhores
    # tem que passar isso pro C++ depois
    # minha ideia é que tu mande os limites inferiores/superiores e resolução
    # e ele retorne uma matriz de cores RGB
    # ou então um número que possa ser mapeado pra cores
    max_iterations = 100
    n = 0

    cr, ci = ponto[0], ponto[1] 
    zr, zi = 0, 0
    while zr * zr + zi * zi < 4 and n < max_iterations:
        tempr = zr * zr - zi * zi + cr
        tempi = zr * zi
        zi = tempi + tempi + ci
        zr = tempr
        n += 1

    brilho = math.floor((n / max_iterations) * 255)
    return brilho

class TelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.modo = True
        x_pos, y_pos, width, height = 300, 300, 600, 600

        self.setGeometry(x_pos, y_pos, width, height)
        self.setWindowTitle("Fractal de Mandelbrot")

        self.limite_superior, self.limite_inferior = 2, -2
        self.offset_x, self.offset_y = 0, 0

        self.img_width, self.img_height = 600, 600
        self.imageDisplay = QLabel(self)
        self.imageDisplay.setGeometry(0, 0, self.img_width, self.img_height)

        self.img = QImage(self.img_width, self.img_height, QImage.Format_RGB32)

    def draw(self):
        largura_total = self.limite_superior - self.limite_inferior
        w_step_size = largura_total / self.img_width
        h_step_size = largura_total / self.img_height 

        base_x = self.limite_inferior + self.offset_x
        base_y = self.limite_superior + self.offset_y

        for x in range(self.img_width):
            for y in range(self.img_height):

                ponto = (base_x + x * (w_step_size), base_y - y * (h_step_size))
                #brilho = mandelbrot_set(ponto)
                # primeiro teste
                brilho = shared.findMandelbrot(ponto[0], ponto[1], 100)
                self.img.setPixel(x, y, qRgb(brilho, brilho, brilho))

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

            
def main():
    app = QApplication(sys.argv)
    win = TelaPrincipal()
    win.draw()
    win.show()
    sys.exit(app.exec_())

main()