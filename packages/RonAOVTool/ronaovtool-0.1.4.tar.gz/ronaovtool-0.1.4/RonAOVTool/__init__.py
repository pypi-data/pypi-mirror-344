def hascode(text: str, hash_type: str="byte"):
    if not isinstance(text, str):
        raise TypeError(f"Expected 'str', not '{type(text).__name__}'.")
        
    if hash_type not in ["integer", "byte", "hex"]:
        raise ValueError("The value of hash_type must be 'integer', 'byte' or 'hex'.")
                
    _number = 0
    for _character in text.lower():
        _number = _number * 31 + ord(_character)
        _number &= 0xFFFFFFFF
        _number += 0x80000000
        _number &= 0xFFFFFFFF
        _number -= 0x80000000
        
    _byte = _number.to_bytes(4, byteorder="little", signed=True)
    _hex = _byte.hex()
    
    if hash_type == "integer":
        return _number
        
    elif hash_type == "byte":
        return _byte
        
    else:
        return _hex
        
class editAssetbundle:
    def __init__(self, data=None, filename=None):
        self.data = data
        self.filename = filename
    
    @classmethod
    def load(cls, filename):
        with open(filename, "rb") as file:
            data = file.read()
        return cls(data, filename)
    
    def checkPath(self, path):
        path_hashcode = hascode(path, 'byte')

        path_end = path.rfind('/') + 1
        name_path = path[path_end:]

        path_hashcode += hascode(name_path)
        return path_hashcode in self.data
    
    def changePath(self, original_path, new_path, skipNotFound=False):        
        if not self.data:
            raise ValueError("No data to change.")
        
        if not isinstance(self.data, bytes):
            raise TypeError(f"Data type must be 'bytes', not '{type(self.data).__name__}'.")
        
        original_path_hashcode = hascode(original_path, "byte")
        new_path_hashcode = hascode(new_path, "byte")

        original_end = original_path.rfind('/') + 1
        original_name = original_path[original_end:]
        
        new_end = new_path.rfind('/') + 1
        new_name = new_path[new_end:]

        original_path_hashcode += hascode(original_name, 'byte')
        new_path_hashcode += hascode(new_name, 'byte')

        if original_path_hashcode not in self.data and not skipNotFound:
            raise ValueError(f"The path '{original_path}' does not exist.")
            
        if new_path_hashcode in self.data:
            raise ValueError(f"The path '{new_path}' already exists.")
            
        self.data = self.data.replace(
            original_path_hashcode,
            new_path_hashcode
        )

    def save(self):
        if not self.filename:
            raise TypeError(f"Data type must be 'bytes', not '{type(self.data).__name__}'.")
        
        if not self.data:
            raise ValueError("No data to save.")
        
        if not isinstance(self.data, bytes):
            raise TypeError("Incorrect data type to save")
            
        with open(self.filename, "wb") as file:
            file.write(self.data)