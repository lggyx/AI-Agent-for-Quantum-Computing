#include <limits>

#include <torch/extension.h>
#include <supa.h>

extern "C" suError_t launch_gemv(const float *d_A, const float *d_x,
                                  float *d_y, int M, int K,
                                  suStream_t stream);

static void check_status(suError_t status, const char *what) {
    TORCH_CHECK(status == suSuccess, what, " failed with SUPA status ",
                static_cast<int>(status));
}

torch::Tensor gemv(torch::Tensor A, torch::Tensor x) {
    TORCH_CHECK(A.dim() == 2, "A must have shape [M,K]");
    TORCH_CHECK(x.dim() == 1, "x must have shape [K]");
    TORCH_CHECK(A.dtype() == torch::kFloat32, "A must be float32");
    TORCH_CHECK(x.dtype() == torch::kFloat32, "x must be float32");
    TORCH_CHECK(A.is_contiguous(), "A must be contiguous");
    TORCH_CHECK(x.is_contiguous(), "x must be contiguous");
    TORCH_CHECK(A.device() == x.device(), "A and x must be on the same device");

    const int64_t M64 = A.size(0);
    const int64_t K64 = A.size(1);
    TORCH_CHECK(M64 > 0 && K64 > 0, "M and K must be positive");
    TORCH_CHECK(x.size(0) == K64, "x length must match A.size(1)");
    TORCH_CHECK(M64 <= static_cast<int64_t>(std::numeric_limits<int>::max()), "M is too large");
    TORCH_CHECK(K64 <= static_cast<int64_t>(std::numeric_limits<int>::max()), "K is too large");

    auto y = torch::empty({M64}, A.options());
    check_status(launch_gemv(
                     static_cast<const float *>(A.data_ptr()),
                     static_cast<const float *>(x.data_ptr()),
                     static_cast<float *>(y.data_ptr()),
                     static_cast<int>(M64), static_cast<int>(K64), nullptr),
                 "launch_gemv");
    return y;
}

PYBIND11_MODULE(gemv_supa_ext, m) {
    m.def("gemv", &gemv,
          "GEMV implemented by a SUPA kernel");
}
