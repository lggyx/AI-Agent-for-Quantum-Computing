import time

import torch
import torch_br

import gemv_supa_ext


def make_inputs(M, K, seed):
    gen = torch.Generator(device='cpu')
    gen.manual_seed(seed)
    A = torch.empty((M, K), dtype=torch.float32, device='cpu')
    x = torch.empty((K,), dtype=torch.float32, device='cpu')
    A.uniform_(-0.5, 0.5, generator=gen)
    x.uniform_(-0.5, 0.5, generator=gen)
    return A.contiguous(), x.contiguous()


def compare(expected, actual):
    diff = (expected - actual).abs()
    max_abs = float(diff.max().item()) if diff.numel() else 0.0
    denom = torch.maximum(expected.abs(), torch.ones_like(expected))
    max_rel = float((diff / denom).max().item()) if diff.numel() else 0.0
    ok = max_abs <= 1.0e-3 or max_rel <= 1.0e-4
    return ok, max_abs, max_rel


def run_case(name, M, K, seed):
    A_cpu, x_cpu = make_inputs(M, K, seed)
    expected = torch.mv(A_cpu, x_cpu)

    # Construct on CPU and then copy to SUPA. Avoid relying on torch_br coverage
    # for input construction ops; the tested computation is the SUPA extension.
    A = A_cpu.to('supa').contiguous()
    x = x_cpu.to('supa').contiguous()
    y = gemv_supa_ext.gemv(A, x)
    torch_br.supa.synchronize()
    actual = y.cpu()

    ok, max_abs, max_rel = compare(expected, actual)
    print({
        'case': name,
        'shape': f'{M}x{K}',
        'max_abs': max_abs,
        'max_rel': max_rel,
        'ok': ok,
    })
    if not ok:
        raise AssertionError(f'{name} failed max_abs={max_abs} max_rel={max_rel}')


def run_bad_shape_case():
    A_cpu, x_cpu = make_inputs(8, 4, 777)
    A = A_cpu.to('supa').contiguous()
    x = x_cpu[:3].to('supa').contiguous()
    try:
        gemv_supa_ext.gemv(A, x)
    except RuntimeError as exc:
        print({'case': 'bad_x_shape', 'caught': type(exc).__name__, 'ok': True})
        return
    raise AssertionError('bad_x_shape did not raise')


def run_bad_dtype_case():
    A_cpu, x_cpu = make_inputs(8, 4, 888)
    A = A_cpu.double().to('supa').contiguous()
    x = x_cpu.to('supa').contiguous()
    try:
        gemv_supa_ext.gemv(A, x)
    except RuntimeError as exc:
        print({'case': 'bad_A_dtype', 'caught': type(exc).__name__, 'ok': True})
        return
    raise AssertionError('bad_A_dtype did not raise')


def run_benchmark():
    M, K = 4096, 1024
    A_cpu, x_cpu = make_inputs(M, K, 999)
    A = A_cpu.to('supa').contiguous()
    x = x_cpu.to('supa').contiguous()

    for _ in range(3):
        gemv_supa_ext.gemv(A, x)
    torch_br.supa.synchronize()

    iters = 20
    t0 = time.time()
    for _ in range(iters):
        y = gemv_supa_ext.gemv(A, x)
    torch_br.supa.synchronize()
    avg_ms = (time.time() - t0) * 1000.0 / iters
    print({'benchmark': 'perf_4096x1024', 'avg_ms': avg_ms, 'output_device': str(y.device)})


def main():
    print({'torch': torch.__version__, 'supa_empty_ok': str(torch.empty((1,), device='supa').device)})
    run_case('small_64x64', 64, 64, 100)
    run_case('wide_257x1024', 257, 1024, 200)
    run_case('large_4096x512', 4096, 512, 300)
    run_bad_shape_case()
    run_bad_dtype_case()
    run_benchmark()
    print({'task': 'gemv_supa_pytorch_extension', 'ok': True})


if __name__ == '__main__':
    main()
