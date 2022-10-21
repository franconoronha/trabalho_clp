from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QImage, QPixmap, qRgb, QIcon, QFont
from PyQt5.QtCore import Qt
from ctypes import *
import sys
import os

# Carrega a biblioteca em C++ levando em conta o SO
if sys.platform == "win32":
    lib_file = "\\shared.dll"
else:
    lib_file = "/shared.so"

path = os.getcwd() + lib_file
shared = CDLL(path)
#

# Define os tipos dos argumentos e retornos das funções da biblioteca, para conversão automática
shared.createArray.argtypes = [POINTER((POINTER(c_int))), c_int]
shared.createArray.restype = None

shared.calcArrayMandelbrot.argtypes = [POINTER(c_int), c_double, c_double, c_int, c_double]
shared.calcArrayMandelbrot.restype = None

shared.release.argtypes = [POINTER(c_int)]
shared.release.restype = None
#

# Definindo uma tela principal extendendo a classe padrão
class TelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Definição dos elementos básicos da tela
        x_pos, y_pos, width, height = 300, 300, 600, 600 # manter width = height
        self.setGeometry(x_pos, y_pos, width, height + 100)
        self.setWindowTitle("Fractal de Mandelbrot")
        self.setWindowIcon(QIcon("icon.png"))
        #

        # Condição inicial do fractal
        self.limite_superior, self.limite_inferior = 2, -2
        self.offset_x, self.offset_y = 0, 0
        #

        # Criação do elemento de imagem(vazio)
        self.imageDisplay = QLabel(self)
        self.imageDisplay.setGeometry(0, 0, width, height)
        self.img = QImage(width, height, QImage.Format_RGB32)
        #

        # Criação e definição das labels da legenda 
        self.label_1 = QLabel("W: mover para cima | A: mover para esquerda | D: mover para direta | S: mover para baixo", self)
        self.label_2 = QLabel("Z: zoom-in | X: zoom-out | C: zoom-in grande | V: zoom-out grande | R: reset",self)
        self.label_1.setFont(QFont('Arial', 10))
        self.label_2.setFont(QFont('Arial', 10))
        self.label_1.setGeometry(0, height + 10, width, 40)
        self.label_2.setGeometry(0, height + 50, width, 40)
        self.label_1.setAlignment(Qt.AlignCenter)
        self.label_2.setAlignment(Qt.AlignCenter)
        #

        # Criação e alocação do array que é compartilhado entre C++ e Python
        self.arrayMandelbrot = POINTER(c_int)()
        shared.createArray(self.arrayMandelbrot, width * height)
        #

    # Função que coloca pixel por pixel da imagem
    def draw(self):
        largura_total = self.limite_superior - self.limite_inferior
        base_x = self.limite_inferior + self.offset_x
        base_y = self.limite_superior + self.offset_y
        size = self.img.height() # largura === altura

        # Atualiza o array compartilhado com os parâmetros atuais
        shared.calcArrayMandelbrot(self.arrayMandelbrot, base_x, base_y, size, largura_total)

        # Percore o array e coloca o valor em RGB na matriz de pixeis
        for x in range(size):
            for y in range(size):
                val = self.arrayMandelbrot[x * size + y]
                self.img.setPixel(x, y, qRgb(val, val, val))

        # Passa essa matriz para o elemento de display de imagem
        pixmap = QPixmap.fromImage(self.img)
        self.imageDisplay.setPixmap(pixmap)
        
    # Trata os comandos do teclado (calcula novo parâmetro e redesenha)
    def keyPressEvent(self, e):
        # Mover para cima
        if e.key() == Qt.Key_W:
            self.offset_y += self.limite_superior * 0.1
            self.draw()

        # Mover para esquerda
        elif e.key() == Qt.Key_A:
            self.offset_x -= self.limite_superior * 0.1
            self.draw()

        # Mover para baixo
        elif e.key() == Qt.Key_S:
            self.offset_y -= self.limite_superior * 0.1
            self.draw()

        # Mover para direita
        elif e.key() == Qt.Key_D:
            self.offset_x += self.limite_superior * 0.1
            self.draw()

        # Zoom-in
        elif e.key() == Qt.Key_Z:
            self.limite_inferior -= self.limite_inferior * 0.05
            self.limite_superior -= self.limite_superior * 0.05
            self.draw()

        # Zoom-out
        elif e.key() == Qt.Key_X:
            self.limite_inferior += self.limite_inferior * 0.05
            self.limite_superior += self.limite_superior * 0.05
            self.draw()

        # Zoom-in grande
        elif e.key() == Qt.Key_C:
            self.limite_inferior -= self.limite_inferior * 0.8
            self.limite_superior -= self.limite_superior * 0.8
            self.draw()

        # Zoom-out grande
        elif e.key() == Qt.Key_V:
            self.limite_inferior += self.limite_inferior * 0.8
            self.limite_superior += self.limite_superior * 0.8
            self.draw()

        # Reset
        elif e.key() == Qt.Key_R:
            self.offset_x, self.offset_y = 0, 0
            self.limite_superior, self.limite_inferior = 2, -2
            self.draw()

    # Ao fechar a janela, desalocar array compartilhado
    def closeEvent(self, event):
        shared.release(self.arrayMandelbrot)
        event.accept()

# Criação da tela
def main():
    app = QApplication(sys.argv)
    win = TelaPrincipal()
    win.draw()
    win.show()
    sys.exit(app.exec_())

main()