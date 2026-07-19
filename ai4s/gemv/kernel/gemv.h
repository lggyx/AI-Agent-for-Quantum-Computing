#pragma once

#include <supa.h>

// G-mode SGEMV: y[M] = A[M,K] * x[K], column-major storage.
// A[m,k] is A[m + k * lda], with lda = M. alpha=1, beta=0.
extern "C" suError_t launch_gemv_colmajor(const float *d_A, const float *d_x,
                                           float *d_y, int M, int K,
                                           suStream_t stream);
