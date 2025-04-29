import math
import numpy as np
from typing import Union, Callable, Any, Dict

class TransformativeHarmonization:
    """Dönüşümsel Uyumlaştırma işlemini gerçekleştiren ana sınıf.
    
    Bu sınıf, sayılar veya matematiksel nesneler üzerinde bağlamsal uyumlaştırma yapar.
    Varsayılan uyum fonksiyonu, enerji ortalaması ve benzerlik oranını birleştirir.
    Bağlam parametreleri ile özelleştirilebilir.
    
    Attributes:
        harmony_function: Kullanıcı tanımlı veya varsayılan uyum fonksiyonu.
        context: Bağlam parametreleri (örn. ağırlık, ölçek).
    """
    
    def __init__(self, harmony_function: Callable[[Any, Any, Dict], Any] = None, context: Dict = None):
        """Uyum fonksiyonunu ve bağlamı başlatır.
        
        Args:
            harmony_function: Özelleştirilmiş uyum fonksiyonu. Varsayılan None ise temel fonksiyon kullanılır.
            context: Bağlam parametreleri (örn. {'weight': 1.0, 'scale': 1.0}).
        """
        self.harmony_function = harmony_function or self._default_harmony
        self.context = context or {'weight': 1.0, 'scale': 1.0}

    def _default_harmony(self, a: float, b: float, context: Dict) -> float:
        """Temel uyum fonksiyonu: Enerji ortalaması ve benzerlik oranı.
        
        Args:
            a: Birinci sayı.
            b: İkinci sayı.
            context: Bağlam parametreleri (weight, scale).
            
        Returns:
            Uyumlaştırılmış değer.
            
        Raises:
            ZeroDivisionError: Eğer a + b = 0 ise.
        """
        if a + b == 0:
            return 0.0
        energy_avg = math.sqrt((a**2 + b**2) / 2) * context.get('scale', 1.0)
        similarity = math.cos(context.get('weight', 1.0) * abs(a - b) / (a + b))
        return energy_avg * similarity

    def harmonize(self, *args: Union[float, np.ndarray], context: Dict = None) -> Union[float, np.ndarray]:
        """Verilen nesneleri uyumlaştırır.
        
        Args:
            *args: Uyumlaştırılacak sayılar veya nesneler (en az 2).
            context: Opsiyonel bağlam parametreleri. Varsayılan olarak sınıfın context'i kullanılır.
            
        Returns:
            Uyumlaştırılmış değer.
            
        Raises:
            ValueError: Eğer 2'den az nesne sağlanırsa.
        """
        if len(args) < 2:
            raise ValueError("En az iki nesne gerekli.")
        
        context = context or self.context
        result = args[0]
        for i in range(1, len(args)):
            result = self.harmony_function(result, args[i], context)
        return result

    @property
    def is_commutative(self) -> bool:
        """Uyum fonksiyonunun değişme özelliği var mı?"""
        return True  # Varsayılan fonksiyon simetrik (a, b) = (b, a)

    @property
    def is_associative(self) -> bool:
        """Uyum fonksiyonunun birleşme özelliği var mı?"""
        return False  # Varsayılan fonksiyon genelde birleşmez

    def continuity(self, a: float, b: float) -> bool:
        """Fonksiyonun süreklilik özelliği.
        
        Args:
            a, b: Test edilecek sayılar.
            
        Returns:
            bool: Sürekli ise True, değilse False.
        """
        try:
            self.harmonize(a, b)
            return True
        except ZeroDivisionError:
            return False