# 壁仞™ suRAND 用户指南

## suRAND 简介

suRAND是基于BIRENSUPA™开发的软件库，提供了高性能伪随机数及拟随机数生成器。本文档是对该库的API的一个完整说明，下文中我们称之为suRAND API。

suRAND是适配壁仞通用 GPU 的一款软件工具，能够充分利用 GPU 的并行计算的能力。基于业界通用的随机数生成算法XORWOW，Philox4x32-10等，suRAND提供了一系列用于生成特定分布的随机数序列的接口。特别地，suRAND除了提供常见的主机端接口（HOST API），还提供了设备端接口（Device API）。通过Device API，您可以在 GPU上便捷地生成数据，并直接在同一 GPU 进程中应用这些数据。这种模式可以提升GPU程序的运行性能。

类似于其他基于BIRENSUPA开发的软件库API，使用HOST API时，您可以通过包含头文件/include/surand.h获取函数声明，并连接到suRAND函数库，然后在主机端（CPU）调用。您可以调用 HOST API在主机端或设备端（GPU）生成随机数。通过设备端生成的随机数，将存储在设备端全局内存（global memory）中，您可以在内核函数中直接使用这些随机数，或将数据拷贝回主机端后使用。

Device API通过头文件/include/surand_kernel.h提供，形式均为设备端函数。在用户编写的内核函数内部，可以通过调用Device API生成随机数，达到在设备端生成随机数的目的。生成的随机数可以立即当前的内核函数使用，而不需要将随机数写入设备端全局内存，然后再从设备端全局内存中读取。

<div style="page-break-after:always"></div>

## suRAND 主机端（CPU）API

### 通用描述

用户要使用Host API，则需要在文件中包含 `/include/surand.h`，并动态链接到suRAND和SUPA库。

使用suRAND Host API生成随机数的一般步骤如下：

1. 创建一个随机数生成器：`surandCreateGenerator()`
2. 设置生成器选项
3. 分配设备内存：`suMalloc()`
4. 生成随机数：`surandGenerate()`
5. 使用随机数
6. 释放随机数生成器：`surandDestroyGenerator()`

如果要在主机CPU上生成随机数，在上述第一步时需要使用 `surandCreateGeneratorHost()`，并且在第三步使用主机内存来存储结果。

另外，suRAND允许用户同时创建多个生成器，它们之间相互独立，每个生成器封装了一个单独的状态，其生成的随机数序列是确定的，只要给定相同的设置参数，无论是在Host生成还是device生成，程序每次运行的结果都会产生相同的序列。

### 生成器算法类型

用户可以通过surandRngType_t指定随机数生成器算法类型。suRAND支持拟随机数和伪随机数生成，默认算法为生成伪随机数的xorwow算法。当前版本还支持生成伪随机数的philox4x32-10算法和mtgp32算法。

### 生成器可配置参数

#### 随机数种子（seed）

随机数种子seed是六十四位整型数据，用于配置随机数生成器的初始状态。相同的seed总是产生相同的随机数序列。

#### 偏移（offset）

偏移（offset）参数用于在结果序列中跳转取值。如果 offset=50，则第一个输出的随机数将是随机数序列中的第50个数值。

#### 排布（ordering）

排布（ordering）参数用于选择结果在内存中的排布方式。该参数对生成随机数的性能有直接影响。

### 返回值

