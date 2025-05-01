# 🧩 Defaultable
 
**Defaultable** is a lightweight Python package that provides abstract base classes for defining "default" instances in your own classes — useful for fallbacks, comparisons, initialization patterns, or clean APIs.
 
It supports both:
- ✅ Public default behavior via `Defaultable`
- 🔒 Internal default behavior via `InternalDefaultable`
 
---
 
## 🚀 Installation
 
Install the package from PyPI:
 
```
pip install defaultable
```
 
---
 
## 📦 Usage Examples
 
### 🔹 Public: Using `Defaultable`
 
Use the `Defaultable` base class when you want to expose a public default instance for your class.
 
```python
from defaultable import Defaultable
 
class ComplexNumber(Defaultable):
    def __init__(self, re: float, im: float):
        self.re = re
        self.im = im
 
    @classmethod
    def default(cls):
        return cls(1.0, 0.0)  # Default is 1 + 0j
 
    def __eq__(self, other):
        return isinstance(other, ComplexNumber) and self.re == other.re and self.im == other.im
 
    def __repr__(self):
        return f"({self.re} + {self.im}j)
```
 
Usage:
 
```python
>>> c = ComplexNumber.default()
>>> print(c)
(1.0 + 0.0j)
 
>>> ComplexNumber.is_default(c)
True
```
 
---
 
### 🔸 Internal: Using `InternalDefaultable`
 
Use the `InternalDefaultable` base class when you need internal logic for a default instance, without exposing it to the public API.
 
```python
from defaultable import InternalDefaultable
 
class Complex(InternalDefaultable):
    def __init__(self, re: float, im: float):
        self.re = re
        self.im = im
 
    @classmethod
    def _default(cls):
        return cls(0.0, 0.0)  # Internal default is 0 + 0j
 
    def __bool__(self):
        default_complex = self._default()
        return self.im != default_complex.im or self.re != default_complex.re
```
 
Internal usage:
 
```python
>>> my_complex = Complex(0, 0)
>>> bool(my_complex)
False
```
 
> 🔒 `InternalDefaultable` is designed for internal/private use. Its methods are prefixed with underscores and should not be exposed in public APIs.
 
---
 
## 📄 License
 
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
 
---
 
## 🛠️ Contributing
 
Contributions are welcome! Feel free to open issues or pull requests on [GitHub](https://github.com/fidtal24/defaultable).
 
---
 
## 🔗 Links
 
- [PyPI Package](https://pypi.org/project/defaultable/)
- [GitHub Repository](https://github.com/fidtal24/defaultable)
