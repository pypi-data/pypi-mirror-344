import numpy as np
from typing import Callable, Dict
from .core import TransformativeHarmonization

class MatrixHarmonization(TransformativeHarmonization):
    """Matrisler için dönüşümsel uyumlaştırma."""
    
    def __init__(self, harmony_function: Callable[[np.ndarray, np.ndarray, Dict], np.ndarray] = None, context: Dict = None):
        """Matris uyumlaştırma sınıfını başlatır.
        
        Args:
            harmony_function: Özelleştirilmiş uyum fonksiyonu.
            context: Bağlam parametreleri (weight, scale).
        """
        super().__init__(harmony_function or self._matrix_harmony, context)

    def _matrix_harmony(self, m1: np.ndarray, m2: np.ndarray, context: Dict) -> np.ndarray:
        """Matrisler için uyum fonksiyonu.
        
        Args:
            m1: Birinci matris.
            m2: İkinci matris.
            context: Bağlam parametreleri (weight, scale).
            
        Returns:
            Uyumlaştırılmış matris.
            
        Raises:
            ValueError: Matris boyutları uyuşmazsa.
        """
        if m1.shape != m2.shape:
            raise ValueError("Matrisler aynı boyutta olmalı.")
        trace_avg = np.sqrt((np.trace(m1.T @ m1) + np.trace(m2.T @ m2)) / 2) * context.get('scale', 1.0)
        similarity = np.trace(m1 @ m2.T) / (np.linalg.norm(m1) * np.linalg.norm(m2) + 1e-10)
        return trace_avg * similarity * (m1 + m2) / (np.linalg.norm(m1 + m2) + 1e-10)