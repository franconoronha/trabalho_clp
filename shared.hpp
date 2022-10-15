#ifdef _WIN32
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT
#endif

#ifndef SHARED_HPP__
#define SHARED_HPP__

extern "C" {
    DLL_EXPORT void createArray(int** input, int size);
    DLL_EXPORT void release(int* input);
    DLL_EXPORT void calcArrayMandelbrot(int* input, double base_x, double base_y, int size, double largura_total);
}

#endif