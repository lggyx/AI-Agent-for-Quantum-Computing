#pragma once

#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>

#include <supa.h>

namespace supa_bench {

enum class MemType {
    UMA,
    NUMA,
};

inline const char *to_string(MemType mem_type) {
    return mem_type == MemType::NUMA ? "numa" : "uma";
}

template <typename T>
inline void check_su(T result, const char *func, const char *file, int line) {
    if (result) {
        std::fprintf(stderr, "SUPA error at %s:%d \"%s\" %s(%d): %s\n",
                     file, line, func, suGetErrorName(result),
                     static_cast<unsigned>(result), suGetErrorString(result));
        std::exit(EXIT_FAILURE);
    }
}

#define SUPA_BENCH_CHECK(val) \
    ::supa_bench::check_su((val), #val, __FILE__, __LINE__)

inline suError_t alloc_device(void **ptr, size_t bytes, MemType mem_type) {
    const size_t alloc_bytes = std::max<size_t>(bytes, 1);
    if (mem_type == MemType::UMA) {
        return suMallocDevice(ptr, alloc_bytes);
    }

    size_t size_per_region_pitch = alloc_bytes;
    return suNumaMallocDevice(ptr, &size_per_region_pitch, 1, alloc_bytes,
                              suMemArchTypeNUMA);
}

template <typename T>
class DeviceBuffer {
public:
    DeviceBuffer() = default;
    DeviceBuffer(size_t count, MemType mem_type) { allocate(count, mem_type); }
    DeviceBuffer(const DeviceBuffer &) = delete;
    DeviceBuffer &operator=(const DeviceBuffer &) = delete;

    ~DeviceBuffer() { reset(); }

    void allocate(size_t count, MemType mem_type) {
        reset();
        count_ = count;
        mem_type_ = mem_type;
        SUPA_BENCH_CHECK(alloc_device(reinterpret_cast<void **>(&ptr_),
                                      count * sizeof(T), mem_type));
    }

    void reset() {
        if (ptr_ != nullptr) {
            SUPA_BENCH_CHECK(suFree(ptr_));
            ptr_ = nullptr;
            count_ = 0;
        }
    }

    T *get() { return ptr_; }
    const T *get() const { return ptr_; }
    size_t count() const { return count_; }
    MemType mem_type() const { return mem_type_; }

    void copy_from_host(const std::vector<T> &host) {
        if (!host.empty()) {
            SUPA_BENCH_CHECK(suMemcpy(ptr_, host.data(), host.size() * sizeof(T)));
        }
    }

    void copy_to_host(std::vector<T> &host) const {
        if (!host.empty()) {
            SUPA_BENCH_CHECK(suMemcpy(host.data(), ptr_, host.size() * sizeof(T)));
        }
    }

private:
    T *ptr_ = nullptr;
    size_t count_ = 0;
    MemType mem_type_ = MemType::UMA;
};

inline double elapsed_us(suEvent_t start, suEvent_t stop, int iters) {
    float elapsed_ms = 0.0f;
    SUPA_BENCH_CHECK(suEventElapsedTime(&elapsed_ms, start, stop));
    return static_cast<double>(elapsed_ms) * 1000.0 / std::max(1, iters);
}

inline std::string get_arg_value(int argc, char **argv,
                                 const std::string &flag,
                                 const std::string &fallback) {
    for (int i = 1; i + 1 < argc; ++i) {
        if (argv[i] == flag) {
            return argv[i + 1];
        }
    }
    return fallback;
}

}  // namespace supa_bench
