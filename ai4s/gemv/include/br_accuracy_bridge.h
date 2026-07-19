#pragma once

#include <cstdint>
#include <vector>

#include <supa.h>
#include "br_compare.h"

namespace supa_bench {

inline bool compare_bf16_accumulative(const std::vector<BF16> &golden,
                                    const std::vector<BF16> &actual,
                                    const char *op_name) {
    accuracy::compare::ErrReporter reporter{};
    reporter.op_type = "ACCUMULATIVE";
    reporter.op_name = op_name;
    reporter.dtype = accuracy::compare::DataType::BF16;
    reporter.total_cnt = static_cast<int>(golden.size());
    reporter.enable_cosine_similarity = true;
    reporter.mismatched_element_print_threshold = 8;
    return accuracy::compare::CompareResult_v2(golden.data(), actual.data(),
                                               reporter);
}

inline bool compare_fp32_accumulative(const std::vector<float> &golden,
                                      const std::vector<float> &actual,
                                      const char *op_name) {
    accuracy::compare::ErrReporter reporter{};
    reporter.op_type = "ACCUMULATIVE";
    reporter.op_name = op_name;
    reporter.dtype = accuracy::compare::DataType::FP32;
    reporter.total_cnt = static_cast<int>(golden.size());
    reporter.enable_cosine_similarity = true;
    reporter.mismatched_element_print_threshold = 8;
    return accuracy::compare::CompareResult_v2(golden.data(), actual.data(),
                                               reporter);
}

}  // namespace supa_bench
