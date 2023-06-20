

class Resource:
    """
    """
    _name: str = None
    _data: bytearray = None

    def __init__(self, name: str = None, data: bytearray = None):
        self._name = name or "basicname.txt"
        self._data = data or []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def __eq__(self, other) -> bool:
        return isinstance(other, Resource) and self.name == other.name

    def __neq__(self, other) -> bool:
        return not self == other

    def __len__(self) -> int:
        return len(self.data)

    def __hash__(self):
        return hash(self.name)

    def add_data(self, data_to_add: bytes) -> None:
        self.data.extend(data_to_add)

    def remove_data(self, start_index: int, end_index: int) -> None:
        del self.data[start_index:end_index]

    def copy_data(self, start_index: int = None, end_index: int = None) -> bytearray:
        start_index = start_index or 0
        end_index = end_index or len(self.data)
        return self.data[start_index:end_index].copy()

    def replace_data(self, start_index: int, end_index: int, replacement_data: bytes) -> None:
        self.data[start_index:end_index] = replacement_data

    def copy(self) -> "Resource":
        copied_data = self.data.copy()
        return Resource(name=self.name, data=copied_data)
