#ifndef SHARED_HPP__
#define SHARED_HPP__

extern "C" {
    //Windows
    //__declspec(dllexport) int soma(int a, int b);
    // Mac
    // int soma(int a, int b);
    // Linux
    // extern int soma(int a, int b);
    __declspec(dllexport) int findMandelbrot (double cr, double ci, int max_iterations);
}

#endif