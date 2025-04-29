CHARMAP="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class BaseInt:
    """
    A class for handling integers in arbitrary bases.
    
    Arguments:
        values:     (int, str, list, tuple): The initial value.
        base:        int =      10: The base of the number.
        forceUpper: bool =    True: Force uppercase when parsing string values.
        charmap:     str = CHARMAP: The character map for digit representation.
    """
    def __init__(self,values,base=10,forceUpper=True,charmap=CHARMAP):
        self.charmap=CHARMAP
        if base>len(charmap): raise ValueError(f"Base {base} is bigger than the length of the charmap!")
        elif base<=1: raise ValueError("Base must be 2 or higher")

        if isinstance(values,int):
            if base!=10: raise ValueError(f"Base is {base}, but an integer was provided.")
            self.values=[int(c) for c in str(values)]
        elif isinstance(values,str):
            if forceUpper:
                self.values=[self.charmap.index(c.upper()) for c in values]
            else:
                self.values=[self.charmap.index(c) for c in values]
        elif isinstance(values,tuple): self.values=list(self.values)
        elif isinstance(values,list): self.values=values
        else: raise TypeError(f"Unsupported type: {type(values)}")
        self.base=base
        for i,v in enumerate(self.values):
            if v>=self.base: raise ValueError(f"One of the values ({v} at index {i}) is higher or equal to the base")
    def string(self):
        """Returns the digits represented as a string. Uses self.charmap."""
        return "".join(map(lambda v: self.charmap[v],self.values))
    def __repr__(self):
        """Returns the string representation containing the base and self.string()."""
        return f"BI:{self.base}:{self.string()}"
    def __str__(self):
        """Returns self.string()."""
        return self.string()
    def toDecimal(self):
        """Converts the number to base 10."""
        current=1
        result=0
        for v in reversed(self.values):
            result+=v*current
            current*=self.base
        return result
    @staticmethod
    def dec2base(n,base):
        """Converts a decimal number to a BaseInt in the given base."""
        if base==10: return BaseInt(n,base)
        if n==0:
            return BaseInt([0],base)
        res=[]
        while n>0:
            res.append(n%base)
            n//=base
        res.reverse()
        return BaseInt(res,base)
    def sconvert(self,base):
        """Returns a new BaseInt converted to the new base."""
        dec=self.toDecimal()
        return BaseInt.dec2base(dec,base)
    def convert(self,base):
        """In-place conversion to the new base."""
        conv=self.sconvert(base)
        self.base=conv.base
        self.values=conv.values