suRAND 设备端API的返回值均为 `surandStatus_t`。如果API运行成功，则返回状态 `SURAND_STATUS_SUCCESS`。如果API运行不成功，您可以查看[surandStatus_t类型的返回值](#surandstatus_t)了解具体错误信息。

### 通用函数
#### 查询当前版本序号
```cpp
surandStatus_t SURANDAPI surandGetVersion(int *version);
```
查询当前suRAND库的版本号。
### 生成器相关函数

#### 创建生成器

```cpp
surandStatus_t SURANDAPI surandCreateGenerator(surandGenerator_t *generator,
                                               surandRngType_t rng_type);

surandStatus_t SURANDAPI surandCreateGeneratorHost(surandGenerator_t *generator,
                                                   surandRngType_t rng_type);
```

根据生成器算法类型创建对应的随机数生成器。`surandCreateGenerator` 创建的生成器将会使用设备端生成随机数。而 `surandCreateGeneratorHost` 创建的生成器将会使用主机端生成随机数。

#### 销毁生成器

```cpp
surandStatus_t surandDestroyGenerator(surandGenerator_t generator);
```

销毁指定的随机数生成器。

#### 配置SUPA流

```cpp
surandStatus_t SURANDAPI surandSetStream(surandGenerator_t generator,
                                         suStream_t stream);
```

为随机数生成器配置SUPA流，配置了同一SUPA流的函数只能串式运行。

#### 为伪随机数生成器配置随机数种子

```cpp
surandStatus_t SURANDAPI surandSetPseudoRandomGeneratorSeed(
    surandGenerator_t generator, unsigned long long seed);
```

配置随机数种子。

#### 为随机数生成器配置偏移

```cpp
surandStatus_t SURANDAPI surandSetGeneratorOffset(surandGenerator_t generator,
                                                  unsigned long long offset);
```

配置随机数输出在随机数序列中的偏移。

#### 为随机数生成器配置排布类型

```cpp
surandStatus_t SURANDAPI surandSetGeneratorOrdering(surandGenerator_t generator,
                                                    surandOrdering_t order);
```

配置生成的随机数序列在内存中的排布形式。

#### 生成无符号整型随机数序列

```cpp
surandStatus_t SURANDAPI surandGenerate(surandGenerator_t generator,
                                        unsigned int *outputPtr, size_t num);
```

获取由输入随机数生成器生成的无符号整型随机数序列。序列长度由`num`指定。

#### 生成符合[0.0, 1.0] 均匀分布的浮点随机数序列

```cpp
surandStatus_t SURANDAPI surandGenerateUniform(surandGenerator_t generator,
                                               float *outputPtr, size_t num);
```

获取由输入随机数生成器生成的符合[0.0, 1.0] 均匀分布浮点随机数序列。序列长度由`num`指定。

#### 生成符合正态分布的浮点随机数序列

```cpp
surandStatus_t SURANDAPI surandGenerateNormal(surandGenerator_t generator,
                                              float *outputPtr, size_t n,
                                              float mean, float stddev);
```

获取由输入随机数生成器生成的符合均值为`mean`，方差为`stddev`的正态分布浮点随机数序列。序列长度由`num`指定。

#### 生成符合对数正态分布的浮点随机数序列

```cpp
surandStatus_t SURANDAPI surandGenerateLogNormal(surandGenerator_t generator,
                                                 float *outputPtr, size_t n,
                                                 float mean, float stddev);
```

获取由输入随机数生成器生成的符合对数均值为`mean`，对数方差为`stddev`的对数正态分布浮点随机数序列。序列长度由`num`指定。
#### 生成符合泊松分布的无符号整型随机数序列
```cpp
surandStatus_t SURANDAPI surandGeneratePoisson(surandGenerator_t generator,
                                               unsigned int *outputPtr,
                                               size_t n, float lambda);
```
获取由输入随机数生成器生成的符合泊松分布的无符号整型随机数序列。序列长度由`num`指定。该泊松分布的参数$\lambda$由输入参数`lambda`决定。
#### 生成符合二项分布的无符号整型随机数序列
```cpp
surandStatus_t SURANDAPI surandGenerateBinomial(surandGenerator_t generator,
                                                unsigned int *outputPtr,
                                                size_t num, unsigned int n,
                                                float p);
```
获取由输入随机数生成器生成的符合二项分布的无符号整型随机数序列。序列长度由`num`指定。该二项分布的参数$n$和$p$由输入参数`n`和`p`决定。
### 枚举值说明

#### surandStatus_t

| **值**                                  | **含义**                                                                                                       |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| SURAND_STATUS_SUCCESS                   | 运行成功。                                                                                                     |
| SURAND_STATUS_VERSION_MISMATCH          | 头文件与链接的软件库版本不匹配。                                                                               |
| SURAND_STATUS_NOT_INITIALIZED           | API传入的随机数生成器未初始化。一般是由于surandCreateGenerator或surandCreateGeneratorHost未先于该API进行调用。 |
| SURAND_STATUS_ALLOCATION_FAILED         | 资源分配失败。                                                                                                 |
| SURAND_STATUS_TYPE_ERROR                | 传入的随机数生成器算法类型和调用的API不匹配。                                                                  |
| SURAND_STATUS_OUT_OF_RANGE              | 超出范围。                                                                                                     |
| SURAND_STATUS_LENGTH_NOT_MULTIPLE       | 请求的长度不是对应维度的乘积。                                                                                 |
| SURAND_STATUS_DOUBLE_PRECISION_REQUIRED | 当前GPU不支持双精度。                                                                                          |
| SURAND_STATUS_LAUNCH_FAILURE            | suRAND内核运行失败。                                                                                           |
| SURAND_STATUS_PREEXISTING_FAILURE       | 在软件库入口已有错误。                                                                                         |
| SURAND_STATUS_INITIALIZATION_FAILED     | SUPA库初始化失败。                                                                                             |
| SURAND_STATUS_ARCH_MISMATCH             | 架构不匹配，设备端（GPU）不支持该功能。                                                                        |
| SURAND_STATUS_INTERNAL_ERROR            | suRAND内部执行错误                                                                                             |

#### surandRngType_t

| **值**                          | **含义**                  |
| ------------------------------- | ------------------------ |
| SURAND_RNG_TEST                 | 保留字符                  |
| SURAND_RNG_PSEUDO_DEFAULT       | 默认算法，采用xorwow      |
| SURAND_RNG_PSEUDO_XORWOW        | Xorwow伪随机数算法        |
| SURAND_RNG_PSEUDO_PHILOX4_32_10 | Philox4x32-10伪随机数算法 |
| SURAND_RNG_PSEUDO_MTGP32        | mtgp32伪随机数算法        |

#### surandOrdering_t

| **值**                         | **含义**                                                                       |
| ------------------------------ | ------------------------------------------------------------------------------ |
| SURAND_ORDERING_PSEUDO_BEST    | 最佳排布类型                                                                   |
| SURAND_ORDERING_PSEUDO_DEFAULT | 默认排布类型                                                                   |
| SURAND_ORDERING_PSEUDO_SEEDED  | Seeded排布类型，减少了生成器的状态设置时间，但可能会导致生成随机数的统计缺陷。 |
| SURAND_ORDERING_PSEUDO_LEGACY  | Legacy排布类型，所有版本的GPU使用该排布类型会生成同样的随机数序列。            |

不同生成器算法类型针对排布类型有不一样的做法。对于xorwow算法，排布类型和做法的对应关系为：

| **值**                         | **Xorwow采用的做法**                                                            |
| ------------------------------ | ------------------------------------------------------------------------------- |
| SURAND_ORDERING_PSEUDO_BEST    | 和SURAND_ORDERING_PSEUDO_LEGACY效果相同                                         |
| SURAND_ORDERING_PSEUDO_DEFAULT | 和SURAND_ORDERING_PSEUDO_LEGACY效果相同                                         |
| SURAND_ORDERING_PSEUDO_SEEDED  | offset n的结果来自于全局序列的(n mod 4096) 2^67 + floor(n/4096)的位置。         |
| SURAND_ORDERING_PSEUDO_LEGACY  | offset n的结果来自于全局序列的floor(n/4096)的位置，即每4096个线程使用不同的seed |

<div style="page-break-after:always"></div>

## suRAND设备端（GPU）API

### 通用描述

如果需要使用设备端API，请在定义使用suRAND设备函数的kernel文件中包含surand_kernel.h文件。Device API可以生成伪随机数和拟随机数。

### API介绍

#### 初始化

和主机端API不一样的是，设备端API使用状态对象以生产随机数序列。不同的随机数生成算法对应不一样的状态对象。

```cpp
__device__ __host__ void surand_init(unsigned long long seed,
unsigned long long subsequence,
unsigned long long offset, surandStateXORWOW_t *state);
```

初始化xorwow状态对象surandStateXORWOW_t。为其配置了随机数种子，初始跳转偏移。

```cpp
__device__ __host__ void surand_init(unsigned long long seed,
unsigned long long subsequence,
unsigned long long offset, surandStatePhilox4_32_10_t *state);
```

初始化Philox4x32-10状态对象 `surandStatePhilox4_32_10_t`。为其配置了随机数种子，初始跳转偏移。

```cpp
surandStatus_t surand_make_mtgp32_constants(
    const mtgp32_params_fast_t *params, mtgp32_kernel_params_t *kernel_param);
```
在主机端使用的帮助函数。使用存在于主机端内存的`mtgp32_params_fast_t`类型的数组初始化存在于设备端内存的`mtgp32_kernel_params_t`类型的数组。

```cpp
surandStatus_t surand_make_mtgp32_state(
    surandStateMtgp32_t *state, mtgp32_params_fast_t *params,
    mtgp32_kernel_params_t *kernel_params, int n, unsigned long long seed);
```

在主机端使用的帮助函数。使用存在于主机端内存的`mtgp32_params_fast_t`类型的数组和存在于设备端内存的`mtgp32_kernel_params_t`类型的数组，初始化存在于设备端内存的`surandStateMtgp32_t`类型的数组。state数组长度由`n`指定，初始化时使用随机种子`seed`。

#### 跳转偏移

```cpp
__device__ __host__ void skipahead (unsigned long long n,
surandStateXORWOW_t *state);
```

为xorwow状态对象 `surandStateXORWOW_t` 配置了跳转偏移，使得输出序列将从随机数序列的第n位开始。

```cpp
__device__ __host__ void skipahead (unsigned long long n,
surandStatePhilox4_32_10_t *state);
```

为Philox4x32-10状态对象 `surandStatePhilox4_32_10_t` 配置了跳转偏移，使得输出序列将从随机数序列的第n位开始。

#### 跳转偏移子序列

```cpp
__device__ __host__ void skipahead_sequence (unsigned long long n,
surandStateXORWOW_t *state);
```

为xorwow状态对象 `surandStateXORWOW_t` 配置了跳转偏移n个子序列，使得输出序列将从随机数序列的第n*sequence_length位开始。

```cpp
__device__ __host__ void skipahead_sequence (unsigned long long n,
surandStatePhilox4_32_10_t *state);
```

为Philox4x32-10状态对象 `surandStatePhilox4_32_10_t` 配置了跳转偏移n个子序列，使得输出序列将从随机数序列的第n*sequence_length位开始。

#### 生成无符号整型随机数
##### surand
```cpp
__device__ __host__ int surand (surandStateXORWOW_t *state);
```

使用xorwow状态对象 `surandStateXORWOW_t` 生成了一个无符号随机数。

```cpp
__device__ __host__ int surand (surandStatePhilox4_32_10_t *state);
```

使用Philox4x32-10状态对象 `surandStatePhilox4_32_10_t` 生成了一个无符号随机数。

##### surand4
```cpp
__device__ __host__  uint4 surand4 (surandStatePhilox4_32_10_t *state);
```

使用Philox4x32-10状态对象 `surandStatePhilox4_32_10_t` 生成了四个无符号随机数。通过使用Philox4x32-10的算法，使用`surand4`的执行效率比使用`surand`更高。

#### 生成均匀分布浮点随机数
##### surand_uniform
```cpp
__device__ __host__  float surand_uniform (surandStateXORWOW_t *state);
```
使用xorwow状态对象 `surandStateXORWOW_t` 生成了符合在区间[0.0, 1.0]均匀分布的一个浮点随机数。

```cpp
__device__ __host__  float surand_uniform (surandStatePhilox4_32_10_t *state);
```

使用Philox4x32-10状态对象 `surandStatePhilox4_32_10_t` 生成了符合在区间[0.0, 1.0]均匀分布的一个浮点随机数。

```cpp
__device__ float surand_uniform(surandStateMtgp32_t *state);
```
使用mtgp32状态对象 `surandStateMtgp32_t` 生成了符合在区间[0.0, 1.0]均匀分布的一个浮点随机数。

##### surand_uniform4
```cpp
__device__ __host__  float4 surand_uniform4 (surandStatePhilox4_32_10_t *state);
```

使用Philox4x32-10状态对象 `surandStatePhilox4_32_10_t` 生成了符合在区间[0.0, 1.0]均匀分布的四个浮点随机数。通过使用Philox4x32-10的算法，使用`surand_uniform4`的执行效率比使用`surand_uniform`更高。

#### 生成正态分布浮点随机数
##### surand_normal
```cpp
__device__ __host__  float surand_normal (surandStateXORWOW_t *state);
```
使用xorwow状态对象 `surandStateXORWOW_t` 生成了符合均值为0，方差为1的正态分布的一个浮点随机数。

```cpp
__device__ __host__  float surand_normal (surandStatePhilox4_32_10_t *state);
```
使用Philox4x32-10状态对象 `surandStatePhilox4_32_10_t` 生成了符合均值为0，方差为1的正态分布的一个浮点随机数。

```cpp
__device__ float surand_normal(surandStateMtgp32_t *state)
```
使用mtgp32状态对象 `surandStateMtgp32_t` 生成了符合均值为0，方差为1的正态分布的一个浮点随机数。

##### surand_normal2
```cpp
__device__ __host__  float2 surand_normal2 (surandStateXORWOW_t *state);
```
使用xorwow状态对象 `surandStateXORWOW_t` 生成了符合均值为0，方差为1的正态分布的两个浮点随机数。用于生成正态分布随机数的Box-Muller算法使得`surand_normal2`比`surand_normal`的执行效率更高。

```cpp
__device__ __host__  float2 surand_normal2 (surandStatePhilox4_32_10_t *state);
```
使用Philox4x32-10状态对象 `surandStatePhilox4_32_10_t` 生成了符合均值为0，方差为1的正态分布的两个浮点随机数。用于生成正态分布随机数的Box-Muller算法使得`surand_normal2`比`surand_normal`的执行效率更高。
##### surand_normal4
```cpp
__device__ __host__  float4 surand_normal4 (surandStatePhilox4_32_10_t *state);
```
使用Philox4x32-10状态对象 `surandStatePhilox4_32_10_t` 生成了符合均值为0，方差为1的正态分布的四个浮点随机数。通过使用Philox4x32-10的算法，使用`surand_normal4`的执行效率比使用`surand_normal`及`surand_normal2`更高。

#### 生成对数正态分布浮点随机数
##### surand_log_normal
```cpp
__device__ __host__ float surand_log_normal(surandStateXORWOW_t *state,
                                            float mean, float stddev);
```
使用xorwow状态对象 `surandStateXORWOW_t` 生成了对数正态分布的一个浮点随机数。对数正态分布的对数均值为输入参数`mean`, 对数方差为输入`stddev`。
```cpp
__device__ __host__ float surand_log_normal(surandStatePhilox4_32_10_t *state,
                                    float mean, float stddev);
```
使用Philox4x32-10状态对象 `surandStatePhilox4_32_10_t` 生成了对数正态分布的一个浮点随机数。对数正态分布的对数均值为输入参数`mean`, 对数方差为输入`stddev`。
```cpp
__device__ __host__ float surand_log_normal(surandStateMtgp32_t *state, float mean,
                                    float stddev)
```
使用mtgp32状态对象 `surandStateMtgp32_t` 生成了对数正态分布的一个浮点随机数。对数正态分布的对数均值为输入参数`mean`, 对数方差为输入`stddev`。
##### surand_log_normal2
```cpp
__device__ __host__ float2 surand_log_normal2(surandStateXORWOW_t *state, float mean,
                                      float stddev)
```
使用xorwow状态对象 `surandStateXORWOW_t` 生成了对数正态分布的两个浮点随机数。对数正态分布的对数均值为输入参数`mean`, 对数方差为输入`stddev`。用于生成对数正态分布随机数的Box-Muller算法使得`surand_log_normal2`比`surand_log_normal`的执行效率更高。
```cpp
__device__ __host__float2 surand_log_normal2(surandStatePhilox4_32_10_t *state,
                                      float mean, float stddev)
```
使用Philox4x32-10状态对象 `surandStatePhilox4_32_10_t` 生成了对数正态分布的两个浮点随机数。对数正态分布的对数均值为输入参数`mean`, 对数方差为输入`stddev`。用于生成对数正态分布随机数的Box-Muller算法使得`surand_log_normal2`比`surand_log_normal`的执行效率更高。
##### surand_log_normal4
```cpp
__device__ __host__float4 surand_log_normal4(surandStatePhilox4_32_10_t *state,
                                      float mean, float stddev);
```
使用Philox4x32-10状态对象 `surandStatePhilox4_32_10_t` 生成了对数正态分布的四个浮点随机数。对数正态分布的对数均值为输入参数`mean`, 对数方差为输入`stddev`。通过使用Philox4x32-10的算法，使用`surand_log_normal4`的执行效率比使用`surand_log_normal`及`surand_log_normal2`更高。

#### 生成泊松分布无符号整型随机数

##### surand_poisson

```cpp
__device__ __host__ unsigned int surand_poisson (surandStateXORWOW_t *state, 
                                          float lambda);
```
使用xorwow状态对象 `surandStateXORWOW_t` 生成了符合泊松分布的一个无符号整型随机数。该泊松分布的$\lambda$参数由函数输入决定。

```cpp
__device__ __host__ unsigned int surand_poisson (surandStatePhilox4_32_10_t *state,
                                 float lambda);
```

使用Philox4x32-10状态对象 `surandStatePhilox4_32_10_t` 生成了符合泊松分布的一个无符号整型随机数。该泊松分布的$\lambda$参数由函数输入决定。

```cpp
__device__ unsigned int surand_poisson(surandStateMtgp32_t *state,
                                        float lambda);
```

使用mtgp32状态对象 `surandStateMtgp32_t` 生成了符合泊松分布的一个无符号整型随机数。该泊松分布的$\lambda$参数由函数输入决定。

##### surand_poisson4
```cpp
__device__ __host__ uint4 surand_poisson4 (surandStatePhilox4_32_10_t *state,
                                    float lambda);
```

使用Philox4x32-10状态对象`surandStatePhilox4_32_10_t`生成了符合泊松分布的四个无符号整型随机数。该泊松分布的$\lambda$参数由函数输入决定。通过使用Philox4x32-10的算法，使用`surand_poisson4`的执行效率比使用`surand_poisson`更高。

##### 生成二项分布无符号整型随机数
```cpp
__device__ __host__ unsigned int surand_binomial(surandStateXORWOW_t *state,
                                         unsigned int n, float p);
```
使用xorwow状态对象 `surandStateXORWOW_t` 生成了符合二项分布的一个无符号整型随机数。该二项分布的参数$n$和$p$由函数输入决定。
```cpp
__device__ __host__ unsigned int surand_binomial(surandStatePhilox4_32_10_t *state,
                                         unsigned int n, float p);
```
使用Philox4x32-10状态对象 `surandStatePhilox4_32_10_t` 生成了符合二项分布的一个无符号整型随机数。该二项分布的参数$n$和$p$由函数输入决定。

<div style="page-break-after:always"></div>

## 法律声明

**著作权©**

壁仞科技2020-2025，版权所有。未经壁仞科技事先书面许可，本文档内容不得以任何形式将其复制、修改、出版、传输或发布。

**商标。**

本文档所包含的任何壁仞科技的商号、商标、图形标志和域名，均为壁仞科技所有。未经壁仞科技事先书面许可，不得以任何形式将其复制、修改、出版、传输或发布。

**性能信息**。

本文档中所包含的性能指标包括设计规格、模拟测试指标以及特定环境下的测试和评估指标。设计规格为产品设计时拟定的指标，仅用于提供信息的目的而供您参考，实测指标将以具体的测试数据为准。模拟测试指标是通过在体系结构模拟器上运行模拟而获得，仅用于提供信息目的。该类测试的系统硬件、软件设计或配置的任何不同都可能影响实际性能。特定环境下的测试和评估指标系采用特定的计算机系统或组件操作而获得，可反映出我司产品的大致性能。系统硬件、软件设计或配置的任何不同都可能影响实际性能。

**前瞻性陈述。**

本文档的信息可能包含前瞻性陈述，可能存在风险和不确定性。请勿仅依赖于上述信息做出您的商业决定。

**注意。**

本产品后续可能进行版本升级，本文档内容会不定期更新。除非在合同中另有约定，本文档仅作产品使用指导，其中的信息和建议不构成任何明示或暗示的担保。
