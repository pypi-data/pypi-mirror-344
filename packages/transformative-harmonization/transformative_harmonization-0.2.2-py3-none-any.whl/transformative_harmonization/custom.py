from typing import Callable, Dict
from .core import TransformativeHarmonization

class CustomHarmonization(TransformativeHarmonization):
    """Özelleştirilmiş uyum fonksiyonları için sınıf."""
    
    def __init__(self, harmony_function: Callable[[any, any, Dict], any], context: Dict = None):
        """Özelleştirilmiş uyum fonksiyonunu başlatır.
        
        Args:
            harmony_function: Kullanıcı tanımlı uyum fonksiyonu.
            context: Bağlam parametreleri.
            
        Raises:
            ValueError: Eğer harmony_function callable değilse.
        """
        if not callable(harmony_function):
            raise ValueError("harmony_function bir callable olmalı.")
        super().__init__(harmony_function, context)