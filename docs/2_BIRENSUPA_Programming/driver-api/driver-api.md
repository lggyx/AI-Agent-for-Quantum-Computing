
# BIRENSUPA™ 驱动 API 参考

## 错误处理

本节介绍 BIRENSUPA™ 驱动应用程序编程接口的错误处理功能。

### sudrvGetErrorName

返回错误代码枚举名称的字符串表示形式。

**函数签名**

```cpp

suError_t sudrvGetErrorName(suError_t error, const char **str);

```


**参数列表**

- `error` [in]：需要转换为字符串的错误代码
- `str` [out]：返回指向错误名称的字符串地址

**返回值**

-  `suSuccess`

**描述**

返回一个字符串，其中包含枚举中错误代码的名称。
如果无法识别错误码，则为“unrecognized error code”。

### sudrvGetErrorString

返回错误码的字符串形式的解释。

**函数签名**

```cpp
suError_t sudrvGetErrorString(suError_t error, const char **str);
```

**参数列表**

- `error` [in]：需要转换为字符串的错误代码
- `str`[out]：返回错误码字符串地址

**返回值**
-  `suSuccess`

**描述**

返回错误码的说明字符串。

> 如果无法识别错误代码，则返回“unrecognized error code”。

##  驱动初始化

### sudrvInit

初始化驱动程序

**函数签名**

```cpp
suError_t sudrvInit(unsigned int flags);
```

**参数列表**
- flags[in]：传0即可

**返回值**

-  `suSuccess`

**描述**

初始化当前进程的驱动程序实例

##  版本管理

### sudrvGetVersion

返回驱动程序版本

**函数签名**

```cpp
suError_t sudrvGetVersion(int *driverVersion);
```

**参数列表**

- driverVersion[out]：返回驱动程序版本

**返回值**
-  `suSuccess`

**描述**

返回驱动程序版本

##  设备管理

### sudrvDeviceGet

返回当前正在使用的设备。

**函数签名**

```cpp
suError_t sudrvDeviceGet(suDevice *device, int ordinal);
```


**参数列表**

- `device` [out]：用于返回当前设备号
- `ordinal`[in]：设备句柄

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*device` 中返回`ordinal`指定的设备号。

### sudrvDeviceGetAttribute

查询设备的相关属性。

```cpp
suError_t sudrvDeviceGetAttribute(int *value, suDeviceAttr attr,
                                  suDevice device);
```

**参数列表**

- `value`[out]：用于返回和`attr`对应的属性值
- `attr`[in]： 需要查询的设备属性
- `device`[in]：要查询的设备号

**返回值**

- `suSuccess`
- `suErrorInvalidDevice`：
- `suErrorInvalidValue`

**描述**

在 `*value` 中返回设备设备上属性`attr` 的整数值。支持的属性包括：

| 可选值 | 说明 |  |
| ---- | ---- | ---- |
| suDevAttrMaxThreadsPerBlock | 每个线程块的最大线程数。 |  |
| suDevAttrMaxBlockDimX | 线程块 X 维度最大值。 |  |
| suDevAttrMaxBlockDimY | 线程块 Y 维度最大值。 |  |
| suDevAttrMaxBlockDimZ | 线程块 Z 维度最大值。 |  |
| suDevAttrMaxGridDimX | 线程网格 X 维度最大值。 |  |
| suDevAttrMaxGridDimY | 线程网格 Y 维度最大值。 |  |
| suDevAttrMaxGridDimZ | 线程网格 Z 维度最大值。 |  |
| suDevAttrMaxSharedMemoryPerBlock | 每个线程块的最大可用共享内存（以字节为单位）。 |  |
| suDevAttrTotalConstantMemory | 核函数中**constant**变量在设备上可用的内存(以字节为单位)。 |  |
| suDevAttrWarpSize | 线程束大小。 |  |
| suDevAttrMaxPitch | 内存拷贝允许的最大字节间距。 |  |
| suDevAttrMaxRegistersPerBlock | 每个线程块允许的最大 32 位寄存器数。 |  |
| suDevAttrClockRate | 峰值时钟频率(千赫兹)。 |  |
| suDevAttrGpuOverlap | 设备可以同时复制内存和执行核函数。 |  |
| suDevAttrMultiProcessorCount | 设备上的多处理器数量。 |  |
| suDevAttrKernelExecTimeout | 指定核函数是否有运行时限制。 |  |
| suDevAttrIntegrated | 设备与主机内存集成。 |  |
| suDevAttrCanMapHostMemory | 设备可以将主机内存映射到 BIRENSUPA 地址空间。 |  |
| suDevAttrComputeMode | 计算模式。 |  |
| suDevAttrConcurrentKernels | 设备可以同时执行多个核函数。 |  |
| suDevAttrEccEnabled | 设备已启用 ECC 支持。 |  |
| suDevAttrPciBusId | 设备的 PCI 总线 ID。 |  |
| suDevAttrPciDeviceId | 设备的 PCI 设备 ID。 |  |
| suDevAttrTccDriver | 设备正在使用 TCC 驱动模型。 |  |
| suDevAttrMemoryClockRate | 峰值内存时钟频率(千赫兹)。 |  |
| suDevAttrGlobalMemoryBusWidth | 全局内存总线宽度(以位为单位)。 |  |
| suDevAttrL2CacheSize | L2 缓存大小(以字节为单位)。 |  |
| suDevAttrMaxThreadsPerMultiProcessor | 每个多处理器最多驻留线程数。 |  |
| suDevAttrAsyncEngineCount | 异步引擎的数量。 |  |
| suDevAttrUnifiedAddressing | 设备与主机共用统一的地址空间。 |  |
| suDevAttrPciDomainId | 设备的 PCI 域 ID。 |  |
| suDevAttrComputeCapabilityMajor | 主要计算能力版本号。 |  |
| suDevAttrComputeCapabilityMinor | 次要计算能力版本号。 |  |
| suDevAttrStreamPrioritiesSupported | 设备支持流优先级。 |  |
| suDevAttrLocalL1CacheSupported | 设备支持在 L1 中缓存局部变量。 |  |
| suDevAttrMaxSharedMemoryPerMultiprocessor | 每个多处理器可用的最大共享内存（以字节为单位）。 |  |
| suDevAttrMaxRegistersPerMultiprocessor | 每个多处理器可用的最大 32 位寄存器数。 |  |
| suDevAttrManagedMemory | 设备可以在此系统上分配托管内存。 |  |
| suDevAttrIsMultiGpuBoard | 设备位于多 GPU 板上。 |  |
| suDevAttrMultiGpuBoardGroupID | 同一多 GPU 板上一组设备的唯一标识符。 |  |
| suDevAttrHostNativeAtomicSupported | 设备和主机之间的连接支持本机原子操作。 |  |
| suDevAttrPageableMemoryAccess | 设备支持连贯地访问可分页内存。 |  |
| suDevAttrConcurrentManagedAccess | 设备可以与 CPU 同时访问托管内存。 |  |
| suDevAttrComputePreemptionSupported | 设备支持计算抢占。 |  |
| suDevAttrCanUseHostPointerForRegisteredMem | 设备可以在与 CPU 相同的虚拟地址访问主机注册内存。 |  |
| suDevAttrCooperativeLaunch | 设备支持启动协作核函数。 |  |
| suDevAttrPageableMemoryAccessUsesHostPageTables | 设备通过主机的页表访问可分页内存。 |  |
| suDevAttrDirectManagedMemAccessFromHost | 主机无需迁移即可直接访问设备上的托管内存。 |  |

  

### sudrvGetDeviceCount

返回系统中设备的数量。


**函数签名**

```cpp

suError_t sudrvGetDeviceCount(int *count);

```

**参数列表**

- `count` [out]：用于返回系统中可用设备数量

**返回值**

- `suSuccess`
- `suErrorInvalidValue`


**描述**

在`*count`中返回可用的设备数量。

### sudrvDeviceGetName

查询设备名称


```cpp
suError_t sudrvDeviceGetName(char *deviceName, int maxLen, suDevice device);
```

**参数列表**

- `deviceName` [out]：用于返回设备名称的地址
- `maxLen`[in]：`deviceName`能容纳的最大字符串长度
- `device`[in]：要查询的设备号

 
**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidDevice`


**描述**

在`*deviceName`中返回设备`device`的名称。


### sudrvDeviceGetUuid

查询设备的UUID


```cpp
suError_t sudrvDeviceGetUuid(suUUID_t *uuid, suDevice device);
```

**参数列表**

- `uuid` [out]：用于返回设备uuid
- `device`[in]：要查询的设备号


**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidDevice`

**描述**

在`*uuid`中返回设备`device`的`UUID`。

### sudrvDeviceTotalMem

获取可用内存和总设备内存。

**函数签名**

```cpp
suError_t sudrvDeviceTotalMem(size_t *bytes, suDevice device);
```

**参数列表**

- `bytes`[out]：返回的可用内存的大小（以字节为单位）
- `device`[in]：要查询的设备号

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*bytes`中返回当前上下文可用的内存总量。

##  原始上下文管理

### sudrvPrimaryContextGetState

查询设备的原始上下文状态

**函数签名**

```cpp
suError_t sudrvPrimaryContextGetState(suDevice device, unsigned int *flags,
                                      int *active);
```

**参数列表**

- `device`[in]：要查询的设备号
- `flags`[out]：返回标志
- `active`[out]：返回查询到的状态

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidDevice`

**描述**

在`*flags`和`*active`中返回上下文的标志和状态

### sudrvPrimaryContextRelease

释放指定设备上的原始上下文。

**函数签名**

```cpp
suError_t sudrvPrimaryContextRelease(suDevice device);
```

**参数列表**

- `device`[in]：要释放上下文的设备号

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidDevice`

**描述**

释放设备`device`上的原始上下文。


### sudrvPrimaryContextReset

释放设备原始上下文上的所有资源，并重置所有状态。

**函数签名**

```cpp
suError_t sudrvPrimaryContextReset(suDevice device);
```

**参数列表**

- `device`[in]：要重置的设备号

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidDevice`

**描述**

重置设备`device`上的原始上下文。

### sudrvPrimaryContextRetain

获取指定设备上的原始上下文句柄。

**函数签名**

```cpp
suError_t sudrvPrimaryContextRetain(suContext *context, suDevice device);
```

**参数列表**

- `context`[out]：返回上下文句柄
- `device`[in]：要查询的设备号

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

获取设备`device`上的原始上下文句柄，并在`*context`中返回。

### sudrvPrimaryContextSetFlags

设置原始上下文标志。

**函数签名**

```cpp
suError_t sudrvPrimaryContextSetFlags(suDevice device, unsigned int flags);
```

**参数列表**

- `device`[in]：返回的可用内存的大小（以字节为单位）
- `flags`[in]：要查询的设备号

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

用`flags`的值设置设备`device`上的原始上下文的标志。
  
##  用户上下文管理

### sudrvContextCreate

创建一个`BIRENSUPA` 上下文。

**函数签名**

```cpp
suError_t sudrvContextCreate(suContext *context, unsigned int flags,
                             suDevice device);
```

**参数列表**

- `context`[out]：返回新创建的上下文
- `flags`[in]：保留供后续使用
- `device`[in]：用于创建上下文的设备

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidDevice`

**描述**

在设备`device`上创建一个新的上下文并与当前主机线程绑定，新创建的上下文在`*context`中返回。此时调用`sudrvContextGetCurrent()`会返回当前创建的上下文。如果用户使用完这个上下文，可以使用`sudrvContextPopCurrent()`弹出这个上下文，或者用`sudrvContextDestroy()`直接销毁这个上下文。


### sudrvContextDestroy

销毁上下文。

**函数签名**

```cpp
suError_t sudrvContextDestroy(suContext context);
```

**参数列表**

- `context`[in]：要销毁的上下文句柄

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

销毁上下文`context`，以及上下文上的所有资源，包括`suStrean_t`，`suModule_t`，`suEvent_t`和内存等。

> 注意主机线程可能会阻塞等待上下文上的任务执行完成后再销毁资源后才返回。


### sudrvContextGetApiVersion

返回上下文的API版本。

**函数签名**

```cpp
suError_t sudrvContextGetApiVersion(suContext context, unsigned int *version);
```

**参数列表**

- `context`[in]：要查询的上下文
- `version`[out]：返回版本信息

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*version`中返回`context`的版本信息。


### sudrvContextGetCacheConfig

返回上下文的cache配置信息。

**函数签名**

```cpp
suError_t sudrvContextGetCacheConfig(suFuncCache *config);
```

**参数列表**

- `config`[out]：返回配置信息

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*config`中返回当前线程所在的上下文的缓存配置信息。


### sudrvContextGetCurrent

查询当前主机线程所在的`BIRENSUPA`上下文。

**函数签名**

```cpp
suError_t sudrvContextGetCurrent(suContext *context);
```

**参数列表**

- `context`[out]：返回当前上下文

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*context`中返回当前主机线程所在的上下文。


### sudrvContextGetDevice

查询上下文所在的设备号。

**函数签名**

```cpp
suError_t sudrvContextGetDevice(suDevice *device);
```

**参数列表**

- `device`[out]：返回设备号

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*device`中返回当前主机线程所在的上下文属于的设备号。

### sudrvContextGetFlags

返回上下文标志。

**函数签名**

```cpp
suError_t sudrvContextGetFlags(unsigned int *flags);
```

**参数列表**

- `*flags`[out]：返回上下文标志

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*flags`中返回当前主机线程所在的上下文标志。


### sudrvContextGetLimit

查询上下文的资源限制。

**函数签名**

```cpp
suError_t sudrvContextGetLimit(size_t *value, suLimit limit);
```

**参数列表**

- `size`[out]：返回限制的大小
- `limit`[in]：要查询的限制类别枚举值，支持以下 `suLimit` 类型：
	- `suLimitStackSize` 是每个 GPU 线程的堆栈大小（以字节为单位）。
	- `suLimitPrintfFifoSize` 是 `printf()` 设备系统调用使用的共享 FIFO 的大小（以字节为单位）
	- `suLimitMallocHeapSize` 是大小（以字节为单位） `malloc()` 和 `free()`设备系统调用使用的堆的大小。

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*value`中返回当前主机线程所在的上下文中`limit`指定的资源类型的限定值。

### sudrvContextGetSharedMemConfig

查询当前上下文的共享内存配置。

**函数签名**

```cpp
suError_t sudrvContextGetSharedMemConfig(suSharedMemConfig *config);
```

**参数列表**

- `config`[out]：返回的配置信息

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*config`中返回当前主机线程所在的上下文的共享内存配置信息。

### sudrvContextGetStreamPriorityRange

返回与最小和最大流优先级相对应的数值。

**函数签名**

```cpp
suError_t sudrvContextGetStreamPriorityRange(int *leastPriority,
                                             int *greatestPriority);
