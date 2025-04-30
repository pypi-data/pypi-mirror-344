"""Chinese number <=> int/float conversion for Python3.8+

Example:

```python

>>> from pycnnum import cn2num, num2cn
>>> from pycnnum import cn2num, num2cn
>>> cn2num("一百二十三")
123
>>> num2cn(123)
'一百二十三'
>>> cn2num("一兆零四十五", numbering_type="mid")
1000000000045
>>> num2cn(2400, alt_2=True)
'两千四'
>>> num2cn(3.4)
'三点四'

```

- `.pycnnum.cn2num`
- `.pycnnum.num2cn`
"""

from .__version__ import __version__
from .pycnnum import cn2num, num2cn
