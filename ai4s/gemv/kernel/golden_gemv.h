#pragma once

namespace golden_gemv {

inline void gemv_colmajor(const float *A, const float *x, float *y, int M, int K,
                          int lda) {
    for (int m = 0; m < M; ++m) {
        float acc = 0.0f;
        for (int k = 0; k < K; ++k) {
            acc += A[m + k * lda] * x[k];
        }
        y[m] = acc;
    }
}

}  // namespace golden_gemv