```

**参数列表**

- `leastPriority`[out]：返回流的最低优先级的数值
- `greatestPriority`[out]：返回流的最大优先级的数值

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

壁仞通用 GPU 硬件设计版本 1.0 不支持流优先级，此函数将在 *low 和*high 中返回0

### sudrvContextPopCurrent

从当前 CPU 线程中弹出当前上下文。

**函数签名**

```cpp
suError_t sudrvContextPopCurrent(suContext *context);
```

**参数列表**

- `context`[out]：返回弹出当前上下文后的当前上下文

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

从 CPU 线程中弹出当前 'BIRENSUPA' 上下文，并在 `*context` 中传回旧的上下文句柄。然后，可以通过调用 `sudrvContextPushCurrent`使该上下文成为其他 CPU 线程的当前上下文。

### sudrvContextPushCurrent

在当前 CPU 线程上压入上下文。

**函数签名**

```cpp
suError_t sudrvContextPushCurrent(suContext context);
```

**参数列表**

- `context`[in]：要使用的上下文

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

将给定的上下文 `context`  压入到 CPU 线程的当前上下文堆栈上。指定的上下文将成为 CPU 线程的当前上下文，因此所有 `BIRENSUPA` 在当前上下文上运行的函数会受到影响。

### sudrvContextSetCacheConfig

设置当前上下文的缓存配置方案。

**函数签名**

```cpp
suError_t sudrvContextSetCacheConfig(suFuncCache config);
```

**参数列表**

- `config`[in]：更新的缓存配置

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

设置当前上下文使用`config`中的新缓存配置。

### sudrvContextSetCurrent

将指定的 `BIRENSUPA` 上下文绑定到调用的 CPU 线程。

**函数签名**

```cpp
suError_t sudrvContextSetCurrent(suContext context);
```

**参数列表**

- `context`[in]：要绑定的上下文

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

将指定的 `BIRENSUPA` 上下文绑定到调用的 CPU 线程。如果 `context` 为 NULL，则之前绑定到调用 CPU 线程的 `BIRENSUPA` 上下文将取消绑定，并返回 `suSuccess`。

如果调用 CPU 线程上存在 `BIRENSUPA` 上下文堆栈，则会将该堆栈的顶部替换为 `context`。如果 `context` 为 NULL，则这相当于弹出调用 CPU 线程的上下文堆栈的顶部。

### sudrvContextSetLimit

设置上下文的资源限制阈值。

**函数签名**

```cpp
suError_t sudrvContextSetLimit(suLimit limit, size_t value);
```

**参数列表**

- `limit`[in]：要限制的资源类型
- `value`[in]：要更新的限制值

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

当前主机线程所在的上下文的资源类型`limit` 设置为 `value` 。

### sudrvContextSetSharedMemConfig

设置上下文的共享内存配置。

**函数签名**

```cpp
suError_t sudrvContextSetSharedMemConfig(suSharedMemConfig config);
```

**参数列表**

- `config`[in]：要更新的配置值

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

将当前主机线程所在的上下文的共享内存配置设置为 `config` 。

### sudrvContextSynchronize

阻塞等待上下文任务完成。

**函数签名**

```cpp
suError_t sudrvContextSynchronize();
```

**参数列表**

> 无

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

阻塞主机线程，等待当前主机线程所在的上下文直到上下文上所有的任务完成后再返回。


##  内核模块管理

### sudrvModuleGetFunction

获取函数句柄。

**函数签名**

```cpp

suError_t sudrvModuleGetFunction(suDevFunc_t *function, suModule_t module,

const char *name);

```

**参数列表**

- `function`[in]：返回函数句柄
- `module`[in]：函数所在的模块
- `name`[in]：函数名称

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在 `function` 中返回模块 `module` 中名为 `name` 的函数的句柄。

### sudrvModuleGetGlobal

返回设备全局变量的地址。

**函数签名**

```cpp
suError_t sudrvModuleGetGlobal(suDeviceptr_t *devPtr, size_t *size,suModule_t   
							   module, const char *name);

```


**参数列表**

- `devPtr`[out]：返回的设备地址
- `size`[out]：返回全局变量大小
- `module`[in]：全局变量所在的模块
- `name`[in]：全局变量名称

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在 `*devPtr` 和 `*size` 中，返回位于模块 `module` 中名字为 `name` 的全局变量的基指针和大小。

### sudrvModuleLoad

从文件加载一个模块的数据。

**函数签名**

```cpp
suError_t sudrvModuleLoad(suModule_t *module, const char *path);
```

**参数列表**

- `module`[out]：返回模块句柄
- `path`[in]：模块代码路径

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*module`中返回新加载模块的数据得到的模块句柄。

### sudrvModuleLoadData

加载一个模块的数据。

**函数签名**

```cpp
suError_t sudrvModuleLoadData(suModule_t *module, const void *data);
```

**参数列表**

- `module`[out]：返回模块句柄
- `data`[in]：模块代码数据

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**
在`*module`中返回新加载模块的数据得到的模块句柄。

### sudrvModuleLoadDataEx

用选项加载模块的数据。

**函数签名**

```cpp
suError_t sudrvModuleLoadDataEx(suModule_t *module, const void *image,
                                unsigned int numOptions, suJitOption *options,
                                void **optionValues);
```

**参数列表**

- `module`[out]：返回模块句柄
- `image`[in]：模块代码数据
- `numOptions`[in]：加载选项数量
- `options`[in]：加载选项类型
- `optionValues`[in]：加载选项值

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

用选项加载模块的数据。总选项数通过 `numOptions` 提供。任何输出都将通过 `optionValues` 返回。options 暂不支持。

### sudrvModuleLoadFatBinary

加载一个fatbin。

**函数签名**

```cpp
suError_t sudrvModuleLoadFatBinary(suModule_t *module, const void *fatbin);
```

**参数列表**

- `module`[out]：返回模块句柄
- `fatbin`[in]：`fatbin`数据

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

获取一个指针 `fatbin` 并将相应的模块 `module` 加载到当前上下文中。 指针代表一个 `fatbin` 对象，它是不同 `subin` 文件的集合，都代表相同的设备代码，但针对不同的架构进行了编译和优化。


### sudrvModuleUnload

卸载模块。

**函数签名**

```cpp
suError_t sudrvModuleUnload(suModule_t module);
```

**参数列表**

- `module`[in]：要卸载的模块

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

卸载由`module`指定的模块。


### sudrvModuleGetLoadingMode

查询模块的惰性加载模式。

**函数签名**

```cpp
suError_t sudrvModuleGetLoadingMode(suModuleLoadingMode *mode);
```

**参数列表**

- `mode`[out]：返回加载模式

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`mode`中返回模块的加载模式，有以下两种模式：
```cpp
typedef enum {
    /// Lazy kernel loading is not enabled
    suModuleEagerLoading = 0x1,
    /// Lazy kernel loading is enabled
    suModuleLazyLoading = 0x2,
```


##  内存管理

返回计算设备的设备号。

### sudrvDeviceGetByPCIBusId

**函数签名**

```cpp
suError_t sudrvDeviceGetByPCIBusId(suDevice *device, const char *pciBusId);
```

**参数列表**

- `device`[out]：用于返回设备序号
- `pciBusId`[in]：PCI总线ID，其中 `domain`、`bus`、`device` 和 `function`采用以下格式的字符串表示： `[domain]:[bus]:[device].[function]`。`domain`、`bus`、`device` 和 `function` 均为十六进制表示

**返回值**

- `suSuccess`
- `suErrorInvalidDevice`
- `suErrorInvalidValue`

**描述**

在给定 `PCI`总线`ID` 字符串的情况下，在 `*device` 中返回设备序号。


### sudrvDeviceGetPCIBusId

返回设备的`PCI`总线`ID`字符串。

**函数签名**

```cpp
suError_t sudrvDeviceGetPCIBusId(char *pciBusId, int len, suDevice device);
```

**参数列表**

- `pciBusId`[out]：以以下格式返回设备的标识符字符串 `[domain]:[bus]:[device].[function]` 其中 `domain`， `bus`， `device` 和 `function` 都是十六进制值。 `pciBusId` 的大小应足够存储 13 个字符（包括 NULL终止符）。
- `len`[in]：`name` 中存储的字符串的最大长度
- `device`[in]：要获取标识符的设备

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidDevice`

**描述**

在`pciBusId`中返回一个 `ASCII`的字符串来标识设备`device`，字符串以`NULL`标识结尾。 `len` 指定可以返回的字符串的最大长度。

### sudrvIpcCloseMemHandle

尝试关闭映射的设备内存。

**函数签名**

```cpp
suError_t sudrvIpcCloseMemHandle(suDeviceptr_t devPtr);
```

**参数列表**

- `devPtr` [in]：要关闭的由`suIpcOpenMemHandle` 返回的设备指针

**返回值**

- `suSuccess`
- `suErrorNotSupported`
- `suErrorInvalidValue`

**描述**

尝试关闭使用 `suIpcOpenMemHandle` 映射的设备内存。


### sudrvIpcGetEventHandle

获取先前分配的事件的进程间句柄。

**函数签名**

```cpp
```

**参数列表**

- `handle` [out]： 指向用户分配的 `suIpcEventHandle` 的指针，在其中返回句柄
- `event` [in]：指定要获取的事件句柄。

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`
- `suErrorNotSupported`
- `suErrorMemoryAllocation`

**描述**

获取先前分配的事件的进程间句柄，在`*handle`中返回。



### sudrvIpcGetMemHandle

获取现有设备内存分配的进程间内存句柄。

**函数签名**

```cpp
suError_t sudrvIpcGetMemHandle(suIpcMemHandle_t *handle, suDeviceptr_t devPtr);
```

**参数列表**

- `handle` [out]：指向用户分配的 `suIpcMemHandle` 的指针以返回句柄。
- `devPtr` [in]：设备内存地址

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`
- `suErrorNotSupported`
- `suErrorMemoryAllocation`

**描述**

获取现有设备内存`devPtr`的进程间内存句柄。在`*handle`中返回。



### sudrvIpcOpenEventHandle

打开进程间事件句柄以供当前进程使用。

**函数签名**

```cpp
suError_t sudrvIpcOpenEventHandle(suEvent_t *event, suIpcEventHandle_t handle);
```

**参数列表**

- `event` [out]： 返回导入的事件
- `handle` [in]：打开进程间句柄

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`
- `suErrorNotSupported`
- `suErrorMemoryAllocation`

**描述**

打开进程间事件句柄`handle`指定的事件以供当前进程使用。事件在`*event`中返回。


### sudrvIpcOpenMemHandle

打开从另一个进程导出的进程间内存句柄，并返回可在当前API所在的进程中使用的设备指针。

**函数签名**

```cpp
suError_t sudrvIpcOpenMemHandle(suDeviceptr_t *devPtr, suIpcMemHandle_t handle,

                                unsigned int flags);
```

**参数列表**

- `devPtr` [out]：返回的设备指针
- `handle` [in]： 需要打开的`suIpcMemHandle` 句柄
- `flags`[in]：此操作的标志。必须指定为 `suIpcMemLazyEnablePeerAccess`的枚举值

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`
- `suErrorNotSupported`
- `suErrorMemoryAllocation`

**描述**

打开从另一个进程导出的进程间内存句柄`handle`，并返回可在当前API所在的进程中使用的设备指针`*devPtr`。


### sudrvMallocDevice

分配设备内存。

**函数签名**

```cpp
suError_t sudrvMallocDevice(suDeviceptr_t *devPtr, size_t size);
```

**参数列表**

- `devPtr`[out]：  指向分配的设备内存的指针
- `size`[in]： 请求的分配大小（以字节为单位）

**返回值**

- `suSuccess`
- `suErrorMemoryAllocation`
- `suErrorInvalidValue`

**描述**

在`*devPtr` 返回在设备上分配的`size`大小的内存。如果分配失败则返回 `suErrorMemoryAllocation`。

> 该 API 不会对分配到的内存进行清零操作。


### sudrvMallocHost

在主机上分配页锁定内存。

**函数签名**

```cpp
suError_t sudrvMallocHost(void **ptr, size_t size,
                          unsigned int flags __dv(suMallocHostDefault));
```

**参数列表**

- `ptr`[out]：指向分配的主机内存的指针
- `size`[in]： 请求的分配大小（以字节为单位）
- `flags`[in]：标志参数

**返回值**

- `suSuccess`
- `suErrorMemoryAllocation`
- `suErrorInvalidValue`

**描述**

在主机上分配`size`大小的主机内存并在`*ptr`中返回，同时为这一块内存在设备上做页锁定使得这块内存能被设备访问。

> 注意：当设备访问主机锁页内存时，可能导致主机性能降低，建议谨慎使用该函数来为设备和主机之间的数据交换分配空间。


### sudrvMallocDevicePitch

在设备上分配pitch内存。

**函数签名**

```cpp
suError_t sudrvMallocDevicePitch(suDeviceptr_t *devPtr, size_t *pitch,
                                 size_t width, size_t height,
                                 unsigned int elementSizeBytes);
```

**参数列表**

- `devPtr`[out]：指向分配的pitch设备内存的指针
- `pitch`[out]：pitch值
- `width`[in]：请求的pitch设备内存宽度（以字节为单位）
- `height`[in]：请求的pitch设备内存高度

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorMemoryAllocation`

**描述**

在`*devPtr`中返回在设备上分配至少`width * height` 字节的线性内存的地址，并在 `*pitch` 中返回分配的宽度的pitch大小（以字节为单位）。该函数可以用于分配符合硬件对其要求的`2D`数据空间，分配后`2D`数据元素的地址计算公式如下：

`T* pElement = (T*)((char*)BaseAddress + Row * pitch) + Column`

对于`2D` 数组的分配，建议使用 `suMallocDevicePitch()`分配空间，这样可以在操作数据时更符合硬件的对其要求，可以加速数据拷贝等操作。


### sudrvMemcpy

在主机和设备之间复制数据。

**函数签名**

```cpp
suError_t sudrvMemcpy(suDeviceptr_t dst, suDeviceptr_t src, size_t size);
```

**参数列表**

- `dst`[in]：目标内存地址
- `src`[in]：源内存地址
- `size`[in]： 待复制的数据的大小（以字节为单位）

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidMemoryDirection`

**描述**

将 `src` 指向的内存区域的`size`字节数据复制到 `dst` 指向的内存区域。

### sudrvMemcpy2D

在主机和设备之间复制数据。

**函数签名**

```cpp
suError_t sudrvMemcpy2D(const suMemcpy2DDesc *copy);
```

**参数列表**

- `*copy`[in]：`2D`数据拷贝参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

将矩阵（高度为`height`，每行的宽度为`width`字节）从 `src` 指向的内存区域复制到 `dst` 指向的内存区域。

`dpitch` 和 `spitch` 是 `dst` 和 `src` 指向的 `2D` 数组的包括了padding的内存宽度（以字节为单位）。

### sudrvMemcpy2DAsync

异步方式在主机和设备之间复制数据。

**函数签名**

```cpp
suError_t sudrvMemcpy2DAsync(const suMemcpy2DDesc *copy, suStream_t stream);
```

**参数列表**

- `copy`[in]：`2D`数据拷贝参数
- `stream`[in]：执行操作的流

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

异步版本的`sudrvMemcpy2D`。

### sudrvMemcpy2DUnaligned

在主机和设备之间复制非对齐的数据。

**函数签名**

```cpp
suError_t sudrvMemcpy2DUnaligned(const suMemcpy2DDesc *copy);
```

**参数列表**

- `copy`[in]：`2D`数据拷贝参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

拷贝`2D`数据，自动对地址做对齐。

### sudrvMemcpy3D

复制`3D`数据。

**函数签名**

```cpp
suError_t sudrvMemcpy3D(const suMemcpy3DDesc *copy);
```

**参数列表**

- `copy`[in]：`3D`内存复制参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidPitchValue`
- `suErrorInvalidMemoryDirection`

**描述**

在由`suMemcpy3DDesc`描述的两个`3D`对象之间复制数据。


### sudrvMemcpy3DAsync

在 `3D` 对象之间复制数据。

**函数签名**

```cpp
suError_t sudrvMemcpy3DAsync(const suMemcpy3DDesc *copy, suStream_t stream);
```

**参数列表**

- `copy`[in]：`3D`内存复制参数
- `stream`[in]：执行操作的流

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidPitchValue`
- `suErrorInvalidMemoryDirection`

**描述**

在由`suMemcpy3DDesc`描述的两个`3D`对象之间复制数据。


### sudrvMemcpy3DPeer

在设备之间复制`3D`对象数据。

**函数签名**

```cpp
suError_t sudrvMemcpy3DPeer(const suMemcpy3DPeerDesc *copy);
```

**参数列表**

- `copy`[in]：`3D`内存复制参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidPitchValue`
- `suErrorInvalidMemoryDirection`
- `suErrorInvalidDevice`

**描述**

在由`suMemcpy3DPeerDesc`描述的两个`3D`对象之间复制数据。
两个`3D`对象分别属于不同的设备。

### sudrvMemcpy3DPeerAsync

在设备之间异步复制内存。

**函数签名**

```cpp
suError_t sudrvMemcpy3DPeerAsync(const suMemcpy3DPeerDesc *copy,
                                 suStream_t stream);
```

**参数列表**

