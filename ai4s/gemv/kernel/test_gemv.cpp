#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <random>
#include <string>
#include <vector>

#include "gemv.h"
#include "golden_gemv.h"
#include "supa_bench_common.h"

namespace {

struct CaseDef {
    const char *name;
    int M;
    int K;
    unsigned seed;
};

void init_fp32(float *buf, size_t count, float lo, float hi, unsigned seed) {
    std::mt19937 rng(seed);
    std::uniform_real_distribution<float> dist(lo, hi);
    for (size_t i = 0; i < count; ++i) {
        buf[i] = dist(rng);
    }
}

bool compare_fp32(const std::vector<float> &expected, const std::vector<float> &actual,
                  const char *case_name) {
    float max_abs = 0.0f;
    float max_rel = 0.0f;
    size_t max_idx = 0;
    for (size_t i = 0; i < expected.size(); ++i) {
        const float diff = std::fabs(expected[i] - actual[i]);
        const float denom = std::max(1.0f, std::fabs(expected[i]));
        const float rel = diff / denom;
        if (diff > max_abs) {
            max_abs = diff;
            max_rel = rel;
            max_idx = i;
        }
    }
    const bool ok = max_abs <= 1.0e-3f || max_rel <= 1.0e-4f;
    if (!ok) {
        std::fprintf(stderr,
                     "%s mismatch at %zu: expected=%g actual=%g max_abs=%g max_rel=%g\n",
                     case_name, max_idx, expected[max_idx], actual[max_idx], max_abs,
                     max_rel);
    }
    return ok;
}

bool run_case(const CaseDef &cfg, bool emit_case_json) {
    const int M = cfg.M;
    const int K = cfg.K;
    const size_t a_sz = static_cast<size_t>(M) * K;
    const size_t x_sz = static_cast<size_t>(K);
    const size_t y_sz = static_cast<size_t>(M);

    std::vector<float> h_A(a_sz);
    std::vector<float> h_x(x_sz);
    std::vector<float> h_golden(y_sz);
    std::vector<float> h_actual(y_sz, 0.0f);

    init_fp32(h_A.data(), a_sz, -0.5f, 0.5f, cfg.seed);
    init_fp32(h_x.data(), x_sz, -0.5f, 0.5f, cfg.seed + 1);
    golden_gemv::gemv_colmajor(h_A.data(), h_x.data(), h_golden.data(), M, K, M);

    supa_bench::DeviceBuffer<float> d_A(a_sz, supa_bench::MemType::UMA);
    supa_bench::DeviceBuffer<float> d_x(x_sz, supa_bench::MemType::UMA);
    supa_bench::DeviceBuffer<float> d_y(y_sz, supa_bench::MemType::UMA);
    d_A.copy_from_host(h_A);
    d_x.copy_from_host(h_x);

    suError_t status = launch_gemv_colmajor(d_A.get(), d_x.get(), d_y.get(), M, K, nullptr);
    if (status == suSuccess) {
        status = suDeviceSynchronize();
    }
    if (status == suSuccess) {
        d_y.copy_to_host(h_actual);
    }

    const bool pass = status == suSuccess && compare_fp32(h_golden, h_actual, cfg.name);
    if (emit_case_json) {
        std::printf("{\"case\":\"%s\",\"storage\":\"uma\",\"passed\":%s}\n",
                    cfg.name, pass ? "true" : "false");
    }
    if (!pass && status != suSuccess) {
        std::fprintf(stderr, "launch failed: %s\n", suGetErrorString(status));
    }
    return pass;
}

const CaseDef kAccuracyCases[] = {
    {"small_64x64", 64, 64, 100u},
    {"wide_257x1024", 257, 1024, 200u},
    {"large_4096x512", 4096, 512, 300u},
};

const CaseDef kPerfCase = {"perf_4096x1024", 4096, 1024, 400u};

double run_perf(const CaseDef &cfg) {
    const int M = cfg.M;
    const int K = cfg.K;
    const size_t a_sz = static_cast<size_t>(M) * K;
    const size_t x_sz = static_cast<size_t>(K);
    const size_t y_sz = static_cast<size_t>(M);

    std::vector<float> h_A(a_sz);
    std::vector<float> h_x(x_sz);
    init_fp32(h_A.data(), a_sz, -0.5f, 0.5f, cfg.seed);
    init_fp32(h_x.data(), x_sz, -0.5f, 0.5f, cfg.seed + 1);

    supa_bench::DeviceBuffer<float> d_A(a_sz, supa_bench::MemType::UMA);
    supa_bench::DeviceBuffer<float> d_x(x_sz, supa_bench::MemType::UMA);
    supa_bench::DeviceBuffer<float> d_y(y_sz, supa_bench::MemType::UMA);
    d_A.copy_from_host(h_A);
    d_x.copy_from_host(h_x);

    constexpr int warmup = 3;
    constexpr int iters = 20;
    for (int i = 0; i < warmup; ++i) {
        SUPA_BENCH_CHECK(launch_gemv_colmajor(d_A.get(), d_x.get(), d_y.get(), M, K, nullptr));
    }
    SUPA_BENCH_CHECK(suDeviceSynchronize());

    suEvent_t start{};
    suEvent_t stop{};
    SUPA_BENCH_CHECK(suEventCreate(&start));
    SUPA_BENCH_CHECK(suEventCreate(&stop));
    SUPA_BENCH_CHECK(suEventRecord(start, nullptr));
    for (int i = 0; i < iters; ++i) {
        SUPA_BENCH_CHECK(launch_gemv_colmajor(d_A.get(), d_x.get(), d_y.get(), M, K, nullptr));
    }
    SUPA_BENCH_CHECK(suEventRecord(stop, nullptr));
    SUPA_BENCH_CHECK(suEventSynchronize(stop));
    const double us = supa_bench::elapsed_us(start, stop, iters);
    SUPA_BENCH_CHECK(suEventDestroy(start));
    SUPA_BENCH_CHECK(suEventDestroy(stop));
    return us;
}

}  // namespace

int main(int argc, char **argv) {
    const std::string mode = supa_bench::get_arg_value(argc, argv, "--mode", "accuracy");
    if (mode == "perf") {
        const double us = run_perf(kPerfCase);
        std::printf("{\"task\":\"gemv\",\"mode\":\"perf\",\"case\":\"%s\","
                    "\"generated_us\":%.6f}\n",
                    kPerfCase.name, us);
        return 0;
    }

    int passed = 0;
    std::printf("{\"task\":\"gemv\",\"mode\":\"case_log_begin\"}\n");
    for (const auto &cfg : kAccuracyCases) {
        if (run_case(cfg, true)) {
            ++passed;
        }
    }
    const int total = static_cast<int>(sizeof(kAccuracyCases) / sizeof(kAccuracyCases[0]));
    std::printf("{\"task\":\"gemv\",\"mode\":\"accuracy\",\"passed_cases\":%d,"
                "\"total_cases\":%d,\"accuracy_ok\":%s}\n",
                passed, total, passed == total ? "true" : "false");
    return passed == total ? 0 : 1;
}
