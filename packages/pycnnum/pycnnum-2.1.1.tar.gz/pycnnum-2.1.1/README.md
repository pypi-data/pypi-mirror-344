# PyCNNUM

Convert numbers in Chinese string to/from `int`/`float`/`str` for Python3.8+.

[API document](https://zcold.github.io/pycnnum/pycnnum.html)

---

- [1. Install from PyPI](#1-install-from-pypi)
- [2. Install from Source](#2-install-from-source)
- [3. Examples](#3-examples)
- [4. Install Development Packages](#4-install-development-packages)

---

## 1. Install from PyPI

```bash
pip install pycnnum
```

## 2. Install from Source

```bash
# git is required
git clone https://github.com/zcold/pycnnum.git
cd pycnnum
python -m pip install .
```

## 3. Examples

```python

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

## 4. Install Development Packages

```bash
# example for working under Ubuntu 22.4
# git and python3.8-venv are required
git clone https://github.com/zcold/pycnnum.git pycnnum_dev
cd pycnnum_dev
python3.8 -m venv .venv
source .venv/bin/activate
python -m pip install .[dev] -U

```