- `copy`[in]：`3D`内存复制参数
- `stream`[in]：执行操作的流

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidPitchValue`
- `suErrorInvalidMemoryDirection`
- `suErrorInvalidDevice`

**描述**

在由`suMemcpy3DPeerDesc`描述的两个`3D`对象之间异步的复制数据。
两个`3D`对象分别属于不同的设备。

### sudrvMemcpyAsync

在主机和设备之间复制数据。

**函数签名**

```cpp
suError_t sudrvMemcpyAsync(suDeviceptr_t dst, suDeviceptr_t src, size_t size,
                           suStream_t stream);
```

**参数列表**

- `dst`[in]：目标内存地址
- `src`[in]： 源存储器地址
- `size`[in]：待复制的数据的大小（以字节为单位）
- `stream`[in]：执行操作的流句柄

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidMemoryDirection`

**描述**

和`sudrvMemcpy()`相比是`sudrvMemcpyAsync()`异步执行复制动作，即该API不会阻塞等待复制完成就立即返回。


### sudrvMemcpyDtoD

在设备和设备之间复制数据。

**函数签名**

```cpp
suError_t sudrvMemcpyDtoD(suDeviceptr_t dstDevice, suDeviceptr_t srcDevice,
                          size_t size);
```

**参数列表**

- `dstDevice`[in]：目标内存地址
- `srcDevice`[in]： 源存储器地址
- `size`[in]：待复制的数据的大小（以字节为单位）

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidMemoryDirection`

**描述**

从设备地址`srcDevice`拷贝大小`size`的数据到另一个设备的地址`dstDevice`。

### sudrvMemcpyDtoDAsync

在设备和设备之间复制数据。

**函数签名**

```cpp
suError_t sudrvMemcpyDtoDAsync(suDeviceptr_t dstDevice, suDeviceptr_t srcDevice,
                               size_t size, suStream_t stream);
```

**参数列表**

- `dstDevice`[in]：目标内存地址
- `srcDevice`[in]： 源存储器地址
- `size`[in]：待复制的数据的大小（以字节为单位）
- `stream`[in]：执行操作的流

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidMemoryDirection`

**描述**

异步的在流`stream`上从设备地址`srcDevice`拷贝大小`size`的数据到另一个设备的地址`dstDevice`。


### sudrvMemcpyDtoH

从设备复制数据到主机。

**函数签名**

```cpp
suError_t sudrvMemcpyDtoH(void *dstHost, suDeviceptr_t srcDevice, size_t size);
```

**参数列表**

- `dstHost`[in]：主机目的地址
- `srcDevice`[in]：源设备地址
- `size`[in]：待复制的数据的大小（以字节为单位）

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

从设备地址`srcDevice`拷贝大小`size`的数据到主机地址`dstHost`。

### sudrvMemcpyDtoHAsync

从设备复制数据到主机。

**函数签名**

```cpp
suError_t sudrvMemcpyDtoHAsync(void *dstHost, suDeviceptr_t srcDevice,
                               size_t size, suStream_t stream);
```

**参数列表**

- `dstHost`[in]：主机目的地址
- `srcDevice`[in]：源设备地址
- `size`[in]：待复制的数据的大小（以字节为单位）
- `stream`[in]：执行操作的流

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

异步的在流`stream`上从设备地址`srcDevice`拷贝大小`size`的数据到主机地址`dstHost`。


### sudrvMemcpyPeerAsync

在两个不同设备的上下文之间异步复制内存。

**函数签名**

```cpp
suError_t sudrvMemcpyPeerAsync(suDeviceptr_t dstDevice, suContext dstContext,
                               suDeviceptr_t srcDevice, suContext srcContext,
                               size_t count, suStream_t stream);
```

**参数列表**

- `dstDevice`[in]：目标内存地址
- `dstContext`[in]：目标上下文
- `srcDevice`[in]：源设备指针
- `srcContext`[in]：源上下文
- `count`[in]：复制大小（以字节为单位）
- `stream`[in]：执行操作的流句柄

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidDevice`

**描述**

这是`sudrvMemcpyPeer()`函数的异步版本，该函数不会阻塞执行复制操作而是立即返回。

> 描述参考 `sudrvMemcpyPeer()`

### sudrvFree

释放设备上的内存。

**函数签名**

```cpp
suError_t sudrvFree(suDeviceptr_t ptr);
```

**参数列表**

- `ptr`[in]：设备内存地址

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

释放 `ptr` 指向的内存空间，该内存空间必须由之前调用以下内存分配 API 之一返回

- `suMallocDevice()`
- `suMallocDevicePitch()`
- `suMallocHost()`
- `sudrvMallocDevice()`
- `sudrvMallocDevicePitch()`
- `sudrvMallocHost()`

如果重复释放同一个`ptr`， 则返回 `suErrorValue`。
如果 `ptr` 为 `0`，则不执行任何操作且返回`suSuccess`。


### sudrvMemGetAddressRange

查询设备地址信息。

**函数签名**

```cpp
suError_t sudrvMemGetAddressRange(suDeviceptr_t *base, size_t *size,
                                  suDeviceptr_t devPtr);
```

**参数列表**

- `base`[out]：返回基地址
- `size`[out]：返回大小
- `devPtr`[in]：要查询的设备地址
**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

查询设备地址`devPtr`所在的设备内存分配基地址`*base`和所分配的大小`*size`。


### sudrvMemGetInfo

获取可用内存和总设备内存。

**函数签名**

```cpp
suError_t sudrvMemGetInfo(size_t *free, size_t *total);
```

**参数列表**

- `free`[out]：返回的可用内存的大小（以字节为单位）
- `total`[out]：返回总内存的大小（以字节为单位）

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*total`中返回当前上下文可用的内存总量。在`*free` 中返回设备上可用的内存量。


### sudrvMallocHost

在主机上分配页锁定内存。


**函数签名**

```cpp
suError_t sudrvMallocHost(void **ptr, size_t size,
                          unsigned int flags __dv(suMallocHostDefault));
```

**参数列表**

- `ptr`[out]：指向分配的主机内存的指针
- `size`[in]： 请求的分配大小（以字节为单位）
- `flags`[in]：标志参数

**返回值**

- `suSuccess`
- `suErrorMemoryAllocation`
- `suErrorInvalidValue`

**描述**

在主机上分配`size`大小的主机内存并在`*ptr`中返回，同时为这一块内存在设备上做页锁定使得这块内存能被设备访问。

> 注意：当设备访问主机锁页内存时，可能导致主机性能降低，建议谨慎使用该函数来为设备和主机之间的数据交换分配空间。

### sudrvMemHostGetDevicePointer

查询锁页内存的设备指针。

**函数签名**

```cpp
suError_t sudrvMemHostGetDevicePointer(suDeviceptr_t *devPtr, void *hostPtr,
                                       unsigned int flags);
```

**参数列表**

- `devPtr`[out]：返回设备地址
- `hostPtr`[in]：锁页内存地址
- `flags`[in]：标志参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**
查询锁页内存`hostPtr`的设备指针，在`*devPtr`中返回。


### sudrvMemHostGetFlags

返回用于 `sudrvMallocHost` 或`suMallocHost` 分配的固定主机内存的标志。

**函数签名**

```cpp
suError_t sudrvMemHostGetFlags(unsigned int *flags, void *ptr);
```

**参数列表**

- `flags`[out]：返回标志
- `hostPtr`[in]：需要查询的主机指针

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

如果输入指针`ptr`不在  `sudrvMallocHost` 或`suMallocHost` 分配的地址范围内,则`sudrvMemHostGetFlags()`将返回
`suErrorInvalidValue`。


### sudrvRegisterHostMemory

注册现有主机内存以供 `BIRENSUPA` 使用。

**函数签名**

```cpp
suError_t sudrvRegisterHostMemory(void *ptr, size_t size, unsigned int flags);
```

**参数列表**

- `ptr`[in]：需要锁定的主机内存地址
- `size`[in]：地址范围的大小(以字节为单位)
- `flags`[in]：注册请求的标志

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorMemoryAllocation`
- `suErrorNotSupported`
- `suErrorHostMemoryAlreadyRegisted`

**描述**

页锁定由`ptr`和`size`指定的内存范围，并将其映射到 `flags` 指定的设备。此内存范围也被添加到与 `sudrvMallocHost()` 相同的跟踪机制中，以自动加速对 `sudrvMemcpy()`等函数的调用。

> 注意：虽然设备可以直接访问锁页内存，但是设备访问主机锁页主机的内存性能与访问设备内存相比会有所降低，最好谨慎使用该函数来为主机和设备之间的数据交换注册内存空间。


### sudrvUnregisterHostMemory

注销使用 `sudrvRegisterHostMemory` 注册的内存范围。

**函数签名**

```cpp
suError_t sudrvUnregisterHostMemory(void *ptr);
```

**参数列表**

- `ptr`[in]： 需要注销锁定的主机内存地址

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorHostMemoryNotRegistered`

**描述**

取消基址`ptr`指定的内存范围的映射。
基地址必须与 `sudrvRegisterHostMemory()` 时的地址相同。

### sudrvMemsetD16

将设备内存初始化或设置为一个值。

**函数签名**

```cpp
suError_t sudrvMemsetD16(suDeviceptr_t devPtr, unsigned short value, size_t n);
```

**参数列表**

- `devPtr`[in]：要初始化的地址
- `value`[in]：要设置的16位的值
- `n`[in]：16位值的个数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

用常量值`value`填充`devPtr` 指向的内存区域的`n`个16位数据。

### sudrvMemsetD16Async

将设备内存初始化或设置为一个值。

**函数签名**

```cpp
suError_t sudrvMemsetD16Async(suDeviceptr_t devPtr, unsigned short value,
                              size_t n, suStream_t stream);
```

**参数列表**

- `devPtr`[in]：要初始化的地址
- `value`[in]：要设置的16位的值
- `n`[in]：16位值的个数
- `stream`[in]：执行操作的流

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在流`stream`上异步的用常量值`value`填充`devPtr` 指向的内存区域的`n`个16位数据。

### sudrvMemsetD2D16

将设备内存初始化或设置为一个值。


**函数签名**

```cpp
suError_t sudrvMemsetD2D16(suDeviceptr_t devPtr, size_t dstPitch,
                           unsigned short value, size_t width, size_t height);
```

**参数列表**

- `devPtr`[in]：要初始化的地址
- `dstPitch`[in]：目标地址的pitch大小
- `value`[in]：要设置的16位的值
- `width`[in]：每行16位值的个数
- `height`[in]：高度

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

用常量值`value`填充`devPtr` 指向的`2D`内存区域的`width * height`个16位数据，每行数据大小做512字节对齐后的pitch值为`dstPitch`。

### sudrvMemsetD2D16Async

将设备内存初始化或设置为一个值。


**函数签名**

```cpp
suError_t sudrvMemsetD2D16Async(suDeviceptr_t devPtr, size_t dstPitch,
                                unsigned short value, size_t width,
                                size_t height, suStream_t stream);
```

**参数列表**

- `devPtr`[in]：要初始化的地址
- `dstPitch`[in]：目标地址的pitch大小
- `value`[in]：要设置的16位的值
- `width`[in]：每行16位值的个数
- `height`[in]：高度
- `stream`[in]：执行操作的流

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在流`stream`上异步的用常量值`value`填充`devPtr` 指向的`2D`内存区域的`width * height`个16位数据，每行数据大小做512字节对齐后的pitch值为`dstPitch`。

### sudrvMemsetD2D32

将设备内存初始化或设置为一个值。

**函数签名**

```cpp
suError_t sudrvMemsetD2D32(suDeviceptr_t devPtr, size_t dstPitch,
                           unsigned int value, size_t width, size_t height);
```

**参数列表**

- `devPtr`[in]：要初始化的地址
- `dstPitch`[in]：目标地址的pitch大小
- `value`[in]：要设置的32位的值
- `width`[in]：每行32位值的个数
- `height`[in]：高度

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

用常量值`value`填充`devPtr` 指向的`2D`内存区域的`width * height`个32位数据，每行数据大小做512字节对齐后的pitch值为`dstPitch`。


### sudrvMemsetD2D32Async

将设备内存初始化或设置为一个值。


**函数签名**

```cpp
suError_t sudrvMemsetD2D32Async(suDeviceptr_t devPtr, size_t dstPitch,
                                unsigned int value, size_t width, size_t height,
                                suStream_t stream);
```

**参数列表**

- `devPtr`[in]：要初始化的地址
- `dstPitch`[in]：目标地址的pitch大小
- `value`[in]：要设置的32位的值
- `width`[in]：每行32位值的个数
- `height`[in]：高度
- `stream`[in]：执行操作的流

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在流`stream`上异步的用常量值`value`填充`devPtr` 指向的`2D`内存区域的`width * height`个32位数据，每行数据大小做512字节对齐后的pitch值为`dstPitch`。

### sudrvMemsetD2D8

将设备内存初始化或设置为一个值。

**函数签名**

```cpp
suError_t sudrvMemsetD2D8(suDeviceptr_t devPtr, size_t dstPitch,
                          unsigned char value, size_t width, size_t height);
```

**参数列表**

- `devPtr`[in]：要初始化的地址
- `dstPitch`[in]：目标地址的pitch大小
- `value`[in]：要设置的8位的值
- `width`[in]：每行8位值的个数
- `height`[in]：高度

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

用常量值`value`填充`devPtr` 指向的`2D`内存区域的`width * height`个8位数据，每行数据大小做512字节对齐后的pitch值为`dstPitch`。

### sudrvMemsetD2D8Async

将设备内存初始化或设置为一个值。

**函数签名**

```cpp
suError_t sudrvMemsetD2D8Async(suDeviceptr_t devPtr, size_t dstPitch,
                               unsigned char value, size_t width, size_t height,
                               suStream_t stream);
```

**参数列表**

- `devPtr`[in]：要初始化的地址
- `dstPitch`[in]：目标地址的pitch大小
- `value`[in]：要设置的8位的值
- `width`[in]：每行8位值的个数
- `height`[in]：高度
- `stream`[in]：执行操作的流

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在流`stream`上异步的用常量值`value`填充`devPtr` 指向的`2D`内存区域的`width * height`个8位数据，每行数据大小做512字节对齐后的pitch值为`dstPitch`。


### sudrvMemsetD32

将设备内存初始化或设置为一个值。

**函数签名**

```cpp
suError_t sudrvMemsetD32(suDeviceptr_t devPtr, unsigned int value, size_t n);
```

**参数列表**

- `devPtr`[in]：要初始化的地址
- `value`[in]：要设置的32位的值
- `n`[in]：32位值的个数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

用常量值`value`填充`devPtr` 指向的内存区域的`n`个32位数据。

### sudrvMemsetD32Async

将设备内存初始化或设置为一个值。

**函数签名**

```cpp
suError_t sudrvMemsetD32Async(suDeviceptr_t devPtr, unsigned int value,

                              size_t n, suStream_t stream);
```

**参数列表**

- `devPtr`[in]：要初始化的地址
- `value`[in]：要设置的32位的值
- `n`[in]：32位值的个数
- `stream`[in]：执行操作的流

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在流`stream`上异步的用常量值`value`填充`devPtr` 指向的内存区域的`n`个32位数据。


### sudrvMemsetD8

将设备内存初始化或设置为一个值。

**函数签名**

```cpp
suError_t sudrvMemsetD8(suDeviceptr_t devPtr, unsigned char value, size_t n);
```

**参数列表**

- `devPtr`[in]：要初始化的地址
- `value`[in]：要设置的8位的值
- `n`[in]：8位值的个数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

用常量值`value`填充`devPtr` 指向的内存区域的`n`个8位数据。


### sudrvMemsetD8Async

将设备内存初始化或设置为一个值。

**函数签名**

```cpp
suError_t sudrvMemsetD8Async(suDeviceptr_t devPtr, unsigned char value,
                             size_t n, suStream_t stream);
```

**参数列表**

- `devPtr`[in]：要初始化的地址
- `value`[in]：要设置的8位的值
- `n`[in]：8位值的个数
- `stream`[in]：执行操作的流

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在流`stream`上异步的用常量值`value`填充`devPtr` 指向的内存区域的`n`个8位数据。

##  统一地址

### sudrvPointerGetAttribute

查询指针属性。

**函数签名**

