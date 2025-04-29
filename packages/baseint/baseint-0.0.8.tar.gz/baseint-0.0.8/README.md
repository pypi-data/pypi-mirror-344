# baseint
BaseInt is a small Python library for converting numbers in arbitrary bases.

## Features
- Create BaseInt instances from integers, strings, lists and tuples.
- Convert between bases easily.
- Supports custom character maps.

## Example

```py
from baseint import BaseInt

b = BaseInt("1111", 2)
print(b.toDecimal())        # 15
print(f"{b.sconvert(8)!r}") # BI:8:17
```