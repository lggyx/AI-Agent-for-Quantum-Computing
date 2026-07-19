# 壁仞™ suFFT 用户指南

## suFFT简介

本文档描述了 BIRENSUPA™ 快速傅里叶变换（Fast Fourier Transform, FFT）计算库产品 suFFT，suFFT 库为壁仞™ GPU 提供高性能的快速傅里叶变换计算。

FFT 是计算复数或实数数据序列离散傅里叶变换（Discrete Fourier Transform, DFT）的高效分治算法，它是计算物理和通用信号处理领域最重要的和使用最为广泛的数值算法之一。壁仞科技提供的 suFFT 库经过高度优化和测试，为在壁仞 GPU 上执行 FFT 计算提供了简洁易用的接口，帮助用户快速、充分地利用壁仞通用 GPU 的浮点运算性能和高并行性。

suFFT 支持多种在壁仞 GPU 上高效计算的FFT输入及选项，该版本的 suFFT 库有以下特征：

1. 支持输入序列长度在 32 位有符号整型数范围内，长度为任意 2，3，5，7，11，13 的幂次，或者这些幂次的任意乘法组合，算法已经经过高度优化。
2. 算法的时间复杂度都是$O\left( n\log n \right)$，其中$n$ 为序列长度。
3. 支持单精度浮点（32bit）数据类型。
4. 支持复数输入输出(C2C),实数输入复数输出(R2C),复数输入实数输出(C2R)。
5. 支持1D变换。
6. 可以同时执行多个1D变换，这种批处理的变换比单个变换有更高的性能。
7. 支持异地（out-of-place）变换。
8. 流式执行，支持异步计算和数据移动。

<div style="page-break-after:always"></div>

## 使用suFFT API