```cpp
suError_t sudrvPointerGetAttribute(void *data, suPointerAttribute attribute,
                                   suDeviceptr_t ptr);
```

**参数列表**

- `data`[out]：返回指针属性值
- `attribute`[in]：要查询的属性
- `ptr`[in]：要查询的设备指针

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*data`中返回`ptr`指针的`attribute`属性的值。


### sudrvPointerGetAttributes

查询指针的多个属性。

**函数签名**

```cpp
suError_t sudrvPointerGetAttributes(unsigned int numAttributes,
                                    suPointerAttribute *attributes, void **data,
                                    suDeviceptr_t ptr);
```

**参数列表**

- `numAttributes`[in]：属性数量
- `attributes`[in]：要查询的属性数组
- `data`[out]：返回指针属性值数组
- `ptr`[in]：要查询的设备指针

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*data`中返回`ptr`指针的`attributes`数组中`numAttributes`个属性的值。


### sudrvPointerSetAttribute

设定指针属性。

**函数签名**

```cpp
suError_t sudrvPointerSetAttribute(const void *value,
                                   suPointerAttribute attribute,
                                   suDeviceptr_t ptr);
```

**参数列表**

- `value`[in]：要设定的值
- `attribute`[in]：要设定的属性
- `ptr`[in]：要更新属性的设备指针

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*value`中的值更新`ptr`指针的`attribute`属性的值。


## 流管理

### sudrvStreamAddCallback

向计算流添加回调函数。

**函数签名**

```cpp
suError_t sudrvStreamAddCallback(suStream_t stream, suStreamCallback_t callback,
                                 void *userData, unsigned int flags);
```

**参数列表**

- `stream`[in]：要添加回调的流
- `callback`[in]：回调函数
- `userData`[in]：要传递给回调函数的用户指定数据
- `flags`[in]：保留以备将来使用，必须为`0`

**返回值**

- `suSuccess`
- `suErrorInvalidResourceHandle`
- `suErrorInvalidValue`
- `suErrorNotSupported`

**描述**

添加一个回调函数到流中，该回调函数在流中排队等待它前面的任务完成后在主机上被调用。对于每一次 `sudrvStreamAddCallback` 调用，其指定的回调函数将只被执行一次。回调函数会阻止流中的后续工作，直到完成它执行完才开始执行，即回调函数的执行具有流的语义。

> 在回调函数内部，不允许调用任何 BIRENSUPA API。

### sudrvStreamBeginCapture

在流上开启捕获并保存为计算图。

**函数签名**

```cpp
suError_t sudrvStreamBeginCapture(suStream_t stream, suStreamCaptureMode mode);
```

**参数列表**

- `stream`[in]：要启动捕获的流
- `mode`[in]：控制此捕获序列与其他可能不安全的 API 调用的交互，可以是：
 	- `suStreamCaptureModeGlobal`
 	- `suStreamCaptureModeThreadLocal`
 	- `suStreamCaptureModeRelaxed`

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

开始在 `stream` 上捕获任务并生成任务图，该任务图将通过 `sudrvStreamEndCapture()`返回。可以通过`suStreamIsCapturing()`查询一个`suStreamLegacy`的`stream`是否在捕捉模式。可以通过`sudrvStreamGetCaptureInfo()`查询到当前在捕获中的任务图和捕获`id`。捕获必须在启动它的同一个流上结束，并且只有当流尚未启动时才可以启动捕获 。
> 如果 `mode` 不是 `suStreamCaptureModeRelaxed`，则必须从同一线程操作此捕获中的流。

> 当流处于捕获模式时，推送到流中的所有操作都**不会被执行**，而是会被捕获。


### sudrvStreamCreateWithFlags

用指定标志创建异步流。

**函数签名**

```cpp
suError_t sudrvStreamCreateWithFlags(suStream_t *stream, unsigned int flags);
```

**参数列表**

- `stream`[out]： 指向新创建流句柄的指针
- `flags`[in]：流创建参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

使用指定的标志参数创建流，支持的流标志可以是：

- `suStreamDefault`：默认流创建标志
- `suStreamNonBlocking`：指定创建的流是非阻塞的，可以和默认流 `0`（NULL 流）并行工作，即创建的流不与流 `0` 执行隐式同步。


### sudrvStreamCreateWithPriority

创建具有指定优先级的异步流。

**函数签名**

```cpp
suError_t sudrvStreamCreateWithPriority(suStream_t *stream, unsigned int flags,
                                        int priority);
```

**参数列表**

- `stream`[out]： 指向新创建的流句柄的指针
- `flags`[in]：流创建参数
- `priority`[in]：流的优先级。

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

> 在壁仞通用 GPU 硬件设计版本 1.0 上**不可用**。


### sudrvStreamDestroy

清理并销毁异步流。

**函数签名**

```cpp
suError_t sudrvStreamDestroy(suStream_t stream);
```

**参数列表**

- `stream`[in]：要销毁的流句柄

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`

**描述**

清理并销毁`stream`指定的异步流。
如果调用`suStreamDestroy()`时设备仍在流 `stream` 中工作，该函数将阻塞直到`stream`完成所有工作后再返回。



### sudrvStreamEndCapture

结束流上的捕获，返回捕获的任务图。

**函数签名**

```cpp
suError_t sudrvStreamEndCapture(suStream_t stream, suTaskGraph_t *graph);
```

**参数列表**

- `stream`[in]：要结束的流句柄
- `graph`[out]：捕获的任务图句柄

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorStreamCaptureWrongThread`

**描述**

结束`stream`上的捕获，通过`*graph`返回捕获的任务图。必须已在 `stream` 上通过调用 `sudrvStreamBeginCapture()`启动捕获。如果由于违反流捕获规则而使捕获无效，则将返回 `NULL` 图。

如果`sudrvStreamBeginCapture()`的 `mode` 参数不是 `suStreamCaptureModeRelaxed`，则必须在调用 `sudrvStreamBeginCapture()` 的线程中调用 `sudrvStreamEndCapture()`。



### sudrvStreamGetCaptureInfo

查询流的捕获状态。

**函数签名**

```cpp
suError_t sudrvStreamGetCaptureInfo(suStream_t stream,
                                 suStreamCaptureStatus *captureStatus,
                                 unsigned long long *id);
```

**参数列表**

- `stream`[in]：要查询的流句柄
- `captureStatus`[out]：返回流的捕获状态
- `id`[out]：返回捕获序列的唯一ID

**返回值**

- `suSuccess`
- `suErrorStreamCaptureImplicit`

**描述**

查询流的捕获状态并获取表示进程生命周期内的捕获序列的唯一ID。

> 注意：此 API 有更高版本： `sudrvStreamGetCaptureInfo_v2()`，并将在后续版本中被弃用。当前版本保留此 API 是为了方便从之前的 CUDA 代码迁移至 BIRENSUPA。。

如果在捕获的流不是使用 `sudrvStreamNonBlocking`所创建时调用`suStreamLegacy`（“空流”），则返回 `suErrorStreamCaptureImplicit`。

仅当以下两个条件都满足才会返回有效的`id`：

- 函数调用返回`suSuccess`
- `*captureStatus`设置为 `suStreamCaptureStatusActive`



### sudrvStreamGetContext

查询和流管理的上下文。

**函数签名**

```cpp
suError_t sudrvStreamGetContext(suStream_t stream, suContext *context);
```

**参数列表**

- `stream`[in]：要查询的流
- `context`[out]：返回关联的上下文

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*context`中返回`stream`创建时所关联的上下文。


### sudrvStreamGetFlags

查询流的标志。

**函数签名**

```cpp
suError_t sudrvStreamGetFlags(suStream_t stream, unsigned int *flags);
```

**参数列表**

- `stream`[in]：要查询的流的句柄
- `flags`[out]：指向返回流标志的`unsigned int`的指针

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`

**描述**

查询流的标志。标志在 `*flags` 中返回。

> 请参阅 `sudrvStreamCreateWithFlags()`以获取有效标志的列表。

### sudrvStreamGetPriority

查询流的优先级。

**函数签名**

```cpp
suError_t sudrvStreamGetPriority(suStream_t stream, int *priority);
```

**参数列表**

- `stream`[in]：要查询的流的句柄
- `priority`[out]：指向有符号整数的指针，其中返回流的优先级

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`

**描述**

> 壁仞通用 GPU 硬件设计版本 1.0 只有优先级 `0`。


### sudrvStreamIsCapturing

返回流的捕获状态。

**函数签名**

```cpp
suError_t sudrvStreamIsCapturing(suStream_t stream,
                                 suStreamCaptureStatus *captureStatus);
```

**参数列表**

- `stream`[in]：要查询的流的句柄
-  `captureStatus`[out]：返回流的捕获状态

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`
- `suErrorStreamCaotureImplicit`

**描述**

通过`*captureStatus`返回`stream`的捕获状态。成功调用后，`*captureStatus` 将是下列状态的一种：

- `suStreamCaptureStatusNone`：流不在捕获状态。
- `suStreamCaptureStatusActive` ：流正在捕获中。
- `suStreamCaptureStatusInvalidated` ：流正在捕获，但发生了错误使捕获序列无效。必须关闭流的捕获 ，以便继续使用`stream`。

> 请注意，
>
> 1. 如果调用此函数使用的`stream`为旧流(即空流)而且在同一设备上有阻塞流处于捕获状态，它将返回`suErrorStreamCaptureImplicit` 同时`*captureStatus`的值无意义。
> 2. 当阻塞流捕获时，旧流处于不可用状态，直到阻塞流捕获终止。
> 3. 流捕获不支持旧流。


### sudrvStreamQuery

查询异步流的完成状态。

**函数签名**

```cpp
suError_t sudrvStreamQuery(suStream_t stream);
```

**参数列表**

- `stream`[in]：要查询流的句柄

**返回值**

- `suSuccess`
- `suErrorNotReady`
- `suErrorInvalidResourceHandle`

**描述**

如果 `stream` 中的所有操作均已完成，则返回 `suSuccess`；否则返回 `suErrorNotReady`。

> 返回 `suSuccess`相当于调用了`sudrvStreamSynchronize()`。



### sudrvStreamSynchronize

主机线程同步等待流任务完成。

**函数签名**

```cpp
suError_t sudrvStreamSynchronize(suStream_t stream);
```

**参数列表**

- `stream`[in]：需要同步的流的句柄

**返回值**

- `suSuccess`
- `suErrorInvalidResourceHandle`
- `suErrorIllegalState`

**描述**

主机线程和`stream`同步。即调用此API的主机线程将阻塞，直到流完成所有任务再返回。


### sudrvStreamWaitEventWithFlags

让GPU上的流等待一个事件。

**函数签名**

```cpp
suError_t sudrvStreamWaitEventWithFlags(suStream_t stream, suEvent_t event,
                                        unsigned int flags);
```

**参数列表**

- `stream`[in]：等待事件的流的句柄
- `event`[in]：要等待的事件的句柄
- `flags`[in]：额外的参数，参见描述

**返回值**

- `suSuccess`
- `suErrorInvalidResourceHandle`
- `suErrorInvalidValue`

**描述**

1. 让`stream`上后续提交的任务都等待`event`所捕获的所有任务。有关事件捕获内容的详细信息，请参阅 `sudrvEventRecord()`。
2. 标志`flags`包括：
 - `suEventWaitDefault`：默认事件创建标志。
 - `suEventWaitExternal`：在捕获任务图时事件作为外部事件节点显式的添加进任务图。

> 这里所说的**等待**发生在设备端，本API的调用是立即返回的，不会等待。



### sudrvThreadExchangeStreamCaptureMode

为主机线程替换新捕获模式

**函数签名**

```cpp
suError_t sudrvThreadExchangeStreamCaptureMode(suStreamCaptureMode *mode);
```

**参数列表**

- `mode`[in]：要替换的新模式

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

将调用线程的流捕获交互模式设置为 `*mode` 中包含的值，并在`*mode`中返回先前模式。


### sudrvStreamCopyAttributes

将源流的属性复制到目标流。


**函数签名**

```cpp
suError_t sudrvStreamCopyAttributes(suStream_t dst, suStream_t src);
```

**参数列表**

- `dst`[in]：目标流
- `src`[in]：源流

**返回值**

- `suSuccess`
- `suErrorNotSupported`

**描述**

在**相同**的上下文中的两个流之间将源流`src`的属性复制到目标流 `dst`。

当前支持的流属性类型有：

- `suLaunchAttributeSpcMask` ：流作用域的`SPC` 掩码

>如果只调用Runtime API或者没有使用Driver API创建用户上下文，那么同一个设备上的两个流属于同一上下文。

### sudrvStreamGetAttribute

查询流的相关属性。

**函数签名**

```cpp
suError_t sudrvStreamGetAttribute(suStream_t stream, suStreamAttrId attr,
                                  suStreamAttrValue *valueOut);
```

**参数列表**

- `stream`[in]：要查询的流的句柄
- `attr`[in]：要查询的属性
- `valueOut`[out]：返回查询到的属性值

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`

**描述**

从`stream`中查询属性`attr`并将其存储在`*valueOut`的相应成员中。

流的属性类型`attr`当前支持的有：

- `suLaunchAttributeSpcMask` ：流作用域的`SPC` 掩码


### sudrvStreamGetCaptureInfo_v2

查询流的捕获状态

**函数签名**

```cpp
suError_t sudrvStreamGetCaptureInfo_v2(suStream_t stream,
                                       suStreamCaptureStatus *captureStatus,
                                       unsigned long long *id,
                                       suTaskGraph_t *graph,
                                       const suTaskGraphNode_t **dependencies,
                                       size_t *numDependencies);
```

**参数列表**

- `stream`[in]：要查询的流
- `captureStatus`[out]：返回流的捕获状态的指针；必需参数不能为空值
- `id`[out]：用于返回捕获序列识别码，识别码在进程的生命周期中是唯一的，传空指针则不返回
- `graph`[out]： 返回正在捕获的任务图句， 可选空指针则不返回
- `dependencies`[out]：存储指向节点数组的指针的可选指针
- `numDependencies`[out]：`dependencies` 中返回的数组大小的可选指针

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorStreamCaptureImplicit`

**描述**

查询流的捕获状态并获取在进程生命周期内表示捕获序列的唯一ID。

如果在捕获的流不是使用 `suStreamNonBlocking`所创建时调用`suStreamLegacy`（“空流”），则返回 `suErrorStreamCaptureImplicit`。

仅当以下两个条件都满足才会返回有效的`id`：

- 函数调用返回`suSuccess`
- `*captureStatus`设置为 `suStreamCaptureStatusActive`

### sudrvStreamSetAttribute

 设置流属性。
 
**函数签名**

```cpp
suError_t sudrvStreamSetAttribute(suStream_t stream, suStreamAttrId attr,
                                  const suStreamAttrValue *value);
```

**参数列表**

- `stream`[in]：要设置的流的句柄
- `attr`[in]：要设置的属性类型
- `value`[in]：要设置的属性值

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`

**描述**

根据`*value`的相应属性在 `stream` 上设置属性 `attr`。更新后的属性将应用于提交到流的后续任务。不会影响之前提交的任务。

流的属性类型`attr`当前支持的有：

- `suLaunchAttributeSpcMask` ：流作用域的`SPC` 掩码


### sudrvStreamUpdateCaptureDependencies

更新捕获流中的依赖项。


**函数签名**

```cpp
suError_t sudrvStreamUpdateCaptureDependencies(suStream_t stream,
                                               suTaskGraphNode_t *dependencies,
                                               size_t numDependencies,
                                               unsigned int flags);
```

**参数列表**

- `stream`[in]：要更新的流的句柄
- `dependencies`[in]：新的任务图节点的依赖关系节点
- `numDependencies`[in]：`dependencies` 中依赖项的数量
- `flags`[in]：标志参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorIllegalState`

**描述**

修改流的下一个捕获节点的节点的依赖项。

有效标志为：

- `suStreamAddCaptureDependencies`：增量模式，参数传递的依赖项和原有依赖合并
- `suStreamSetCaptureDependencies`：替换模式，参数传递的依赖项取代原有依赖

如果流不是捕获状态，则返回 `suErrorIllegalState`


## 事件管理

### sudrvEventCreateWithFlags

创建具有指定标志的事件对象。

**函数签名**

```cpp
suError_t sudrvEventCreateWithFlags(suEvent_t *event, unsigned int flags);
```

**参数列表**

- `event`[out]：用于返回新创建的事件的指针
- `flags`[in]：用于创建事件的标志

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorMemoryAllocation`

