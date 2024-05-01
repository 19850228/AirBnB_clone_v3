class DBStorage:
    ...
    
    def get(self, cls, id):
        """Retrieve one object by ID."""
        if cls and id:
            return self.__session.query(cls).filter_by(id=id).first()
        return None
    
    def count(self, cls=None):
        """Count the number of objects in storage."""
        if cls:
            return self.__session.query(cls).count()
        return sum(self.__session.query(cls).count() for cls in self.classes.values())
