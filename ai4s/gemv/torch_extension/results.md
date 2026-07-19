# GEMV SUPA + PyTorch Extension Results

## Environment

- SUPA SDK: `/usr/local/birensupa/sdk/1.11.0.0.rc2`
- Python extension route: `torch` + `torch_br` + manual `brcc --supa-link`

## Build

Command:

```bash
cd /workspace/br_competition/gemv/torch_extension
./build.sh
```

Result: PASS

## Correctness and error-path tests

Command:

```bash
LD_LIBRARY_PATH=/usr/local/lib/python3.10/dist-packages/torch/lib:/usr/local/lib/python3.10/dist-packages/torch_br/lib:/usr/local/birensupa/sdk/1.11.0.0.rc2/supa/lib:$LD_LIBRARY_PATH \
  python3 test_gemv_ext.py
```

Output:

```text
{'torch': '1.12.1+cpu', 'supa_empty_ok': 'supa:0'}
{'case': 'small_64x64', 'shape': '64x64', 'max_abs': 2.384185791015625e-07, 'max_rel': 2.384185791015625e-07, 'ok': True}
{'case': 'wide_257x1024', 'shape': '257x1024', 'max_abs': 6.67572021484375e-06, 'max_rel': 3.248453140258789e-06, 'ok': True}
{'case': 'large_4096x512', 'shape': '4096x512', 'max_abs': 5.7220458984375e-06, 'max_rel': 2.6226043701171875e-06, 'ok': True}
{'case': 'bad_x_shape', 'caught': 'RuntimeError', 'ok': True}
{'case': 'bad_A_dtype', 'caught': 'RuntimeError', 'ok': True}
{'benchmark': 'perf_4096x1024', 'avg_ms': 2.948307991027832, 'output_device': 'supa:0'}
{'task': 'gemv_supa_pytorch_extension', 'ok': True}
```

Verdict: PASS

## Notes

- Inputs are constructed on CPU, then copied to `device='supa'`.
- The extension accepts ordinary row-major PyTorch tensors with shape `[M,K]`.
- The `.su` kernel runs on SUPA and writes to a SUPA tensor allocated by the C++ wrapper.
- Final link must use `brcc --supa-link`; plain `g++ -shared` is not sufficient for SUPA device code.