**描述**

使用指定标志为当前设备创建事件对象。有效标志包括：

| 可选值                                          | 说明                                                       |
| -------------------- | ----------------------------------------------------- |
| suEventDefault       | 默认事件创建标志。                                   |
| suEventBlockingSync  | 指定事件应使用阻塞同步。使用`suEventSynchronize()` 等待使用此标志创建的事件的主机线程将阻塞，直到事件实际完成。                                     |
| suEventDisableTiming | 指定创建的事件不需要记录计时数据。指定此标志且未指定 `suEventBlockingSync`标志创建的事件在与 `suStreamWaitEvent()`和 `suEventQuery()` 一起使用时将提供最佳性能。                                     |
| suEventInterprocess  | 指定创建的事件可以被`suIpcGetEventHandle()`用作进程间事件。 `suEventInterprocess`必须与`suEventDisableTiming` 一起使用。                                    |

### sudrvEventDestroy

销毁事件对象。

**函数签名**

```cpp
suError_t sudrvEventDestroy(suEvent_t event);
```

**参数列表**

- `event`[in]：要销毁的事件的句柄

**返回值**

- `suSuccess`
- `suErrorInvalidResourceHandle`
- `suErrorInvalidValue`

**描述**

销毁`event`指定的事件。

> 事件可能会在完成之前被销毁（即`sudrvEventQuery()`返回 `suErrorNotReady`）。在这种情况下调用`suEventDestroy`不会阻塞主机线程，系统会在`event`完成后自动释放相关资源。

### sudrvEventElapsedTime

计算事件之间经过的时间。

**函数签名**

```cpp
suError_t sudrvEventElapsedTime(float *ms, suEvent_t start, suEvent_t end);
```

**参数列表**

- `ms`[out]：返回事件之间经过的时间，单位为毫秒（ms）
- `start`[int]：开始计时的事件的句柄
- `end`[in]：结束计时的事件的句柄

**返回值**

- `suSuccess`
- `suErrorNotReady`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`

**描述**

以毫秒为单位计算两个事件之间经过的时间。

1. 如果`start`和`end`没有都被 `sudrvEventRecord()`记录到`stream`则返回 `suErrorInvalidResourceHandle`。
2. 如果对两个事件都调用了 `sudrvEventRecord()`但其中一个或两个事件尚未完成（即 `sudrvEventQuery()`返回 `suErrorNotReady`)，则返回 `suErrorNotReady`
3. 如果有一个或者两个事件使用了 `suEventDisableTiming`标志创建，则此函数将返回 `suErrorInvalidResourceHandle`。

> 如果`start`和`end`分别在不同的`stream`并且`stream`之间无法保证`start`在`end`之前被`record`， 则测量到的时间可能不具有参考意义。



### sudrvEventQuery

查询事件的状态。

**函数签名**

```cpp
suError_t sudrvEventQuery(suEvent_t event);
```

**参数列表**

- `event`[in]：要查询的事件的句柄

**返回值**

- `suSuccess`
- `suErrorNotReady`
- `suErrorInvalidResourceHandle`
- `suErrorInvalidValue`

**描述**

查询当前由事件捕获的所有任务的状态。
有关事件捕获内容的详细信息，请参阅 `sudrvEventRecord()`。

如果所有捕获的任务已完成，则返回 `suSuccess`，否则返回`suErrorNotReady`。


### sudrvEventRecord

在流上记录一个事件。

**函数签名**

```cpp
suError_t sudrvEventRecord(suEvent_t event, suStream_t stream);
```

**参数列表**

- `event`[in]：要记录的事件的句柄
- `stream`[in]： 记录事件的流的句柄

**返回值**

- `suSuccess`
- `suErrorInvalidResourceHandle`
- `suErrorInvalidValue`

**描述**

在流上记录一个事件， 使得主机线程能够使用`suEventQuery()`或者`suEventSynchronize()`查询或同步这个事件。
由于流的顺序执行的特性，该`event`的状态会隐式包含流上在它前面的任务是否已经完成的语义。 这就是我们所说的这个`stream`上的任务被`event`事件所捕获了。

在调用此API时， `event` 和 `stream` 必须位于同一上下文中。然后，`suEventQuery()`或 `sudrvStreamWaitEvent()`等调用将检查或等待捕获的工作完成。

 可以对同一事件多次调用`sudrvEventRecord()`，这将覆盖之前捕获的状态， `sudrvEventQuery()`或者`sudrvEventSynchronize()` 查询或同步的是最后一次所捕获的任务的状态。

> `sudrvEventRecord()`等同于`sudrvEventRecordWithFlags()` 的`flags`参数使用`suEventRecordDefault`标志。

### sudrvEventRecordWithFlags

在流上记录一个事件，附带操作标志。


**函数签名**

```cpp
suError_t sudrvEventRecordWithFlags(suEvent_t event, suStream_t stream,
                                    unsigned int flags);
```

**参数列表**

- `event`[in]：要记录的事件的句柄
- `stream`[in]： 记录事件的流的句柄
- `flags`[in]：操作标志参数

**返回值**

- `suSuccess`
- `suErrorInvalidResourceHandle`
- `suErrorInvalidValue`

**描述**

相比`sudrvEventRecord()`增加了`flags`参数，可以是：

- `suEventRecordDefault`：默认事件标志
- `suEventRecordExternal`：执行流捕获时，在计算图中捕获事件作为外部事件节点

### sudrvEventSynchronize

在主机上等待一个事件完成。

**函数签名**

```cpp
suError_t sudrvEventSynchronize(suEvent_t event);
```

**参数列表**

- `event`[in]：要等待的事件的句柄

**返回值**

- `suSuccess`
- `suErrorInvalidResourceHandle`
- `suErrorInvalidValue`

**描述**

当前主机线程阻塞并等待`event`事件中捕获的所有任务完成。有关事件捕获内容的详细信息，请参阅`sudrvEventRecord()`。

##  流上内存操作


### sudrvStreamBatchMemOp

启动用于同步的批处理内存操作。

**函数签名**

```cpp
suError_t sudrvStreamBatchMemOp(suStream_t stream, unsigned int count,
                                suStreamBatchMemOpParams *paramArray,
                                unsigned int flags);
```

**参数列表**

- `stream`[in]：启动操作的流
- `count`[in]：操作个数
- `paramArray`[in]：操作参数
- `flags`[in]：操作参数，保留字，传0

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在流`stream`上启动`count`个批处理的内存操作。具体操作类型和值在`paramArray`数组中描述。


### sudrvStreamWaitValue32

流同步GPU上的32位的值。

**函数签名**

```cpp
suError_t sudrvStreamWaitValue32(suStream_t stream, suDeviceptr_t addr,
                                 uint32_t value, unsigned int flags);
```

**参数列表**

- `stream`[in]：用于等待值的流
- `addr`[in]：等待的设备地址
- `value`[in]：等待的设备地址的值
- `flags`[in]：等待标志

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

让流`stream`和设备地址`addr`处的32位值同步，同步标志`suStreamWaitValueFlags`可以是：
- `suStreamWaitValueGeq`：`(int32_t)(*addr - value) >= 0 `时流继续执行。
- `suStreamWaitValueEq`：`(int32_t)(*addr - value) == 0 `时流继续执行。


### sudrvStreamWaitValue64

流同步GPU上的64位的值。

**函数签名**

```cpp
suError_t sudrvStreamWaitValue64(suStream_t stream, suDeviceptr_t addr,
                                 uint64_t value, unsigned int flags);
```

**参数列表**

- `stream`[in]：用于等待值的流
- `addr`[in]：等待的设备地址
- `value`[in]：等待的设备地址的值
- `flags`[in]：等待标志

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

让流`stream`和设备地址`addr`处的64位值同步，同步标志`suStreamWaitValueFlags`可以是：
- `suStreamWaitValueGeq`：`(int64_t)(*addr - value) >= 0 `时流继续执行。
- `suStreamWaitValueEq`：`(int64_t)(*addr - value) == 0 `时流继续执行。

### sudrvStreamWriteValue32

给设备地址写入32位的值。

**函数签名**

```cpp
suError_t sudrvStreamWriteValue32(suStream_t stream, suDeviceptr_t addr,
                                  uint32_t value, unsigned int flags);
```

**参数列表**

- `stream`[in]：用于写值的流
- `addr`[in]：写值的设备地址
- `value`[in]：要写入`addr`的值
- `flags`[in]：标志参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在流`stream`上启动一个内存写操作，给设备地址`addr`写入一个32位的整型值`value`。
操作参数`suStreamWriteValueFlags`只能是`suStreamWriteValueDefault`。



### sudrvStreamWriteValue64

给设备地址写入64位的值。

**函数签名**

```cpp
suError_t sudrvStreamWriteValue64(suStream_t stream, suDeviceptr_t addr,
                                  uint32_t value, unsigned int flags);
```

**参数列表**

- `stream`[in]：用于写值的流
- `addr`[in]：写值的设备地址
- `value`[in]：要写入`addr`的值
- `flags`[in]：标志参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在流`stream`上启动一个内存写操作，给设备地址`addr`写入一个64位的整型值`value`。
操作参数`suStreamWriteValueFlags`只能是`suStreamWriteValueDefault`。

  

##  执行控制

### sudrvFuncGetAttribute

查询给定函数的属性。

**函数签名**

```cpp
suError_t sudrvFuncGetAttribute(int *value, suFuncAttribute attr,
                                suDevFunc_t function);
```

**参数列表**

- `value`[out]：返回函数的属性
- `attr`[in]：查询的属性类型
- `func`[in]：核函数的名称

**返回值**

- `suSuccess`
- `suErrorInvalidDeviceFunction`

**描述**

该函数获取通过`func`指定的函数的属性。`func` 是核函数符号，必须声明为 `__global__` 函数。获取的属性放置在`attr`中。如果指定的函数不存在，则返回`suErrorInvalidDeviceFunction`对于模板化函数，请按如下所示传递函数符号： `func_name<template_arg_0,...,template_arg_N>`

> 注意：某些函数（例如maxThreadsPerBlock）的属性可能因为设备差异而有所变化。



### sudrvFuncSetAttribute

更新给定函数的属性。

**函数签名**

```cpp
suError_t sudrvFuncSetAttribute(suDevFunc_t function, suFuncAttribute attr,
                                int value);
```

**参数列表**

- `function`[in]：要设置属性的函数
- `attr`[in]：要设置的属性
- `value`[in]：属性的值

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

用`value`的值更新函数`function`的属性`attr`。

### sudrvFuncSetCacheConfig

更新函数的缓存配置。

**函数签名**

```cpp
suError_t sudrvFuncSetCacheConfig(suDevFunc_t function,
                                  suFuncCache cacheConfig);
```

**参数列表**

- `function`[in]：要更新的函数
- `cacheConfig`[in]：用于更新的值

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

用`cacheConfig`更新函数`function`的缓存配置。


### sudrvFuncSetSharedMemConfig

设置函数的共享内存配置。

**函数签名**

```cpp
suError_t sudrvFuncSetSharedMemConfig(suDevFunc_t function,
                                      suSharedMemConfig config);
```

**参数列表**

- `function`[in]：要查询的设备号
- `config`[in]：用于更新的值

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**
用`config`更新函数`function`的共享内存配置。

### sudrvLaunchHostFunc

在流队列中启动主机函数调用。

**函数签名**

```cpp
suError_t sudrvLaunchHostFunc(suStream_t stream, suHostFn_t callBackFn,
                              void *userData);
```

**参数列表**

- `stream`[in]：要启动的函数所在的流的句柄
- `callBackFn`[in]：回调函数
- `userData`[in]：要传递给函数的用户指定数据

**返回值**

- `suSuccess`
- `suErrorInvalidResourceHandle`
- `suErrorInvalidValue`
- `suErrorNotSupported`


### sudrvModuleLaunchKernel

启动核函数

**函数签名**

```cpp
suError_t sudrvModuleLaunchKernel(suDevFunc_t function, unsigned int gridDimX,
                                  unsigned int gridDimY, unsigned int gridDimZ,
                                  unsigned int blockDimX,
                                  unsigned int blockDimY,
                                  unsigned int blockDimZ,
                                  unsigned int sharedMemSize, suStream_t stream,
                                  void **funcArgs, void **extra);
```

**参数列表**

- `kernel`[in]：设备函数名字
- `gridDimX`[in]：网格尺寸x维度
- `gridDimY`[in]：网格尺寸y维度
- `gridDimZ`[in]：网格尺寸z维度
- `blockDimX`[in]：块的尺寸x维度
- `blockDimY`[in]：块的尺寸y维度
- `blockDimZ`[in]：块的尺寸z维度
- `shareMemSize`[in]：共享内存大小
- `stream`[in]：流的句柄
- `arguments`[in]：设备函数的参数
- `extra`[in]：extra格式参数

**返回值**

- `suSuccess`
- `suErrorInvalidDeviceFunction`
- `suErrorInvalidConfiguration`
- `suErrorLaunchFailure`
- `suErrorLaunchOutOfResource`

**描述**

- 调用内核函数，该函数使用的网格是`gridDim`，这表示有总数为`gridDim.x * gridDim.y * gridDim.z`个线程块，每个块都包含 `blockDim` （即`blockDim.x * blockDim.y * blockDim.z`）个线程。

- 如果内核有 N 个参数，则 args 应指向 N 个指针的数组。从 args[0] 到 args[N - 1] 的每个指针都指向将从中复制实际参数的内存区域。
- sharedMem 设置每个线程块可用的动态共享内存量。
- stream 指定调用所关联的流。
- 该函数是异步的，即启动核函数后立即返回，不会等待核函数执行完成。


### sudrvFuncGetModule

查询函数所在的模块。

**函数签名**

```cpp
suError_t sudrvFuncGetModule(suModule_t *module, suDevFunc_t function);
```

**参数列表**

- `module`[out]：返回模块句柄
- `function`[in]：要查询的函数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*module`中返回函数`function`所在的模块。


### sudrvLaunchKernelEx

使用启动时配置启动 `BIRENSUPA`函数。

**函数签名**

```cpp
suError_t sudrvLaunchKernelEx(const suLaunchConfig *config, suDevFunc_t f,
                              void **kernelParams, void **extra);
```

**参数列表**

- config[in]：设备函数配置
- `f`[in]：设备函数名字
- `args`[in]：设备函数参数
- `extra`[in]：设备函数extra参数

**返回值**

- `suSuccess`
- `suErrorInvalidDeviceFunction`
- `suErrorInvalidConfiguration`
- `suErrorLaunchFailure`
- `suErrorLaunchOutOfResource`

**描述**

类同`suLaunchKernelSingleDevice`，启动配置信息在`*config`中描述。

>`extra`参数可以用于传递 `suTensorObject_t`类型的参数。


##  任务图管理

本节介绍`BIRENSUPA`驱动应用程序编程接口的任务图管理功能。

### sudrvGraphAddChildGraphNode

创建一个子任务图节点并将其添加到任务图中。

**函数签名**

```cpp
suError_t sudrvGraphAddChildGraphNode(suTaskGraphNode_t *node,
                                      suTaskGraph_t graph,
                                      const suTaskGraphNode_t *dependencies,
                                      size_t numDependencies,
                                      suTaskGraph_t childGraph);
```

**参数列表**

- `node`[out]：返回新创建的节点
- `graph`[in]：要添加节点的任务图
- `dependencies`[in]：节点的依赖关系
- `numDependencies`[in]： 依赖项数量
- `childGraph`[in]：要克隆到此节点的任务图

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`

**描述**

创建一个包含子图的新节点，并将其添加到具有通过 `dependencies` 指定的 `numDependencies` 依赖项的任务图中。`numDependencies` 可能为 `0`，在这种情况下，该节点将成为根节点。`dependencies` 不能有任何重复的节点。新节点的句柄将在 `*node` 中返回。

> 被包含进节点的子任务图是`graph`的克隆子图。

### sudrvGraphAddDependencies

向任务图添加依赖关系边缘。

**函数签名**

```cpp
suError_t sudrvGraphAddDependencies(suTaskGraph_t graph,
                                    const suTaskGraphNode_t *from,
                                    const suTaskGraphNode_t *to,
                                    size_t numDependencies);