本章提供 suFFT 库的 API 概览，有关函数更完整的信息请参考[suFFT API参考手册](#sufft-api-参考手册)。建议您首先阅读本章节内容并了解 suFFT 的关键概念后，再深入查看更详细的说明。

DFT将一个时域复数向量$x_{n}$映射到它的频域表示，变换公式如下所示：

$$
X_{k} = \sum_{n = 0}^{N - 1}x_{n}e^{- 2\pi i\frac{kn}{N}}
$$

其中，$X_{k}$是相同长度的复数向量。上式是正向的DFT公式，如果e的指数符号变为正的，那么该公式就变成了逆变换。根据$N$的大小采用不同的算法可以获得更好的性能。

suFFT使用简单的称为plan的配置机制，它使用内部构建的块基于给定的配置和特定的GPU来优化FFT变换。如下图所示：

1. 通过 `sufftCreatePlan()`函数创建plan,然后通过 `sufftBuildPlan*()`函数配置该plan。
2. 当 `sufftExecC2C()`等执行函数被调用时，实际的变换按照plan的配置去执行。这种方式的优势在于一旦用户创建了一个plan，suFFT库会保留重复执行plan所需的任何状态而无需重新计算配置。由于不同类型的FFT变换需要不同的线程配置和GPU资源，而plan接口提供了一种重用配置的简单方法，所以这种模式对于suFFT非常有效。
3. 当某个plan不再需要时，可以调用 `sufftDestroy()`销毁该plan。

<img src="./images/sufft_exec_flow.png"/>
<p align="center">图 2‑1 suFFT执行流程图</p>

使用suFFT计算BATCH个长度为NX的一维DFT通常如下所示：

```cpp
#define NX 256
#define BATCH 10
…
{
    sufftHandle_t plan;
    size_t workSize;
    suComplex *data;
    ...
    suMalloc((void**) &data, sizeof(suComplex)*NX*BATCH);
    sufftCreatePlan(&plan);
    sufftBuildPlan1d(plan,NX,BATCH,SUFFT_TYPE_C2C,&workSize);
    ...
    sufftExecC2C(plan, data, data, SUFFT_DIRECTION_FORWARD);
    suDeviceSynchronize();
    ...
    sufftDestroy(plan);
    suFree(data);
}
```

### 获取 suFFT

suFFT作为共享库被使用，它包含编译的程序，方便用户用编译器和链接器将其一起整合进相应的上层应用。suFFT计算库可以从壁仞官网下载。通过下载SUPA产品发行版，用户可以安装含有SUPA工具链的安装包、SDK 代码以及开发驱动。SUPA工具链包含suFFT以及示例example-c2c-1d。

以ubuntu20.04操作系统为例，suFFT与其依赖的BRCC编译器的默认安装路径如下表所示

| **产品** | **位置**                                            | **头文件**                                          |
| -------------- | --------------------------------------------------------- | --------------------------------------------------------- |
| BRCC编译器     | `/usr/local/birensupa/sdk/latest/brcc/bin/brcc`         |                                                           |
| suFFT库        | `/usr/local/birensupa/sdk/latest/sufft/lib/libsufft.so` | `/usr/local/birensupa/sdk/latest/sufft/include/sufft.h` |

对于开发者来说最常见的情况是修改一个现成的SUPA程序(file.su)来调用suFFT。这种情况下需要将头文件sufft.h添加到file.su文件中，并且需要链接sufft库。简单的编译和链接如下所示：

```shell
/usr/local/birensupa/sdk/latest/brcc/bin/brcc [options] file.su … -I/usr/local/birensupa/sdk/latest/sufft/include -L/usr/local/birensupa/sdk/latest/sufft/lib -lsufft
```

当然也可以用其它的编译方式，只要库路径设置正确，也可以使用g++编译器链接。

suFFT中的函数假定数据存放在GPU可见的内存里。这意味着任何由 `suMalloc()`，`suMallocHost()`以及 `suMallocManaged()`分配的存储空间都可以作为suFFT的输入、输出和plan工作空间。为了获得最佳的性能，输入输出以及plan工作空间应当配置在设备内存中。

### 傅里叶变换设置

使用suFFT库时，首先通过 `sufftCreatePlan()`创建一个plan,然后使用 `sufftBuildPlan1d()`配置该plan。如需执行特定大小和数据类型的变换，可能需要多个处理步骤。plan创建完成后，suFFT会推导出所需的内部步骤，这些步骤可能包括多个核函数启动、内存复制等操作。sufft运行时需要独立的临时内存空间，在不同的plan之间不共享。创建和配置完成后，用户可以使用 `sufftExecC2C()`等执行该变换。期间，产生的所有中间缓存（包括CPU和GPU内存），在plan被 `sufftDestroy()`销毁后会自动释放。

#### 可用内存要求

首次调用任意suFFT函数都会初始化suFFT核函数，如果GPU上没有足够内存的话初始化会失败。建议先初始化suFFT（通过创建并配置一个plan），然后再分配内存。

在调用 `sufftBuildPlan1d()`或 `sufftGetSize1d()`时，sufft会返回给定plan所需的GPU内存空间大小。用户可以使用 `suMalloc()`等函数自行申请GPU内存空间，并通过 `sufftSetWorkArea()`完成设置以便sufft使用；也可以直接调用 `sufftExec*()`，由sufft自动申请并管理当前plan所需的内存空间。

### 傅里叶变换类型

当前版本的suFFT支持以下类型的变换：

1. 复数到复数（Complex-to-Complex, C2C）变换。
2. 实数到复数（Real-to-Complex, R2C）变换。
3. 复数到实数（Complex-to-Real, C2R）变换。

单精度傅里叶变换执行函数定义如下：

- sufftExecC2C()---单精度复数到复数变换
- sufftExecR2C()---单精度实数到复数变换
- sufftExecC2R()---单精度复数到实数变换

### 数据布局

在suFFT库中，数据布局严格依赖变换的类型和配置。

- 在复数到复数变换中，输入和输出数据都是长度为L的suComplex类型的数组。
- 在实数到复数变换中，输入为实数数组，输出为满足厄米特对称的复数数组，以python风格的下标描述为 ``output[i] = conjugate(output[-i])``。所以, 我们只输出L/2+1长度的变换结果以提升性能并减少内存占用。
- 在复数到实数变换中，输入为满足厄米特对称的复数数组，输出为实数数组。同样的，我们只取$L/2+1$长度的输入来提升性能和减少内存占用。

| **FFT 类型** | **输入数据大小**   | **输出数据大小**   |
| ------------------ | ------------------------ | ------------------------ |
| C2C                | $L$ suFloatComplex     | $L$ suFloatComplex     |
| R2C                | $L$ float              | $L/2+1$ suFloatComplex |
| C2R                | $L/2+1$ suFloatComplex | $L$ float              |

### 流式 suFFT 变换

每一个suFFT plan都与一个SUPA流（stream）相关联。一旦关联上，该plan执行期间启动的所有核函数都通过这个特定的流进行，suFFT的流式执行允许变换和内存复制之间存在重叠。如果plan没有被指定与某个流相关联，则会自动与SUPA默认的流stream(0)相关联。需要注意的是，大部分plan执行需要启动多个核函数。

每一个同时发生的plan 执行需要它独立的工作空间，在当前版本中，plan的工作空间仅被suFFT本身管理，用户可通过 `sufftGetSize1d()`和 `sufftBuildPlan1d()`查询工作空间使用量。

### 线程安全

只要不同的主机端线程使用不同的plan执行FFT，并且输出数据之间是不相关的，那么suFFT API就是线程安全的。

### 精度与性能

DFT可以通过矩阵与向量相乘得到，计算的时间复杂度是$O\left( N^{2} \right)$。suFFT使用Stockham算法优化傅里叶变换性能。suFFT 库构建的基本矩阵块在当前版本中包括以下基数(radix)：2、3、5、7、11、13。单纯的Stockham计算有非常高的精度，其相对误差与$\log_{2}(N)$成正比。

suFFT 批处理plan要求输入数据包括所有批次的有效信号。批处理模式下的性能优化可以组合来自不同批的信号进行处理。

<div style="page-break-after:always"></div>

## suFFT API 参考手册

本章介绍suFFT库函数，包括输入/输出参数、数据类型和错误代码。suFFT库在API函数被第一次调用时初始化，并且当所有用户创建的FFT plan被销毁时会自动关闭。

### 返回值 sufftStatus_t

除了SUFFT_STATUS_SUCCESS之外的所有suFFT库返回值都表明当前API调用失败，用户应该重新配置以解决问题。可能的返回值定义如下：

```cpp
typedef enum {
    SUFFT_STATUS_SUCCESS = 0, // suFFT操作成功
    SUFFT_STATUS_INVALID_PLAN = 1, // 传递给suFFT的plan句柄无效 
    SUFFT_STATUS_ALLOC_FAILED = 2, // suFFT未能分配GPU或CPU内存
    SUFFT_STATUS_INVALID_TYPE = 3, // type属性无法被识别
    SUFFT_STATUS_INVALID_VALUE = 4, // 用户指定的指针或参数无效
    SUFFT_STATUS_INTERNAL_ERROR = 5, // 驱动程序或内部suFFT库错误
    SUFFT_STATUS_EXEC_FAILED = 6, // 未能在GPU上执行FFT
    SUFFT_STATUS_SETUP_FAILED = 7, // suFFT库未能初始化
    SUFFT_STATUS_INVALID_SIZE = 8, // 用户指定的变换大小无效
    SUFFT_STATUS_UNALIGNED_DATA = 9, // 数据指针未对齐
    SUFFT_STATUS_INCOMPLETE_PARAMETER_LIST = 10, // 缺少调用参数
    SUFFT_STATUS_INVALID_DEVICE = 11, // 无效的GPU设备
    SUFFT_STATUS_PARSE_ERROR = 12, // 内部plan数据库错误
    SUFFT_STATUS_NO_WORKSPACE = 13, // plan执行前未提供工作空间
    SUFFT_STATUS_NOT_IMPLEMENTED = 14, // 给定参数的函数功能尚未实现
    SUFFT_STATUS_LICENSE_ERROR = 15, // 在以前的版本使用
    SUFFT_STATUS_NOT_SUPPORTED = 16 // 给定参数的操作不支持
} sufftStatus_t;
```

### suFFT 类型

#### 参数 sufftType_t

suFFT库支持复数数据的变换。数据类型sufftType_t是suFFT支持的变换数据类型的枚举。

```cpp
typedef enum {
    SUFFT_TYPE_R2C = 0,  // 实数到复数(实部虚部交错存储)变换
    SUFFT_TYPE_C2R = 2,  // 复数(实部虚部交错存储)到实数变换
    SUFFT_TYPE_C2C = 1  // 复数到复数(实部虚部交错存储)变换
} sufftType_t;
```

#### 变换方向参数

suFFT库根据复数指数项的符号定义正向和逆向快速傅里叶变换。

```cpp
type enum{
	SUFFT_DIRECTION_FORWARD=0,
    SUFFT_DIRECTION_INVERSE=1
}sufftDirection_t
```

#### 其它 suFFT 类型

##### sufftHandle_t

用于存储和访问suFFT plan的句柄类型。用户在创建suFFT plan后会得到一个句柄，并使用该句柄执行plan。

```cpp
typedef long long sufftHandle_t;
```

### suFFT 基础的 Plan

#### 函数 sufftCreatePlan()

```cpp
sufftStatus_t sufftCreatePlan(sufftHandle_t *plan);
```

只创建一个不透明的句柄，并在主机端分配小型的数据结构。调用sufftBuildPlan1d()才会实际执行plan配置。

##### 输入

| 参数 | 描述                        |
| ---- | --------------------------- |
| plan | 指向sufftHandle_t对象的指针 |

##### 输出

| 参数 | 描述                     |
| ---- | ------------------------ |
| plan | 包含一个suFFT plan句柄值 |

##### 返回值

| 值                          | 描述                          |
| --------------------------- | ----------------------------- |
| SUFFT_STATUS_SUCCESS        | suFFT成功创建了FFT plan       |
| SUFFT_STATUS_ALLOC_FAILED   | 为plan分配资源失败            |
| SUFFT_STATUS_INVALID_VALUE  | 向API传递了一个或多个无效参数 |
| SUFFT_STATUS_INTERNAL_ERROR | 内部驱动程序错误              |
| SUFFT_STATUS_SETUP_FAILED   | suFFT库未能初始化             |

#### 函数 sufftBuildPlan1d()

```cpp
sufftStatus_t sufftBuildPlan1d(sufftHandle_t plan, int nx, int batch, sufftType_t type, size_t *workSize);
```

根据指定的信号大小和数据类型创建1D FFT plan配置，参数batch表示需要配置多少个1D变换。

对于给定句柄，此调用只能使用一次。如果该句柄已经被用于不同的sufftPlan, 那么plan会处于锁定状态，本次调用将会返回 `SUFFT_STATUS_INVALID_PLAN`。

在当前版本中，支持输入序列长度为：在32位有符号整型数范围内，长度为任意2，3或5的幂次，或者这些幂次的任意乘法组合。

##### 输入

| 参数  | 描述                                                               |
| ----- | ------------------------------------------------------------------ |
| plan  | 指向sufftHandle_t对象的指针                                        |
| nx    | 变换的大小（例如，256表示256个点的FFT）                            |
| type  | 变换的数据类型（例如，SUFFT_TYPE_C2C表示单精度的复数到复数的变换） |
| batch | 大小为多少个nx的变换。                                             |

##### 返回值

| 参数                       | 描述                                             |
| -------------------------- | ------------------------------------------------ |
| SUFFT_STATUS_SUCCESS       | suFFT成功配置了FFT plan                          |
| SUFFT_STATUS_INVALID_PLAN  | 参数plan不是有效的句柄。当plan被锁定时，句柄无效 |
| SUFFT_STATUS_ALLOC_FAILED  | 为plan分配GPU资源失败                            |
| SUFFT_STATUS_INVALID_VALUE | 向API传递了一个或多个无效参数                    |

### 管理 suFFT 所需的 workSize

#### 函数 sufftGetSize1d()

```cpp
sufftStatus_t sufftGetSize1d(sufftHandle_t handle, int nx, sufftType_t type, int batch,
                 size_t *workSize);
```

使用 `sufftBuildPlan*`配置plan后，此调用将返回支持plan所需的工作空间的实际大小。此调用必须在plan生成之后以及plan生成后的任何可能会改变所需的工作空间大小的 `sufftSet*`()调用之后使用。

- **输入**

| 参数     | 描述                                 |
| -------- | ------------------------------------ |
| handle   | sufftCreatePlan返回的sufftHandle_t   |
| nx       | 给定Plan的nx                         |
| type     | 给定Plan的变换数据类型               |
| batch    | 给定Plan的batch                      |
| workSize | 指向工作空间大小的指针，以字节为单位 |

- **输出**

| 参数     | 描述                   |
| -------- | ---------------------- |
| workSize | 指向工作空间大小的指针 |

- **返回值**

| 值                         | 描述                          |
| -------------------------- | ----------------------------- |
| SUFFT_STATUS_SUCCESS       | suFFT成功返回了工作空间的大小 |
| SUFFT_STATUS_INVALID_VALUE | 无效的workSize参数            |

### 函数 sufftSetWorkArea()

```cpp
sufftStatus_t sufftSetWorkArea(sufftHandle_t plan, void *workArea);
```

当用户准备好suFFT所需的工作空间之后，需要使用本API将 `workArea`传递给要使用的 `plan`

- **输入**

| 参数     | 描述                               |
| -------- | ---------------------------------- |
| handle   | sufftCreatePlan返回的sufftHandle_t |
| workArea | 用户准备好的workArea指针           |

- **返回值**

| 值                         | 描述                          |
| -------------------------- | ----------------------------- |
| SUFFT_STATUS_SUCCESS       | suFFT成功返回了工作空间的大小 |
| SUFFT_STATUS_INVALID_VALUE | 无效的workArea参数            |

### 函数 sufftDestroy ()

```cpp
sufftStatus_t sufftDestroy(sufftHandle_t plan);
```

释放与suFFT plan关联的所有GPU资源，并销毁内部plan数据结构。一旦不再需要某个plan，就应该调用此函数销毁该plan，以避免浪费GPU资源。

- **输入**

| 参数 | 描述                          |
| ---- | ----------------------------- |
| plan | 即将被销毁的sufftHandle_t对象 |

- **返回值**

| 值                        | 描述                      |
| ------------------------- | ------------------------- |
| SUFFT_STATUS_SUCCESS      | suFFT成功地销毁了FFT plan |
| SUFFT_STATUS_INVALID_PLAN | 参数plan不是有效的句柄    |

### suFFT 执行

#### 函数 sufftExecC2C()

```cpp
sufftStatus_t sufftExecC2C(sufftHandle_t plan, suFloatComplex *input,
        suFloatComplex *output, sufftDirection_t direction);
```

sufftExecC2C()在参数direction指定的变换方向上执行单精度的复数到复数的变换plan。suFFT使用参数input指向的GPU内存作为输入数据，将FFT的结果存储在output数组中。

- **输入**

| 参数      | 描述                                          |
| --------- | --------------------------------------------- |
| plan      | sufftCreatePlan返回的sufftHandle_t            |
| input     | 指向要变换的复数输入数据（在GPU内存中）的指针 |
| output    | 指向复数输出数据（在GPU内存中）的指针         |
| direction | 变换的方向                                    |

- **返回值**

| 值                         | 描述                          |
| -------------------------- | ----------------------------- |
| SUFFT_STATUS_SUCCESS       | suFFT成功地执行了FFT plan     |
| SUFFT_STATUS_INVALID_PLAN  | 参数plan不是有效的句柄        |
| SUFFT_STATUS_INVALID_VALUE | 向API传递了一个或多个无效参数 |
| SUFFT_STATUS_EXEC_FAILED   | suFFT未能在GPU上执行变换      |

#### 函数 sufftExecR2C()

```cpp
sufftStatus_t sufftExecR2C(sufftHandle_t plan, float *input,
        suFloatComplex *output);
```

sufftExecR2C()执行单精度的实数到复数的变换plan，方向固定为正向。suFFT使用参数input指向的GPU内存作为输入数据，将FFT的结果存储在output数组中。

- **输入**

| 参数   | 描述                                          |
| ------ | --------------------------------------------- |
| plan   | sufftCreatePlan返回的sufftHandle_t            |
| input  | 指向要变换的复数输入数据（在GPU内存中）的指针 |
| output | 指向复数输出数据（在GPU内存中）的指针         |

- **返回值**

| 值                         | 描述                          |
| -------------------------- | ----------------------------- |
| SUFFT_STATUS_SUCCESS       | suFFT成功地执行了FFT plan     |
| SUFFT_STATUS_INVALID_PLAN  | 参数plan不是有效的句柄        |
| SUFFT_STATUS_INVALID_VALUE | 向API传递了一个或多个无效参数 |
| SUFFT_STATUS_EXEC_FAILED   | suFFT未能在GPU上执行变换      |

#### 函数 sufftExecC2R()

```cpp
sufftStatus_t sufftExecC2R(sufftHandle_t plan, suFloatComplex *input,
        float *output);
```

sufftExecC2R()执行单精度的复数到实数的变换plan，方向固定为反向。suFFT使用参数input指向的GPU内存作为输入数据，将FFT的结果存储在output数组中。

- **输入**

| 参数   | 描述                                          |
| ------ | --------------------------------------------- |
| plan   | sufftCreatePlan返回的sufftHandle_t            |
| input  | 指向要变换的复数输入数据（在GPU内存中）的指针 |
| output | 指向复数输出数据（在GPU内存中）的指针         |

- **返回值**

| 值                         | 描述                          |
| -------------------------- | ----------------------------- |
| SUFFT_STATUS_SUCCESS       | suFFT成功地执行了FFT plan     |
| SUFFT_STATUS_INVALID_PLAN  | 参数plan不是有效的句柄        |
| SUFFT_STATUS_INVALID_VALUE | 向API传递了一个或多个无效参数 |
| SUFFT_STATUS_EXEC_FAILED   | suFFT未能在GPU上执行变换      |

### 函数 sufftSetStream()

```cpp
sufftStatus_t sufftSetStream(sufftHandle_t plan, suStream_t stream);
```

将一个SUPA流与suFFT plan相关联。在plan执行期间启动的所有核函数现在都通过相关流完成，从而与其它流中的活动可以重叠（例如数据复制）。该关联将一直保留着，直到plan被销毁或者该流被另一次sufftSetStream()调用所更改。

- **输入**

| 参数   | 描述                                              |
| ------ | ------------------------------------------------- |
| plan   | 与流相关联的sufftHandle_t对象                     |
| stream | 使用supaStreamCreate()创建的有效SUPA流；默认流为0 |

- **返回值**

| 值                         | 描述                   |
| -------------------------- | ---------------------- |
| SUFFT_STATUS_SUCCESS       | 流与plan已关联         |
| SUFFT_STATUS_INVALID_PLAN  | 参数plan不是有效的句柄 |
| SUFFT_STATUS_INVALID_VALUE | 输入了无效的stream参数 |

### 函数 sufftGetVersion()

```cpp
sufftStatus_t sufftGetVersion(int *version);
```

返回suFFT的版本号。

- **输入**

| 参数    | 描述             |
| ------- | ---------------- |
| version | 指向版本号的指针 |

- **输出**

| 参数    | 描述       |
| ------- | ---------- |
| version | 包含版本号 |

- **返回值**

| 值                         | 描述                  |
| -------------------------- | --------------------- |
| SUFFT_STATUS_SUCCESS       | suFFT成功返回了版本号 |
| SUFFT_STATUS_INVALID_VALUE | 输入了无效的参数      |

<div style="page-break-after:always"></div>

## suFFT 代码范例

### 1D 复数-复数变换

在这个例子中，我们考虑一维的复数-复数变换问题。

```cpp
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <supa.h>
#include <vector>

#include <sufft.h>

#include "utility.hpp"

int main(int argc, const char **argv) {
    sufftHandle_t plan;
    suComplex *d_input;
    suComplex *d_output;

    int n = 64;

    std::vector<suComplex> h_input(n);
    std::vector<suComplex> h_output(n);

    // Allocate device memory
    CHECK_SUPA_ERROR(suMallocDevice((void **)&d_input, sizeof(suComplex) * n));
    CHECK_SUPA_ERROR(suMallocDevice((void **)&d_output, sizeof(suComplex) * n));

    // Init d_input values
    for (int i = 0; i < n; i++) {
        h_input[i].x = i;
        h_input[i].y = 0;
        std::cout << std::fixed           // fix the number of decimal digits
                  << std::setprecision(6) // to 2
                  << i << " " << h_input[i].x << ", " << h_input[i].y
                  << std::endl;
    }

    // Copy host memory to device
    CHECK_SUPA_ERROR(suMemcpy(d_input, h_input.data(), sizeof(suComplex) * n));

    // Create plan
    if (sufftCreatePlan(&plan) != SUFFT_STATUS_SUCCESS) {
        fprintf(stderr, "sufft error: Plan create failed\n");
    }

    // Build the plan
    size_t workSize = 0;
    if (sufftBuildPlan1d(plan, n, 1, SUFFT_TYPE_C2C, &workSize) !=
        SUFFT_STATUS_SUCCESS) {
        fprintf(stderr, "sufft error: Plan build failed\n");
    }

    // Execute the forward pass
    if (sufftExecC2C(plan, d_input, d_output, SUFFT_DIRECTION_FORWARD) !=
        SUFFT_STATUS_SUCCESS) {
        fprintf(stderr, "sufft error: ExecC2C Forward failed\n");
    }

    // Copy host memory to device
    CHECK_SUPA_ERROR(
        suMemcpy(h_output.data(), d_output, sizeof(suComplex) * n));

    // Print the result
    for (int i = 0; i < n; i++) {
        std::cout << std::fixed           // fix the number of decimal digits
                  << std::setprecision(6) // to 2
                  << i << " " << h_output[i].x << ", " << h_output[i].y
                  << std::endl;
    }

    if (suDeviceSynchronize() != suSuccess) {
        fprintf(stderr, "su error: Failed to synchronize\n");
    }

    sufftDestroy(plan);
    suFree(d_input);
    suFree(d_output);
    return 0;
}
```

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
