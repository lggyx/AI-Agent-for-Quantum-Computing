#pragma once

#include <cstdint>
#include <vector>

#include <supa.h>
#include <supa_tensor.h>

#include "supa_bench_common.h"

namespace supa_bench {
namespace tensor_util {

using namespace tensor;

inline uint32_t ceil_div_u32(uint32_t a, uint32_t b) { return (a + b - 1) / b; }

inline uint32_t find_gran(uint32_t x) {
    constexpr uint32_t kMatrixHwLimit = 8192;
    constexpr uint32_t kMatrixColGran = 256;
    if (x <= kMatrixHwLimit) {
        return x;
    }
    for (uint32_t i = kMatrixHwLimit; i >= kMatrixColGran; i /= 2) {
        if (x % i == 0) {
            return i;
        }
    }
    uint32_t prev_i = kMatrixHwLimit;
    for (uint32_t i = kMatrixHwLimit / 2; i >= kMatrixColGran; i /= 2) {
        const uint32_t need_zero = i - x % i;
        if (need_zero >= prev_i - x % prev_i) {
            return prev_i;
        }
        prev_i = i;
    }
    return kMatrixColGran;
}

inline void get_splited_hw(uint32_t H, uint32_t W, uint32_t &splited_h, uint32_t &splited_w) {
    constexpr uint32_t kMatrixHwLimit = 8192;
    splited_h = H > kMatrixHwLimit ? find_gran(H) : H;
    splited_w = W > kMatrixHwLimit ? find_gran(W) : W;
}

inline void matrix3d_fold_params(int N, int H, int W, uint32_t &nplanes_folded,
                               uint32_t &height_folded, uint32_t &width_folded) {
    get_splited_hw(static_cast<uint32_t>(H), static_cast<uint32_t>(W), height_folded,
                   width_folded);
    const uint32_t n_folded_from_h = ceil_div_u32(static_cast<uint32_t>(H), height_folded);
    const uint32_t n_folded_from_w = ceil_div_u32(static_cast<uint32_t>(W), width_folded);
    nplanes_folded = static_cast<uint32_t>(N) * n_folded_from_h * n_folded_from_w;
}

template <typename E, MatrixLayout Layout = BLOCK_COL_MAJOR>
inline UmaDynMatrix3D<E, Layout> make_matrix3d_from_plain(const E *host_plain, int N,
                                                          int H, int W) {
    uint32_t nplanes_folded = 0;
    uint32_t height_folded = 0;
    uint32_t width_folded = 0;
    matrix3d_fold_params(N, H, W, nplanes_folded, height_folded, width_folded);
    UmaDynMatrix3D<E, Layout> tensor(static_cast<int>(nplanes_folded),
                                      static_cast<int>(height_folded),
                                      static_cast<int>(width_folded), 1);
    tensor.copyFromRawData(suDenseRowMajor, const_cast<E *>(host_plain));
    tensor.moveToDevice();
    return tensor;
}

template <typename E>
inline UmaDynVectors<E> make_vectors_from_plain(const E *host_plain, int len) {
    uint32_t splited_w = static_cast<uint32_t>(len);
    get_splited_hw(1, static_cast<uint32_t>(len), splited_w, splited_w);
    const uint32_t n_folded = ceil_div_u32(static_cast<uint32_t>(len), splited_w);
    UmaDynVectors<E> vec(static_cast<int>(n_folded), static_cast<int>(splited_w), 1);
    vec.copyFromRawData(suDenseRowMajor, const_cast<E *>(host_plain));
    vec.moveToDevice();
    return vec;
}

template <typename E, MatrixLayout Layout = BLOCK_COL_MAJOR>
inline void matrix3d_to_plain(const UmaDynMatrix3D<E, Layout> &tensor, E *host_plain, int N,
                              int H, int W) {
    UmaDynMatrix3D<E, Layout> host_copy = tensor;
    host_copy.moveToHost();
    host_copy.copyToRawData(suDenseRowMajor, host_plain);
    (void)N;
    (void)H;
    (void)W;
}

template <typename E>
inline void vectors_to_plain(const UmaDynVectors<E> &vec, E *host_plain, int len) {
    UmaDynVectors<E> host_copy = vec;
    host_copy.moveToHost();
    host_copy.copyToRawData(suDenseRowMajor, host_plain);
    (void)len;
}

}  // namespace tensor_util
}  // namespace supa_bench
