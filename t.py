import torch

print(f"PyTorch 版本: {torch.__version__}")
print(f"CUDA 是否可用: {torch.cuda.is_available()}")
print(f"MPS 是否可用: {getattr(torch.backends, 'mps', None) and torch.backends.mps.is_available()}")