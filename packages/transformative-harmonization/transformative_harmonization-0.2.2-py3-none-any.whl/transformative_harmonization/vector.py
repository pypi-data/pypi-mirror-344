import numpy as np
from typing import Callable, Dict
from .core import TransformativeHarmonization

class VectorHarmonization(TransformativeHarmonization):
    """Vektörler için dönüşümsel uyumlaştırma, makine öğrenimi için optimize edilmiş."""
    
    def __init__(self, harmony_function: Callable[[np.ndarray, np.ndarray, Dict], np.ndarray] = None, context: Dict = None):
        """Vektör uyumlaştırma sınıfını başlatır.
        
        Args:
            harmony_function: Özelleştirilmiş uyum fonksiyonu.
            context: Bağlam parametreleri (weight, scale).
        """
        super().__init__(harmony_function or self._vector_harmony, context)

    def _vector_harmony(self, v1: np.ndarray, v2: np.ndarray, context: Dict) -> np.ndarray:
        """Vektörler için uyum fonksiyonu.
        
        Args:
            v1: Birinci vektör.
            v2: İkinci vektör.
            context: Bağlam parametreleri (weight, scale).
            
        Returns:
            Uyumlaştırılmış vektör.
            
        Raises:
            ValueError: Vektör boyutları uyuşmazsa.
        """
        if v1.shape != v2.shape:
            raise ValueError("Vektörler aynı boyutta olmalı.")
        norm_avg = np.sqrt((np.linalg.norm(v1)**2 + np.linalg.norm(v2)**2) / 2) * context.get('scale', 1.0)
        cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-10)
        # Sıfır benzerlikten kaçınmak için küçük bir düzeltme
        similarity = np.cos(context.get('weight', 1.0) * np.arccos(np.clip(cos_theta, -1.0, 1.0))) + 1e-3
        result = norm_avg * similarity * (v1 + v2)
        # Sıfır vektörü kontrolü
        if np.allclose(result, 0):
            return np.zeros_like(v1)
        return result / (np.linalg.norm(result) + 1e-10)