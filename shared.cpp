#include "shared.hpp"

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
}