```

**参数列表**

- `graph`[in]：要添加依赖边缘的任务图
- `from`[in]：提供被依赖的节点数组
- `to`[in]： 依赖节点数组
- `numDependencies`[in]：要添加的依赖项数量

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`

**描述**

向任务图添加依赖关系边缘。
依赖关系由 `from[i]` 和 `to[i]`组成被依赖节点以及依赖的节点关系表达，其中`i ∈ [0 .... (numDependencies-1)]` 。
要求`from` 和 `to` 中的每个节点都必须属于 `graph`。

如果`numDependencies`为`0，`则`from`和`to`中的元素将被忽略。


### sudrvGraphAddEmptyNode

创建一个空节点并将其添加到任务图中。

**函数签名**

```cpp
suError_t sudrvGraphAddEmptyNode(suTaskGraphNode_t *node, suTaskGraph_t graph,
                                 const suTaskGraphNode_t *dependencies,
                                 size_t numDependencies);
```

**参数列表**

- `node`[out]： 返回新创建的节点
- `graph`[in]：要添加节点的任务图
- `dependencies`[in]：节点的依赖关系
- `numDependencies`[in]： 依赖项数量

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`

**描述**

创建新的空节点，并将其添加到具有通过 `dependencies` 指定的 `numDependencies` 依赖项的任务图中。`numDependencies` 可能为 `0`，在这种情况下，该节点将成为根节点。`dependencies` 不能有任何重复的节点。新节点的句柄将在 `*node` 中返回。

> 空节点不包含实际的计算任务，只在图中添加一个占位节点。可以用于改变图中依赖关系。

### sudrvGraphAddHostNode

创建主机执行节点并将其添加到任务图中。

**函数签名**

```cpp
suError_t sudrvGraphAddHostNode(suTaskGraphNode_t *node, suTaskGraph_t graph,
                                const suTaskGraphNode_t *dependencies,
                                size_t numDependencies,
                                const suHostNodeParams *nodeParams);
```

**参数列表**

- `node`[out]： 返回新创建的节点
- `graph`[in]：要添加节点的任务图
- `dependencies`[in]：节点的依赖关系
- `numDependencies`[in]： 依赖项数量
- `nodeParams`[in]：主机回调函数的参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`

**描述**

创建新的Host节点，并将其添加到具有通过 `dependencies` 指定的 `numDependencies` 依赖项的任务图中。`numDependencies` 可能为 `0`，在这种情况下，该节点将成为根节点。`dependencies` 不能有任何重复的节点。新节点的句柄将在 `*node` 中返回。

### sudrvGraphAddKernelNode

创建内核执行节点并将其添加到任务图中。

**函数签名**

```cpp
suError_t sudrvGraphAddKernelNode(suTaskGraphNode_t *node, suTaskGraph_t graph,
                                  const suTaskGraphNode_t *dependencies,
                                  size_t numDependencies,
                                  const sudrvKernelNodeParams *nodeParams);
```

**参数列表**

- `node`[out]： 返回新创建的节点
- `graph`[in]：要添加节点的任务图
- `dependencies`[in]：节点的依赖关系
- `numDependencies`[in]： 依赖项数量
- `nodeParams`[in]：kernel参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`

**描述**

创建新的Kernel节点，并将其添加到具有通过 `dependencies` 指定的 `numDependencies` 依赖项的任务图中。`numDependencies` 可能为 `0`，在这种情况下，该节点将成为根节点。`dependencies` 不能有任何重复的节点。新节点的句柄将在 `*node` 中返回。

###  sudrvGraphAddMemcpyNode

创建一个 memcpy 节点并将其添加到任务图中。

**函数签名**

```cpp
suError_t sudrvGraphAddMemcpyNode(suTaskGraphNode_t *node, suTaskGraph_t graph,
                                  const suTaskGraphNode_t *dependencies,
                                  size_t numDependencies,
                                  const suMemcpy3DDesc *nodeParams,
                                  suContext context);
```

**参数列表**

- `node`[out]： 返回新创建的节点
- `graph`[in]：要添加节点的任务图
- `dependencies`[in]：节点的依赖关系
- `numDependencies`[in]： 依赖项数量
- `nodeParams`[in]：内存复制的参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`

**描述**

创建新的memcpy节点，并将其添加到具有通过 `dependencies` 指定的 `numDependencies` 依赖项的任务图中。`numDependencies` 可能为 `0`，在这种情况下，该节点将成为根节点。`dependencies` 不能有任何重复的节点。新节点的句柄将在 `*node` 中返回。

### sudrvGraphAddMemsetNode

创建一个 memset 节点并将其添加到任务图中。

**函数签名**

```cpp
suError_t sudrvGraphAddMemsetNode(suTaskGraphNode_t *node, suTaskGraph_t graph,
                                  const suTaskGraphNode_t *dependencies,
                                  size_t numDependencies,
                                  const suMemsetParams *nodeParams);
```

**参数列表**

- `node`[out]： 返回新创建的节点
- `graph`[in]：要添加节点的任务图
- `dependencies`[in]：节点的依赖关系
- `numDependencies`[in]： 依赖项数量
- `nodeParams`[in]：memset的参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`

**描述**

创建新的memset节点，并将其添加到具有通过 `dependencies` 指定的 `numDependencies` 依赖项的任务图中。`numDependencies` 可能为 `0`，在这种情况下，该节点将成为根节点。`dependencies` 不能有任何重复的节点。新节点的句柄将在 `*node` 中返回。

### sudrvGraphAddEventRecordNode

创建事件记录节点并将其添加到任务图中。

**函数签名**

```cpp
suError_t sudrvGraphAddEventRecordNode(suTaskGraphNode_t *node,
                                       suTaskGraph_t graph,
                                       const suTaskGraphNode_t *dependencies,
                                       size_t numDependencies, suEvent_t event);
```

**参数列表**

- `node`[out]： 返回新创建的节点
- `graph`[in]：要添加节点的任务图
- `dependencies`[in]：节点的依赖关系
- `numDependencies`[in]： 依赖项数量
- `event`[in]：节点的事件

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`

**描述**

创建新的事件记录节点，并将其添加到具有通过 `dependencies` 指定的 `numDependencies` 依赖项的任务图中。`numDependencies` 可能为 `0`，在这种情况下，该节点将成为根节点。`dependencies` 不能有任何重复的节点。新节点的句柄将在 `*node` 中返回。

### sudrvGraphAddEventWaitNode

创建一个事件等待节点并将其添加到任务图中。

**函数签名**

```cpp
suError_t sudrvGraphAddEventWaitNode(suTaskGraphNode_t *node,
                                     suTaskGraph_t graph,
                                     const suTaskGraphNode_t *dependencies,
                                     size_t numDependencies, suEvent_t event);
```

**参数列表**

- `node`[out]： 返回新创建的节点
- `graph`[in]：要添加节点的任务图
- `dependencies`[in]：节点的依赖关系
- `numDependencies`[in]： 依赖项数量
- `event`[in]：节点的事件

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`

**描述**

创建新的事件等待节点，并将其添加到具有通过 `dependencies` 指定的 `numDependencies` 依赖项的任务图中。`numDependencies` 可能为 `0`，在这种情况下，该节点将成为根节点。`dependencies` 不能有任何重复的节点。新节点的句柄将在 `*node` 中返回。

###  sudrvGraphChildGraphNodeGetGraph

获取子任务图节点的嵌入任务图的句柄。

**函数签名**

```cpp
suError_t sudrvGraphChildGraphNodeGetGraph(suTaskGraphNode_t node,
                                           suTaskGraph_t *graph);
```

**参数列表**

- `node`[in]：获取嵌入式任务图的节点
- `graph`[out]：存储任务图句柄的位置

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`

**描述**

获取子图节点中嵌入图的任务图句柄。这个函数不会克隆节点中的任务图。所以后续对`graph`的的修改就是在修改子图节点。

> 子图节点保留图的所有权，用户**不要**使用`suTaskGraphDestroy()`去销毁本函数返回的图。

###  sudrvGraphClone

克隆任务图。

**函数签名**

```cpp
suError_t sudrvGraphClone(suTaskGraph_t *graphClone,
                          suTaskGraph_t originalGraph);
```

**参数列表**

- `graphClone`[out]：返回新创建的克隆任务图
- `originalGraph`[in]：要克隆的任务图

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

此函数创建 `originalGraph` 的副本并将其返回到 `graphClone` 中。所有参数都被复制到克隆图中。后续原始图的修改不会影响克隆图。

> 原始图中的子图节点被递归地复制到克隆的新中。

### sudrvGraphCreate

创建任务图。

**函数签名**

```cpp
suError_t sudrvGraphCreate(suTaskGraph_t *graph, unsigned int flags);
```

**参数列表**

- `graph`[out]：返回新创建的任务图
- `flags`[in]：任务图创建标志，必须为 0

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

创建一个空图，通过 `*graph` 返回。

### sudrvGraphDestroy

销毁任务图。

**函数签名**

```cpp
suError_t sudrvGraphDestroy(suTaskGraph_t graph);
```

**参数列表**

- `graph`[in]：要销毁的任务图

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

销毁图 `graph` 及其所有节点。

### sudrvGraphDestroyNode

从任务图中删除节点。

**函数签名**

```cpp
suError_t sudrvGraphDestroyNode(suTaskGraphNode_t node);
```

**参数列表**

- `node`[in]：要删除的节点

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

从图中删除 `node`。此操作还会切断所有其他节点对 `node` 依赖关系。

### sudrvGraphExecDestroy

销毁可执行任务图。

**函数签名**

```cpp
suError_t sudrvGraphExecDestroy(suTaskGraphExec_t graphExec);
```

**参数列表**

- `graphExec`[in]：要销毁的可执行图

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

销毁`graphExec`指定的可执行图。

### sudrvGraphExecHostNodeSetParams

在给定的 `graphExec` 中设置主机节点的参数。

**函数签名**

```cpp
suError_t sudrvGraphExecHostNodeSetParams(suTaskGraphExec_t graphExec,
                                          suTaskGraphNode_t node,
                                          const suHostNodeParams *nodeParams);
```

**参数列表**

- `graphExec`[in]：用于设置指定节点的可执行图
- `node`[in]： 图中用于实例化 `graphExec` 的主机节点
- `nodeParams`[in]：要更新的参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

更新 `graphExec` 中 `node` 表示的主机节点的任务参数。 `node`必须在用于实例化`graphExec`的任务图中。

这些修改仅影响后续启动`graphExec`。已排队或正在运行的 `graphExec` 不受此调用的影响。 `node`的参数也不会被此函数修改。


### sudrvGraphExecKernelNodeSetParams

在给定的  `graphExec` 中设置内核节点的参数。

**函数签名**

```cpp
suError_t
sudrvGraphExecKernelNodeSetParams(suTaskGraphExec_t graphExec,
                                  suTaskGraphNode_t node,
                                  const sudrvKernelNodeParams *nodeParams);
```

**参数列表**

- `graphExec`[in]：用于设置指定节点的可执行图
- `node`[in]： 图中用于实例化 `graphExec` 的主机节点
- `nodeParams`[in]：要更新的参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

更新 `graphExec` 中 `node` 表示的kernel节点的任务参数。 `node`必须在用于实例化`graphExec`的任务图中。

这些修改仅影响后续启动`graphExec`。已排队或正在运行的 `graphExec` 不受此调用的影响。 `node`的参数也不会被此函数修改。

### sudrvGraphExecMemsetNodeSetParams

设置给定 `graphExec` 中 memset 节点的参数。

**函数签名**

```cpp
suError_t sudrvGraphExecMemsetNodeSetParams(suTaskGraphExec_t graphExec,
                                            suTaskGraphNode_t node,
                                            const suMemsetParams *nodeParams,
                                            suContext context);
```

**参数列表**

- `graphExec`[in]：用于设置指定节点的可执行图
- `node`[in]：图中用于实例化 `graphExec` 的主机节点
- `nodeParams`[in]：要更新的参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

更新 `graphExec` 中 `node` 表示的memset节点的任务参数。 `node`必须在用于实例化`graphExec`的任务图中。

这些修改仅影响后续启动`graphExec`。已排队或正在运行的 `graphExec` 不受此调用的影响。 `node`的参数也不会被此函数修改。

### sudrvGraphExecMemcpyNodeSetParams

设置给定 `graphExec` 中 memcpy 节点的参数。

**函数签名**

```cpp
suError_t sudrvGraphExecMemcpyNodeSetParams(suTaskGraphExec_t graphExec,
                                            suTaskGraphNode_t node,
                                            const suMemcpy3DDesc *nodeParams,
                                            suContext context);
```

**参数列表**

- `graphExec`[in]：用于设置指定节点的可执行图
- `node`[in]： 图中用于实例化 `graphExec` 的主机节点
- `nodeParams`[in]：要更新的参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

更新 `graphExec` 中 `node` 表示的memcpy节点的任务参数。 `node`必须在用于实例化`graphExec`的任务图中。

这些修改仅影响后续启动`graphExec`。已排队或正在运行的 `graphExec` 不受此调用的影响。 `node`的参数也不会被此函数修改。

### sudrvGraphExecUpdate

检查可执行图是否可以用图更新，如果可能则执行更新。

**函数签名**

```cpp
suError_t sudrvGraphExecUpdate(suTaskGraphExec_t graphExec, suTaskGraph_t graph,
                               suTaskGraphNode_t *errorNodeOut,
                               suTaskGraphExecUpdateResult *updateResultOut);
```

**参数列表**

- `graphExec`[in]：用于更新的可执行图
- `graph`[in]：包含更新参数的任务图
- `errorNode`Out[out]：导致权限检查禁止更新的节点（如果有）
- `updateResultOut`[out]：是否允许任务图更新。如果被禁止，原因是什么

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorGraphExecUpdateFailure`

**描述**

使用 `graph` 指定的拓扑相同图中的节点参数更新 `graphExec` 指定的实例化图中的节点参数。


### sudrvGraphGetEdges

返回图的依赖边。

**函数签名**

```cpp
suError_t sudrvGraphGetEdges(suTaskGraph_t graph, suTaskGraphNode_t *from,
                             suTaskGraphNode_t *to, size_t *numEdges);
```

**参数列表**

- `graph`[in]：从中获取边缘的任务图
- `from`[out]：返回边缘端点的数组
- `to`[out]：返回边缘端点的数组
- `numEdges`[out]：边的数目

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

返回任务图依赖边的列表。边通过 `from` 和 `to` 中相应的索引返回；也就是说，`to[i]`中的节点对`from[i]`中的节点有依赖关系。 `from` 和 `to` 可能都为 `NULL`，在这种情况下，此函数仅在 `numEdges` 中返回边数。否则， `from` 和 `to` 中将填充`numEdges`数量的依赖。如果`numEdges`高于实际边数，则`from`和`to`中的剩余条目将被设置为`NULL`，实际返回的边数将被写入`numEdges`。

### sudrvGraphGetNodes

返回图的节点。

**函数签名**

```cpp
suError_t sudrvGraphGetNodes(suTaskGraph_t graph, suTaskGraphNode_t *nodes,
                             size_t *numNodes);
```

**参数列表**

- `graph`[in]：要查询的图
- `nodes`[out]：返回节点的数组
- `numNodes`[out]：返回节点数目

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

返回任务图的节点列表。 `nodes` 可能为 NULL，在这种情况下，此函数将在`*numNodes`中返回节点数。如果`numNodes`高于实际节点数，则`nodes`中的剩余条目将被设置为`NULL`，`numNodes`中返回实际获取的节点数。

### sudrvGraphGetRootNodes

返回图的根节点。

**函数签名**

```cpp
suError_t sudrvGraphGetRootNodes(suTaskGraph_t graph,
                                 suTaskGraphNode_t *rootNodes,
                                 size_t *numRootNodes);
