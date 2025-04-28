class AbstractQuantityTypeData:
    def __init__(self) -> None:
        self._sorted=None
        pass

    def __len__(self):
        return NotImplemented
    
    def toJsonDict(self):
        return NotImplemented