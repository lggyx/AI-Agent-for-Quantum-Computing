#pragma once

#include <cstdio>
#include <cstring>

namespace supa_bench::anticheat {

inline bool buffers_differ(const void *a, const void *b, size_t nbytes) {
    if (nbytes == 0) {
        return false;
    }
    return std::memcmp(a, b, nbytes) != 0;
}

inline void emit_result(const char *task, bool ok, const char *reason) {
    std::printf(
        "{\"task\":\"%s\",\"mode\":\"anticheat\",\"anticheat_ok\":%s,"
        "\"reason\":\"%s\"}\n",
        task, ok ? "true" : "false", reason ? reason : "");
}

}  // namespace supa_bench::anticheat