```

**参数列表**

- `graph`[in]：要查询的图
- `rootNodes`[out]：返回节点的数组
- `numRootNodes`[out]：返回节点数目

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

返回计算图根节点的列表。 `rootNodes` 可以为 `NULL`，在这种情况下，此函数将在 `numRootNodes` 中返回根节点数。否则，`rootNodes` 中将传出 `numRootNodes`个节点。如果 `numRootNodes`高于实际根节点数，则`rootNodes`中的剩余条目将被设置为`NULL`，实际获取的节点数将在`numRootNodes`中返回。

### sudrvGraphHostNodeGetParams

返回主机节点的参数。

**函数签名**

```cpp
suError_t sudrvGraphHostNodeGetParams(suTaskGraphNode_t node,
                                      suHostNodeParams *nodeParams);
```

**参数列表**

- `node`[in]：要获取参数的节点
- `nodeParams`[out]：返回参数的指针

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*nodeParams`中返回主机节点`node`的参数。

### sudrvGraphHostNodeSetParams

设置主机节点的参数。

**函数签名**

```cpp
suError_t sudrvGraphHostNodeSetParams(suTaskGraphNode_t node,
                                      const suHostNodeParams *nodeParams);
```

**参数列表**

- `node`[in]：要更新参数的节点
- `nodeParams`[out]：参数所在结构体指针

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

将主机节点`node`的参数设置为`nodeParams`。

### sudrvGraphInstantiate

用任务图创建可执行任务图。

**函数签名**

```cpp
suError_t sudrvGraphInstantiate(suTaskGraphExec_t *graphExec,
                                suTaskGraph_t graph,
                                suTaskGraphNode_t *errorNode, char *logBuffer,
                                size_t bufferSize);
```

**参数列表**

- `graphExec`[out]：返回实例化图
- `graph`[in]：实例化任务图
- `errorNode`[out]：保留参数，传NULL即可
- `logBuffer`[out]：保留参数，传NULL即可
- `bufferSize`[out]：保留参数，传NULL即可

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

验证 `graph` 的有效性。如果符合要求则实例化`graph`并在 `*graphExec`返回实例化的可执行图。


### sudrvGraphKernelNodeGetParams

返回内核节点的参数。

**函数签名**

```cpp
suError_t sudrvGraphKernelNodeGetParams(suTaskGraphNode_t node,
                                        sudrvKernelNodeParams *nodeParams);
```

**参数列表**

- `node`[in]：要获取参数的节点
- `nodeParams`[out]：返回参数的指针

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*nodeParams`中返回Kernel节点`node`的参数。

### sudrvGraphKernelNodeSetParams

设置内核节点的参数。

**函数签名**

```cpp
suError_t
sudrvGraphKernelNodeSetParams(suTaskGraphNode_t node,
                              const sudrvKernelNodeParams *nodeParams);
```

**参数列表**

- `node`[in]：要更新参数的节点
- `nodeParams`[out]：参数所在结构体指针

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

将Kernel节点`node`的参数设置为`nodeParams`。

### sudrvLaunchGraphExec

在流中启动可执行图。

**函数签名**

```cpp
suError_t sudrvLaunchGraphExec(suTaskGraphExec_t graphExec, suStream_t stream);
```

**参数列表**

- `graphExec`[in]：要启动的可执行图
- `stream`[in]：启动可执行图的流的句柄

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`stream`中执行`graphExec`。一次只能执行一个`graphExec` 实例。每次启动都排在 `stream` 中任何先前的任务以及先前启动 `graphExec` 的后面。要同时执行一个图，必须将其多次实例化为多个可执行图。

### sudrvGraphMemcpyNodeGetParams

返回 memcpy 节点的参数。

**函数签名**

```cpp
suError_t sudrvGraphMemcpyNodeGetParams1D(suTaskGraphNode_t node,
                                          suMemcpyParams *nodeParams);
```

**参数列表**

- `node`[in]：要获取参数的节点
- `nodeParams`[out]：返回参数的指针

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*nodeParams`中返回memcpy节点`node`的参数。

### sudrvGraphMemcpyNodeSetParams

设置 memcpy 节点的参数。

**函数签名**

```cpp
suError_t sudrvGraphMemcpyNodeSetParams(suTaskGraphNode_t node,
                                        const suMemcpy3DDesc *nodeParams);
```

**参数列表**

- `node`[in]：要更新参数的节点
- `nodeParams`[out]：参数所在结构体指针

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

将memcpy节点`node`的参数设置为`nodeParams`。

### sudrvGraphMemsetNodeGetParams

返回 memset 节点的参数。

**函数签名**

```cpp
suError_t sudrvGraphMemsetNodeGetParams(suTaskGraphNode_t node,
                                        suMemsetParams *nodeParams);
```

**参数列表**

- `node`[in]：要获取参数的节点
- `nodeParams`[out]：返回参数的指针

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*nodeParams`中返回memset节点`node`的参数。

### sudrvGraphMemsetNodeSetParams

设置 memset 节点的参数。

**函数签名**

```cpp
suError_t sudrvGraphMemsetNodeSetParams(suTaskGraphNode_t node,
                                        const suMemsetParams *nodeParams);
```

**参数列表**

- `node`[in]：要更新参数的节点
- `nodeParams`[out]：参数所在结构体指针

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

将memset节点`node`的参数设置为`nodeParams`。

### sudrvGraphNodeFindInClone

查找节点的克隆版本。

**函数签名**

```cpp
suError_t sudrvGraphNodeFindInClone(suTaskGraphNode_t *node,
                                    suTaskGraphNode_t originalNode,
                                    suTaskGraph_t clonedGraph);
```

**参数列表**

- `node`[out]：返回克隆节点的句柄
- `originalNode`[in]：原始节点的句柄
- `clonedGraph`[in]：要查询的克隆图

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

返回`clonedGraph`中与原始任务图中的`originalNode`相对应的节点。

`clonedGraph` 必须是通过 `suTaskGraphClone()` 从 `originalGraph` 克隆得到。 `originalNode` 在调用 `suTaskGraphClone()` 时必须已在 `originalGraph` 中，并且 `clonedGraph` 中对应的克隆节点没有被删除。然后通过 `*node` 返回克隆的节点。

### sudrvGraphNodeGetDependentNodes

返回节点的依赖节点。

**函数签名**

```cpp
suError_t sudrvGraphNodeGetDependentNodes(suTaskGraphNode_t node,
                                          suTaskGraphNode_t *dependentNodes,
                                          size_t *numDependentNodes);
```

**参数列表**

- `node`[in]：需要查询的节点的句柄
- `dependentNodes`[out]：返回依赖的节点数组
- `numDependentNodes`[out]：返回`dependentNodes`中节点的数量
-

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

返回节点的依赖节点的列表。 `dependentNodes` 可能为 NULL，在这种情况下，此函数将在`numDependentNodes`返回依赖节点数。如果`*numDependentNodes`高于实际依赖节点数，则`dependentNodes`中的剩余条目将被设置为`NULL`，实际获取的节点数将在`*numDependentNodes`中返回。

### sudrvGraphNodeGetDependencies

返回节点的依赖关系。

**函数签名**

```cpp
suError_t sudrvGraphNodeGetDependencies(suTaskGraphNode_t node,
                                        suTaskGraphNode_t *dependencies,
                                        size_t *numDependencies);
```

**参数列表**

- `node`[in]：需要查询的节点的句柄
- `dependentNodes`[out]：返回依赖的节点数组
- `numDependentNodes`[out]：返回`dependentNodes`中节点的数量

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

返回节点依赖项的列表。 `dependencies` 可能为 `NULL`，在这种情况下，此函数将在 `*numDependencies` 中返回依赖项数量。如果`numDependencies`高于实际的依赖项数量，则`dependencies`中的剩余条目将被设置为`NULL`，实际获取的节点数将在`numDependencies`中返回。

### sudrvGraphNodeGetType

返回节点的类型。

**函数签名**

```cpp
suError_t sudrvGraphNodeGetType(suTaskGraphNode_t node,
                                suTaskGraphNodeType *type);
```

**参数列表**

- `node`[in]：要查询的节点句柄
- `type`[out]：返回节点类型

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*type`中返回节点`node`的类型。

### sudrvGraphRemoveDependencies

从图中删除依赖边。

**函数签名**

```cpp
suError_t sudrvGraphRemoveDependencies(suTaskGraph_t graph,
                                       const suTaskGraphNode_t *from,
                                       const suTaskGraphNode_t *to,
                                       size_t numDependencies);
```

**参数列表**

- `graph`[in]：依赖边所在的任务图句柄
- `from`[in]：依赖边的起始节点数组
- `to`[in]：依赖边的结束节点数组
- `numDependencies`[in]：`from`与`to`数组的大小

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

删除任务图中 `numDependencies` 个依赖关系，依赖关系由`from[i]` 和 `to[i]` 组成的成对节点所在的边所表示。 其中`from` 和 `to` 中的每个节点都必须属于 `graph`。

如果`numDependencies`为`0`，则`from`和`to`中的元素将被忽略。
指定不存在的依赖项将返回错误。

### sudrvGraphDebugDotPrint

编写一个描述图结构的 DOT 文件。

**函数签名**

```cpp
suError_t sudrvGraphDebugDotPrint(suTaskGraph_t graph, const char *path,
                                  unsigned int flags);
```

**参数列表**

- `graph`[in]：要打印的任务图
- `path`[in]：DOT文件的保存路径
- `flags`[in]：标志参数，目前传0即可

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

编写一个描述图结构的 DOT 文件。

### sudrvGraphEventRecordNodeGetEvent

返回与事件记录节点关联的事件。

**函数签名**

```cpp
suError_t sudrvGraphEventRecordNodeGetEvent(suTaskGraphNode_t node,
                                            suEvent_t *event);
```

**参数列表**

- `node`[in]：要获取参数的节点
- `event`[out]：返回事件句柄

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*event`中返回事件记录节点`node`的中使用的事件。

### sudrvGraphEventRecordNodeSetEvent

设置事件记录节点的事件。

**函数签名**

```cpp
suError_t sudrvGraphEventRecordNodeSetEvent(suTaskGraphNode_t node,
                                            suEvent_t event);
```

**参数列表**

- `node`[in]：要更新参数的节点
- `event`[in]：要设置的事件的句柄

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

 给事件记录节点`node`设置新的事件`event`。

### sudrvGraphEventWaitNodeGetEvent

返回与事件等待节点关联的事件。

**函数签名**

```cpp
suError_t sudrvGraphEventWaitNodeGetEvent(suTaskGraphNode_t node,
                                          suEvent_t *event);
```

**参数列表**

- `node`[in]：要获取参数的节点
- `event`[out]：返回事件句柄

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*event`中返回事件等待节点`node`的中使用的事件。

### sudrvGraphEventWaitNodeSetEvent

设置事件等待节点的事件。

**函数签名**

```cpp
suError_t sudrvGraphEventWaitNodeSetEvent(suTaskGraphNode_t node,
                                          suEvent_t event);
```

**参数列表**

- `node`[in]：要更新参数的节点
- `event`[in]：要设置的事件的句柄

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

给事件等待节点`node`设置新的事件`event`。

### sudrvGraphExecEventRecordNodeSetEvent

设置给定 `graphExec` 中事件记录节点的事件。

**函数签名**

```cpp
suError_t sudrvGraphExecEventRecordNodeSetEvent(suTaskGraphExec_t graphExec,
                                                suTaskGraphNode_t node,
                                                suEvent_t event);
```

**参数列表**

- `graphExec`[in]： 设置指定节点的可执行图
- `node`[in]：实例化 `graphExec` 的任务图中的事件记录节点
- `event`[in]：要更新的事件

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

设置可执行图`graphExec`中的事件记录节点的事件。该节点由源任务图图中对应的节点 `node`实例化得到。

这些修改仅影响 `graphExec` 的未来启动。已排队或正在运行的 `graphExec`启动不受此调用的影响。 `node` 也不会被此调用修改。

### sudrvGraphExecEventWaitNodeSetEvent

设置给定 `graphExec` 中事件等待节点的事件。

**函数签名**

```cpp
suError_t sudrvGraphExecEventWaitNodeSetEvent(suTaskGraphExec_t graphExec,
                                              suTaskGraphNode_t node,
                                              suEvent_t event);
```

**参数列表**

- `graphExec`[in]： 设置指定节点的可执行图
- `node`[in]：实例化 `graphExec`的任务图中的事件记录节点
- `event`[in]：要更新的事件

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

设置可执行图`graphExec`中的事件等待节点的事件。该节点由源任务图图中对应的节点 `node`实例化得到。

这些修改仅影响 `graphExec` 的未来启动。已排队或正在运行的 `graphExec`启动不受此调用的影响。 `node` 也不会被此调用修改。

### sudrvGraphExecChildGraphNodeSetGraph  

更新给定 `graphExec` 中子图节点中的节点参数。
 
  **函数签名**

```cpp
suError_t sudrvGraphExecChildGraphNodeSetGraph(suTaskGraphExec_t graphExec,
                                               suTaskGraphNode_t node,
                                               suTaskGraph_t childGraph);
```

**参数列表**

- `graphExec`[in]：设置指定节点的可执行图
- `node`[in] 实例化 `graphExec` 的任务图中的子图节点
- `childGraph`[in]：用于更新参数的子图

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

设置可执行图`graphExec`中子图节点所使用的子图。该节点由源任务图图中对应的节点 `node`实例化得到。

这些修改仅影响 `graphExec` 的未来启动。已排队或正在运行的 `graphExec`启动不受此调用的影响。 `node` 也不会被此调用修改。

### sudrvGraphAddBatchMemOpNode

创建一个内存操作批处理节点并将其添加到任务图中。

  **函数签名**

```cpp
suError_t sudrvGraphAddBatchMemOpNode(suTaskGraphNode_t *graphNode,
                                      suTaskGraph_t graph,
                                      const suTaskGraphNode_t *dependencies,
                                      size_t numDependencies,
                                      const suBatchMemOpNodeParams *nodeParams);
```

**参数列表**

- `node`[out]：返回新创建的节点
- `graph`[in]：要添加节点的任务图
- `dependencies`[in]：节点的依赖关系
- `numDependencies`[in]： 依赖项数量
- `nodeParams`[in]：内存操作批处理参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidResourceHandle`

**描述**

创建一个内存操作批处理节点，并将其添加到具有通过 `dependencies` 指定的 `numDependencies` 依赖项的任务图中。`numDependencies` 可能为 `0`，在这种情况下，该节点将成为根节点。`dependencies` 不能有任何重复的节点。新节点的句柄将在 `*node` 中返回。


### sudrvGraphBatchMemOpNodeGetParams

返回内存操作批处理节点的参数。

  **函数签名**

```cpp
suError_t sudrvGraphBatchMemOpNodeGetParams(suTaskGraphNode_t graphNode,
                                            suBatchMemOpNodeParams *nodeParams);
```

**参数列表**

- `node`[in]：要获取参数的节点
- `nodeParams`[out]：返回参数的指针

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*nodeParams`中返回内存操作批处理节点`node`的参数。

### sudrvGraphBatchMemOpNodeSetParams

设置内存操作批处理节点的参数。

  **函数签名**

```cppsuError_t
sudrvGraphBatchMemOpNodeSetParams(suTaskGraphNode_t graphNode,
                                  const suBatchMemOpNodeParams *nodeParams);
```

**参数列表**

- `node`[in]：要更新参数的节点
- `nodeParams`[out]：参数所在结构体指针

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

将内存操作批处理节点`node`的参数设置为`nodeParams`。

### sudrvGraphExecBatchMemOpNodeSetParams

设置给定 `graphExec` 中内存操作批处理节点的参数。

**函数签名**

```cpp
suError_t
sudrvGraphExecBatchMemOpNodeSetParams(suTaskGraphExec_t graphExec,
                                      suTaskGraphNode_t graphNode,
                                      const suBatchMemOpNodeParams *nodeParams);
```

**参数列表**

- `graphExec`[in]： 设置指定节点的可执行图
- `node`[in]：实例化 `graphExec` 的任务图中的内存操作批处理节点
- `nodeParams`[in]：要更新的参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

