SUPA_BASE ?= /usr/local/birensupa/base/latest
BRCC_PATH ?= $(SUPA_BASE)/brcc
BRCC      ?= $(BRCC_PATH)/bin/brcc
SUPA_PATH ?= $(SUPA_BASE)/supa
SUPTI     ?= $(SUPA_BASE)/supti
BRUMD     ?= $(SUPA_BASE)/brumd/lib
SUPA_ARCH_VERSION ?= br100
SUPA_TENSOR ?= $(SUPA_PATH)/include

OPT ?= -O2
FLAGS := $(OPT) --supa-gpu-arch=$(SUPA_ARCH_VERSION) --supa-path=$(SUPA_PATH)
INCLUDES := -Ikernel -I$(BENCH_ROOT)/include -I$(SUPA_TENSOR)
CPPFLAGS := -x supa -fPIC $(FLAGS) -std=c++17 $(INCLUDES)
SUFLAGS := -fPIC $(FLAGS) $(INCLUDES)
LINKFLAGS := --supa-link $(FLAGS)

ifeq ($(BR_ACCURACY),1)
BR_ACC_ROOT := $(BENCH_ROOT)/third_party/br_accuracy
CPPFLAGS += -I$(BR_ACC_ROOT)/include
SUFLAGS += -I$(BR_ACC_ROOT)/include
BR_ACC_OBJS := build/br_accuracy/br_compare.o \
               build/br_accuracy/compare_norm.o \
               build/br_accuracy/special_op_threshold.o \
               build/br_accuracy/utils.o
endif

RUN_ENV := LD_LIBRARY_PATH=$(BRUMD):$(SUPA_PATH)/lib:$(SUPTI)/lib:$$LD_LIBRARY_PATH
BIN := build/test_$(OP).out
EXTRA_OBJS ?=
OBJS := build/kernel/$(OP).o build/kernel/test_$(OP).o $(EXTRA_OBJS) $(BR_ACC_OBJS)

build: $(BIN)

build/kernel:
	mkdir -p build/kernel

build/br_accuracy:
	mkdir -p build/br_accuracy

build/kernel/%.o: kernel/%.su | build/kernel
	$(BRCC) $(SUFLAGS) $< -c -o $@

build/kernel/%.o: kernel/%.cpp | build/kernel
	$(BRCC) $(CPPFLAGS) $< -c -o $@

build/br_accuracy/%.o: $(BR_ACC_ROOT)/src/%.cpp | build/br_accuracy
	$(BRCC) $(CPPFLAGS) $< -c -o $@

$(BIN): $(OBJS)
	$(BRCC) $(LINKFLAGS) $^ -o $@

run-accuracy: $(BIN)
	$(RUN_ENV) ./$(BIN) --mode accuracy

run-perf: $(BIN)
	$(RUN_ENV) ./$(BIN) --mode perf

run-anticheat: $(BIN)
	$(RUN_ENV) ./$(BIN) --mode anticheat

clean:
	rm -rf build logs perf_output

.PHONY: build run-accuracy run-perf run-anticheat clean
