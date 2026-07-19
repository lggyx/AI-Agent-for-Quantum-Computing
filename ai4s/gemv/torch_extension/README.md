# GEMV SUPA + PyTorch Extension

This directory demonstrates the second development route: wrapping a SUPA kernel as a Python-callable PyTorch extension.

The operator computes row-major SGEMV with ordinary PyTorch `[M,K]` tensors:

```text
y[M] = A[M,K] * x[K]
A[m,k] = A[m * K + k]
```

The Python test constructs inputs on CPU, copies them to `device='supa'`, calls the extension, synchronizes with `torch_br`, and compares against a CPU reference.

## Build

```bash
./build.sh
```

## Run

```bash
LD_LIBRARY_PATH=/usr/local/lib/python3.10/dist-packages/torch/lib:/usr/local/lib/python3.10/dist-packages/torch_br/lib:/usr/local/birensupa/sdk/1.11.0.0.rc2/supa/lib:$LD_LIBRARY_PATH \
  python3 test_gemv_ext.py
```