设置可执行图`graphExec`中的内存操作批处理节点的事件。该节点由源任务图图中对应的节点 `node`实例化得到。

这些修改仅影响 `graphExec` 的未来启动。已排队或正在运行的 `graphExec`启动不受此调用的影响。 `node` 也不会被此调用修改。

### sudrvGraphKernelNodeCopyAttributes

将属性从源节点复制到目标节点。

  **函数签名**

```cpp
suError_t sudrvGraphKernelNodeCopyAttributes(suTaskGraphNode_t dst,
                                             suTaskGraphNode_t src);
```

**参数列表**

- `dst`[in]：目标节点句柄
- `src`[in]：源节点句柄

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

将属性从源节点 `src` 复制到目标节点 `dst`。两个节点必须具有相同的上下文。

### sudrvGraphKernelNodeGetAttribute

 查询内核节点属性。
 
**函数签名**

```cpp
suError_t sudrvGraphKernelNodeGetAttribute(suTaskGraphNode_t graphNode,
                                           suKernelNodeAttrId attr,
                                           suKernelNodeAttrValue *valueOut);
```

**参数列表**

- `graphNode`[in]：要查询的节点句柄
- `attr`[in]：属性类别的枚举值
- `valueOut`[out]：返回属性的值

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

从节点 `graphNode` 查询属性 `attr` 并将其存储到 `*valueOut`的相应成员中。

### sudrvGraphKernelNodeSetAttribute

设置内核节点属性。

**函数签名**

```cpp
suError_t sudrvGraphKernelNodeSetAttribute(suTaskGraphNode_t graphNode,
                                           suKernelNodeAttrId attr,
                                           const suKernelNodeAttrValue *value);
```

**参数列表**

- `graphNode`[in]：要设置的节点句柄
- `attr`[in]：属性类别的枚举值
- `valueOut`[in]：要设置的属性的值的指针

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

用值`*value`的相应属性设置节点 `graphNode` 的属性 `attr`。

### sudrvGraphNodeGetEnabled

查询给定 `graphExec` 中的节点是否启用。

**函数签名**

```cpp
suError_t sudrvGraphNodeGetEnabled(suTaskGraphExec_t graphExec,
                                   suTaskGraphNode_t node,
                                   unsigned int *isEnabled);
```

**参数列表**

- `graphExec`[in]：设置指定节点的可执行图
- `node`[in]：例化 `graphExec` 的图表中的节点
- `isEnabled`[out]： 返回节点启用状态的指针

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

返回`node`所表示的节点在`graphExec`中是否被启用。
 `isEnabled` = 1 为启用，反之则禁用。
 
### sudrvGraphNodeSetEnabled

启用或禁用给定 `graphExec` 中的指定节点。

**函数签名**

```cpp
suError_t sudrvGraphNodeSetEnabled(suTaskGraphExec_t graphExec,
                                   suTaskGraphNode_t node,
                                   unsigned int isEnabled);
```

**参数列表**

- `graphExec`[in]：设置指定节点的可执行图
- `node`[in]：实例化 `graphExec` 的图表中的节点
- `isEnabled`[in]：如果`isEnabled` != 0 则启用节点，否则禁用节点

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

设置`graphExec`中有`node`所表示的节点为启用或禁用，`isEnabled` = 1 为启用，反之则禁用。

### sudrvGraphReleaseUserObject

从任务图中释放用户对象引用。

**函数签名**

```cpp
suError_t sudrvGraphReleaseUserObject(suTaskGraph_t graph,
                                      suUserObject_t object,
                                      unsigned int count);
```

**参数列表**

- `graph`[in]：要从中释放对象引用的任务图
- `object`[in]：需要释放的对象
- `count`[in]：释放的引用数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**
释放任务图`graph`拥有的用户对象`object`引用数`count`次。

### sudrvGraphRetainUserObject

增加对任务图中用户对象的引用。

**函数签名**

```cpp
suError_t sudrvGraphRetainUserObject(suTaskGraph_t graph, suUserObject_t object,
                                     unsigned int count, unsigned int flags);
```

**参数列表**

- `graph`[in]：要从中释放对象引用的任务图
- `object`[in]：需要释放的对象
- `count`[in]：增加的引用数
- `flags`[in]：标志参数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

增加对图`graph`中用户对象`object`的引用`count`次。

### sudrvGraphUpload

在流中上传可执行图。

**函数签名**

```cpp
suError_t sudrvGraphUpload(suTaskGraphExec_t graphExec, suStream_t stream);
```

**参数列表**

- `graphExec`[in]：要上传的可执行图的句柄
- `stream`[in]：上传到的流的句柄

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

提前上传`graphExec`到流`stream`以提高后续启动可执行图的性能。

### sudrvUserObjectCreate

创建一个用户对象。

**函数签名**

```cpp
suError_t sudrvUserObjectCreate(suUserObject_t *objectOut, void *ptr,
                                suHostFn_t destroy,
                                unsigned int initialRefcount,
                                unsigned int flags);
```

**参数列表**

- `objectOut`[out]：返回用户对象句柄
- `ptr`[in]：传递给销毁函数的指针
- `destroy`[in]：当用户对象不再使用时的回调函数
- `initialRefcount`[in]：初始引用计数
- `flags`[in]：标志

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

在`*objectOut`中返回新创建的用户对象。该用户对象所管理的指针`ptr`在引用计数为0时调用`destroy` 来释放自己相关的资源。 用户对象的初始应用计数为`initialRefcount`。

### sudrvUserObjectRelease

释放对用户对象的引用。

**函数签名**

```cpp
suError_t sudrvUserObjectRelease(suUserObject_t object, unsigned int count);
```

**参数列表**

- `object`[in]：要释放的用户对象句柄
- `count`[in]：释放的引用数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

释放用户对象`object`的引用计数`count`次。如果引用计数达到零，则调用对象的析构函数。

### sudrvUserObjectRetain

增加对用户对象的引用。

**函数签名**

```cpp
suError_t sudrvUserObjectRetain(suUserObject_t object, unsigned int count);
```

**参数列表**

- `object`[in]：要增加引用的用户对象句柄
- `count`[in]：增加的引用数

**返回值**

- `suSuccess`
- `suErrorInvalidValue`

**描述**

增加用户对象`object`的引用计数`count`次。

##  资源占用

### sudrvOccupancyMaxActiveBlocksPerMultiprocessor

返回设备函数的占用率信息。

**函数签名**

```cpp
suError_t sudrvOccupancyMaxActiveBlocksPerMultiprocessor(
    int *numBlocks, suDevFunc_t function, int blockSize,
    size_t dynamicSMemSize);
```

**参数列表**

- `numBlocks`[in]： 返回占用率
- `func`[in]：要计算占用率的内核函数
- `blockSize`[in]：内核启动时使用的块大小
- `dynamicSMemSize`[in]：每个块的动态共享内存使用量（以字节为单位）

**返回值**

- `suSuccess`
- `suErrorInvalidDevice`
- `suErrorInvalidDeviceFunction`
- `suErrorInvalidValue`

**描述**

在 `*numBlocks` 中返回运行设备函数的每个流处理多处理器的最大活动块数。


### sudrvOccupancyMaxActiveBlocksPerMultiprocessorWithFlags

返回具有指定标志的设备函数的占用率。

**函数签名**

```cpp
suError_t sudrvOccupancyMaxActiveBlocksPerMultiprocessorWithFlags(
    int *numBlocks, suDevFunc_t function, int blockSize, size_t dynamicSMemSize,
    unsigned int flags);
```

**参数列表**

- `numBlocks`[in]： 返回占用率
- `func`[in]：要计算占用率的内核函数
- `blockSize`[in]：内核启动时使用的块大小
- `dynamicSMemSize`[in]：每个块的动态共享内存使用量（以字节为单位）
- `flags`[in]： 标志参数

**返回值**

- `suSuccess`
- `suErrorInvalidDevice`
- `suErrorInvalidDeviceFunction`
- `suErrorInvalidValue`

**描述**

在 `*numBlocks` 中返回运行设备函数的每个流处理多处理器的最大活动块数。

### sudrvOccupancyMaxPotentialBlockSize

返回实现设备功能最大潜在占用率的网格和块大小。

**函数签名**

```cpp
suError_t sudrvOccupancyMaxPotentialBlockSize(
    int *minGridSize, int *blockSize, suDevFunc_t function,
    suOccupancyB2DSize blockSizeToDynamicSMemSize, int blockSizeLimit);
```

**参数列表**

- `minGridSize`[out]：返回实现最佳潜在占用率所需的最小网格
- `blockSize`[out]：返回的块大小
- `func`[in]：设备核函数符号
- `dynamicSMemSize`[in]：每个块的动态共享内存使用量（以字节为单位）
- `blockSizeLimit`[in]：核函数`func`能够支持的最大的块大小 。0 表示无限制。

**返回值**

- `suSuccess`
- `suErrorInvalidDevice`
- `suErrorInvalidDeviceFunction`
- `suErrorInvalidValue`

**描述**

在 `*minGridSize` 和 `*blocksize` 中返回一个建议的网格/块大小，该对实现最佳潜在占用率（即 最小块数）。

### sudrvOccupancyMaxPotentialBlockSizeWithFlags

返回实现设备功能最大潜在占用率的网格和块大小。

**函数签名**

```cpp
suError_t sudrvOccupancyMaxPotentialBlockSizeWithFlags(
    int *minGridSize, int *blockSize, suDevFunc_t function,
    suOccupancyB2DSize blockSizeToDynamicSMemSize, int blockSizeLimit,
    unsigned int flags);
```

**参数列表**

- `minGridSize`[out]：返回最小网格大小
- `blockSize`[out]：返回的块大小
- `function`[in]：核函数
- `blockSizeToDynamicSMemSize`[in]：一个回调函数，它返回动态共享内存的大小
- `blockSizeLimit`[in]：核函数`func`能够支持的最大的块大小 。0 表示无限制。
- `flags`[in]：标志参数

**返回值**

- `suSuccess`
- `suErrorInvalidDevice`
- `suErrorInvalidDeviceFunction`
- `suErrorInvalidValue`

**描述**

在`*dynamicSmemSize` 中返回 `CU` 上允许 核函数`func`运行`numBlocks` 块时动态共享内存的最大大小。

### sudrvOccupancyAvailableDynamicSMemPerBlock

在 `CU` 上启动 `numBlocks` 块时返回每个块可用的动态共享内存。

**函数签名**

```cpp
suError_t sudrvOccupancyAvailableDynamicSMemPerBlock(size_t *dynamicSmemSize,
                                                     suDevFunc_t function,
                                                     int numBlocks,
                                                     int blockSize);
```

**参数列表**

- `dynamicSmemSize`[out]：返回的最大动态共享内存
- `function`[in]：核函数
- `numBlocks`[in]：`CU` 上适合的块数
- `blockSize`[in]：块大小

**返回值**

- `suSuccess`
- `suErrorInvalidDevice`
- `suErrorInvalidDeviceFunction`
- `suErrorInvalidValue`

**描述**

在`*dynamicSmemSize` 中返回 `CU` 上允许 核函数`func`运行`numBlocks` 块时动态共享内存的最大的大小。

##  对等上下文内存访问

### sudrvContextDisablePeerAccess

禁用对对等设备上上下文的内存分配的直接访问。

**函数签名**

```cpp
suError_t sudrvContextDisablePeerAccess(suContext peerContext);
```

**参数列表**

- `peerContext`[in]： 用于禁用直接访问的对等设备的上下文

**返回值**

- `suSuccess`
- `suErrorInvalidDevice`
- `suErrorPeerAccessNotEnabled`

**描述**

- 如果尚未启用从当前设备直接访问`peerContext`上的内存，则返回 `suErrorPeerAccessNotEnabled`。
- 如果启用了则返回`suSuccess`。

### sudrvContextEnablePeerAccess

允许直接访问对等设备上的上下文上的内存。

**函数签名**

```cpp
suError_t sudrvContextEnablePeerAccess(suContext peerContext,
                                       unsigned int flags);
```

**参数列表**

- `peerContext`[in]： 对等设备的上下文，支持从当前设备直接访问
- `flags`[in]：保留供将来使用，必须设置为 0

**返回值**

- `suSuccess`
- `suErrorInvalidDevice`
- `suErrorPeerAccessAlreadyEnabled`
- `suErrorInvalidValue`

**描述**

设置当前设备可以访问 `peerContext` 上的分配的内存。

### sudrvDeviceCanAccessPeer

查询设备是否可以直接访问对等设备的内存。

**函数签名**

```cpp
suError_t sudrvDeviceCanAccessPeer(int *canAccessPeer, suDevice device,
                                   suDevice peerDevice);
```

**参数列表**

- `canAccessPeer`[out]：返回访问能力，1为可以，0 为不可以
- `device`[in]：直接访问 `peerDevice` 的发起设备
- `peerDevice`[in]：需要被访问的设备

**返回值**

- `suSuccess`
- `suErrorInvalidDevice`

**描述**

如果设备能够直接访问对等设备`peerDevice`的内存，则在`*canAccessPeer` 中返回值 1，否则返回值 0。如果需要从设备直接访问 `peerDevice`，则可以通过调用 `sudrvContextEnablePeerAccess()`来启用访问。

### sudrvDeviceGetP2PAttribute

查询两个设备之间的链路属性。

**函数签名**

```cpp
suError_t sudrvDeviceGetP2PAttribute(int *value, suDeviceP2PAttr attr,
                                     suDevice srcDevice, suDevice dstDevice);
```

**参数列表**

- `value`[out]：所请求属性的返回值
- `attr`[in]：需要查询的相关属性， 目前只支持`suDevP2PAttrAccessSupported`
- `srcDevice`[in]：链接的源设备。
- `dstDevice`[in]：链接的目标设备。

**返回值**

- `suSuccess`
- `suErrorInvalidValue`
- `suErrorInvalidDevice`

**描述**

在`*value` 中返回 `srcDevice` 和 `dstDevice` 之间链接的属性 `attr` 的值。支持的属性有：

- `suDevP2PAttrAccessSupported`

##  性能分析控制

### sudrvProfilerStart

启用分析工具。

**函数签名**

```cpp
suError_t sudrvProfilerStart(void);
```


**参数列表**
> 无

**返回值**

- `suSuccess`

**描述**

在当前上下文中开始收集性能分析数据。如果已经启用，则 `sudrvProfilerStart()`直接返回`suSuccess`。

### sudrvProfilerStop

停用分析工具。

**函数签名**

```cpp
suError_t sudrvProfilerStop(void);
```

**参数列表**
> 无

**返回值**

- `suSuccess`

**描述**

在当前上下文中停止收集性能分析数据。如果分析已停止，则 `sudrvProfilerStop()`直接返回。

## 法律声明

**著作权 ©**

壁仞科技 2020-2023，版权所有。未经壁仞科技事先书面许可，本文档内容不得以任何形式将其复制、修改、出版、传输或发布。

**商标。**

本文档所包含的任何壁仞科技的商号、商标、图形标志和域名，均为壁仞科技所有。未经壁仞科技事先书面许可，不得以任何形式将其复制、修改、出版、传输或发布。

**性能信息**。

本文档中所包含的性能指标包括设计规格、模拟测试指标以及特定环境下的测试和评估指标。设计规格为产品设计时拟定的指标，仅用于提供信息的目的而供您参考，实测指标将以具体的测试数据为准。模拟测试指标是通过在体系结构模拟器上运行模拟而获得，仅用于提供信息目的。该类测试的系统硬件、软件设计或配置的任何不同都可能影响实际性能。特定环境下的测试和评估指标系采用特定的计算机系统或组件操作而获得，可反映出我司产品的大致性能。系统硬件、软件设计或配置的任何不同都可能影响实际性能。

**前瞻性陈述。**

本文档的信息可能包含前瞻性陈述，可能存在风险和不确定性。请勿仅依赖于上述信息做出您的商业决定。

**注意。**

本产品后续可能进行版本升级，本文档内容会不定期更新。除非在合同中另有约定，本文档仅作产品使用指导，其中的信息和建议不构成任何明示或暗示的担保。