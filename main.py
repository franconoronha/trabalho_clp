from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QImage, QPixmap, qRgb
import ctypes
import math
import sys
import os

if os.name == "nt":
    suffix = ".dll"
else:
    suffix = ".so"

path = os.getcwd() + "\\shared" + suffix
shared = ctypes.CDLL(path)

def mandelbrot_set(ponto):
    # https://www.youtube.com/watch?v=6z7GQewK-Ks copiei desse video? talvez tenha coisas melhores
    # tem que passar isso pro C++ depois
    # minha ideia é que tu mande os limites inferiores/superiores e resolução
    # e ele retorne uma matriz de cores RGB
    # ou então um número que possa ser mapeado pra cores
    max_iterations = 100
    a = ponto[0] # real
    b = ponto[1] # imaginario

    ca = a # ponto incial
    cb = b
    
    n = 0
    while n < max_iterations:
        aa = a * a - b * b
        bb = 2 * a * b
        a = aa + ca
        b = bb + cb

        if(abs(a + b) > 16):
            break

        n += 1

    bright = math.floor((n / max_iterations) * 255)
    return bright

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    xpos, y_pos, width, height = 300, 300, 600, 600
    win.setGeometry(xpos, y_pos, width, height)
    win.setWindowTitle("Fractal de Mandelbrot")

    img_width, img_height = 600, 600
    img = QImage(img_width, img_height, QImage.Format_RGB32)

    limite_superior = 2
    limite_inferior = -2
    largura_total = 4

    w_step_size = largura_total / img_width
    h_step_size = largura_total / img_height 

    for x in range(img_width):
        for y in range(img_height):
            ponto = (limite_inferior + x * (w_step_size), limite_superior - y * (h_step_size))
            brilho = mandelbrot_set(ponto)
            img.setPixel(x, y, qRgb(brilho, brilho, brilho))

    pixmap = QPixmap.fromImage(img)
    imageDisplay = QLabel(win)
    imageDisplay.setGeometry(0, 0, img_width, img_height)
    imageDisplay.setPixmap(pixmap)

    win.show()
    sys.exit(app.exec_())

window()