class FileStorage:
    ...
    
    def get(self, cls, id):
        """Retrieve one object by ID."""
        key = "{}.{}".format(cls.__name__, id)
        return self.__objects.get(key)
    
    def count(self, cls=None):
        """Count the number of objects in storage."""
        if cls:
            return sum(1 for obj in self.__objects.values() if type(obj) == cls)
        return len(self.__objects)
