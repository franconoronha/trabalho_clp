// adiciona a diretiva de exportação ao arquivo objeto no windows
#if defined(_WIN32)
#  define DLL_EXPORT __declspec(dllexport)
#else
#  define DLL_EXPORT
#endif

#include "shared.hpp"
#include <stdlib.h>
#include <cmath>

// desabilita o name mangling do C++ dentro do bloco
extern "C" {
  // Função para alocar um array compartilhado em memória
  DLL_EXPORT void createArray(int** input, int size) {
    int* p = (int*) malloc (size * sizeof(int));
   *input = p;
  }

  // Função para desalocar um array compartilhado em memória
  DLL_EXPORT void release(int* input) {
    free(input);
  }

  // Calcula o valor de cada pixel do array com base no tamanho do plano cartesiano dos números complexos
  DLL_EXPORT void calcArrayMandelbrot(int* input, double base_x, double base_y, int size, double largura_total) {
    double step_size = largura_total / size; // Tamanho do intervalo que o pixel representa
    double ponto_x, ponto_y, zr, zi, temp;

    int index, count;

    for(int i = 0; i < size; ++i) {
      for(int j = 0; j < size; ++j) {
        index = i * size + j;
        // Definição do ponto no plano cartesiano
        ponto_x = base_x + i * step_size;
        ponto_y = base_y - j * step_size;

        // Verificar em quantas iterações tende ao inifito
        // Max iterações = 100
        count = 0;
        zr = 0.0, zi = 0.0;

        do {
            temp = zr * zr - zi * zi + ponto_x;
            zi = 2.0 * zr * zi + ponto_y;
            zr = temp;
            ++count;
        } while (count < 100 && zr * zr + zi * zi < 4.0);

        input[index] = floor((count / 100.0) * 255); // transformado para faixa de 0 a 255
      }
    }
   }
}


