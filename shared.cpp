#include "shared.hpp"

extern "C" {
  __declspec(dllexport) int soma(int a, int b) {
    return a + b;
  }
}

