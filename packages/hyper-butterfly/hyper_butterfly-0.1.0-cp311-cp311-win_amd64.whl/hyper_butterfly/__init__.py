import torch
from torch.autograd import Function
import sys
sys.modules['hb'] = sys.modules[__name__]

from ._C import (
    log_map_origin_cpu,
    exp_map_origin_cpu,
    hyper_butterfly_cpu,
)
_has_cuda = False
if torch.cuda.is_available():
    try:
        from ._C import (
            log_map_origin_cuda,
            exp_map_origin_cuda,
            hyper_butterfly_cuda,
            hyper_butterfly_backward_cuda,   # ← backward 바인딩
        )
        _has_cuda = True
    except ImportError:
        _has_cuda = False

from .hyper_butterfly_py import hyper_butterfly_py

class HyperButterflyFunction(Function):
    @staticmethod
    def forward(ctx, x, params, c, L):
        ctx.save_for_backward(x, params)
        ctx.c, ctx.L = c, L
        if x.is_cuda and _has_cuda:
            y, u, v = hyper_butterfly_cuda(x, params, torch.empty(0,device=x.device), c, L)
        else:
            if not x.is_cuda and 'hyper_butterfly_cpu' in globals():
                y, u, v = hyper_butterfly_cpu(x, params, c, L)
            else:
                y = hyper_butterfly_py(x, params, c, L)
        return y

    @staticmethod
    def backward(ctx, grad_out):
        x, params = ctx.saved_tensors
        c, L = ctx.c, ctx.L
        # CUDA backward available?
        if x.is_cuda and _has_cuda:
            grad_x, grad_p = hyper_butterfly_backward_cuda(
                grad_out.contiguous(), x, params, c, L
            )
            return grad_x, grad_p, None, None
        # fallback to pure-PyTorch autograd
        with torch.enable_grad():
            x_req = x.detach().requires_grad_()
            p_req = params.detach().requires_grad_()
            y = hyper_butterfly_py(x_req, p_req, c, L)
            gx, gp = torch.autograd.grad(y, (x_req, p_req), grad_out)
        return gx, gp, None, None

def hyper_butterfly(x: torch.Tensor, params: torch.Tensor, c: float, L: int):
    return HyperButterflyFunction.apply(x, params, c, L)


# 
# import torch
# from torch.autograd import Function
# 
# # C++/CUDA bindings
# from ._C import (
#     matmul,
#     log_map_origin_cpu,
#     exp_map_origin_cpu,
#     hyper_butterfly_cpu,
# )
# _has_cuda = False
# if torch.cuda.is_available():
#     try:
#         from ._C import (
#             log_map_origin_cuda,
#             exp_map_origin_cuda,
#             hyper_butterfly_cuda,
#         )
#         _has_cuda = True
#     except ImportError:
#         _has_cuda = False
# 
# # Pure-PyTorch fallback
# from .hyper_butterfly_py import hyper_butterfly_py
# 
# # Autograd-aware wrapper
# class HyperButterflyFunction(Function):
#     @staticmethod
#     def forward(ctx, x, params, c, L):
#         ctx.save_for_backward(x, params)
#         ctx.c, ctx.L = c, L
#         # Try C++ extension if available
#         if x.is_cuda and _has_cuda:
#             y, u, v = hyper_butterfly_cuda(x, params, torch.empty(0, device=x.device), c, L)
#         else:
#             # CPU extension or fallback
#             if not x.is_cuda and 'hyper_butterfly_cpu' in globals():
#                 y, u, v = hyper_butterfly_cpu(x, params, torch.empty(0), c, L)
#             else:
#                 y = hyper_butterfly_py(x, params, c, L)
#         return y
# 
#     @staticmethod
#     def backward(ctx, grad_out):
#         x, params = ctx.saved_tensors
#         c, L = ctx.c, ctx.L
#         with torch.enable_grad():
#             x_req = x.detach().requires_grad_()
#             p_req = params.detach().requires_grad_()
#             y = hyper_butterfly_py(x_req, p_req, c, L)
#             grads = torch.autograd.grad(y, (x_req, p_req), grad_out)
#         return grads[0], grads[1], None, None
# 
# def hyper_butterfly(x: torch.Tensor, params: torch.Tensor, c: float, L: int) -> torch.Tensor:
#     return HyperButterflyFunction.apply(x, params, c, L)
