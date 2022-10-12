#include "shared.hpp"
#include <stdlib.h>

extern "C" {
  __declspec(dllexport) int findMandelbrot (double cr, double ci, int max_iterations) {
    int i = max_iterations;
    double zr = 0.0, zi = 0.0;

    do {
        double temp = zr * zr - zi * zi + cr;
        zi = 2.0 * zr * zi + ci;
        zr = temp;
    } while (--i && zr * zr + zi * zi < 4.0);

    return max_iterations - i;
  }

  __declspec(dllexport) void testeArray(int** input, int size) {
    int* p = (int*) malloc(size * sizeof(int));
    for(int i = 0; i < size; ++i) {
      p[i] = i;
    }

    *input = p;
  }

  __declspec(dllexport) void release(int* input) {
    free(input);
  }

}


