#if defined(_WIN32)
#  define DLL_EXPORT __declspec(dllexport)
#else
#  define DLL_EXPORT
#endif

#include "shared.hpp"
#include <stdlib.h>
#include <cmath>
#include <iostream>

extern "C" {
  DLL_EXPORT void createArray(int** input, int size) {
    int* p = (int*) malloc (size * sizeof(int));
   *input = p;
  }

  DLL_EXPORT void release(int* input) {
    free(input);
  }

  DLL_EXPORT void calcArrayMandelbrot(int* input, double base_x, double base_y, int size, double largura_total) {
    double step_size = largura_total / size;
    double ponto_x, ponto_y, zr, zi, temp;

    int index, count, result;

    for(int i = 0; i < size; ++i) {
      for(int j = 0; j < size; ++j) {
        index = i * size + j;
        ponto_x = base_x + i * step_size;
        ponto_y = base_y - j * step_size;

        count = 0;
        zr = 0.0, zi = 0.0;

        do {
            temp = zr * zr - zi * zi + ponto_x;
            zi = 2.0 * zr * zi + ponto_y;
            zr = temp;
            ++count;
        } while (count < 100 && zr * zr + zi * zi < 4.0);

        result = floor((count / 100.0) * 255);
        input[index] = result;
      }
    }
   }
}


