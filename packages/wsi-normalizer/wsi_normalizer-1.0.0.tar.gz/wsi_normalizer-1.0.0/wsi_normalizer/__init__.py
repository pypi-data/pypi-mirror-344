from wsi_normalizer.norm_tools import MacenkoNormalizer, ReinhardNormalizer, VahadaneNormalizer
try:
    import torch
    from wsi_normalizer.torchvahadane import TorchVahadaneNormalizer
    if not torch.cuda.is_available():
        ImportError('CUDA is not ready, import failed')
    else:
        print('CUDA is ready, Vahadane GPU version is available')
    normalizer = TorchVahadaneNormalizer(device='cuda', staintools_estimate=True)
    __all__ = ['MacenkoNormalizer', 'ReinhardNormalizer', 'VahadaneNormalizer', 'TorchVahadaneNormalizer']
except ImportError as e:
    print(f'Fallback to CPU version \n {e}')
    normalizer = VahadaneNormalizer()
    __all__ = ['MacenkoNormalizer', 'ReinhardNormalizer', 'VahadaneNormalizer']
