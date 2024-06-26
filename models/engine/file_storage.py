#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls:
            new_dict = {}
            for key, value in self.__objects.items():
                if value.__class__.__name__ == cls.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """
        Saves all objects to the storage.

        Args:
            obj: The object to be saved.
        """
        name = obj.__class__.__name__
        self.__objects[f"{name}.{obj.id}"] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it's inside
        if obj is equal to None does nothing
        """
        if obj:
            name = obj.__class__.__name__
            del self.__objects[f"{name}.{obj.id}"]
            self.save()

    def get(self, cls, id):
        """
        Returns the object based on the class and its ID,
        or None if not found
        """
        key = f'{cls.__name__}.{id}'
        objs = self.all(cls)
        try:
            return objs[key]
        except KeyError:
            return None

    def count(self, cls=None):
        """
        Returns the number of objects in storage matching the given class.
        If no class is passed, returns the count of all objects in storage.
        """
        objs = self.all(cls)
        return len(objs)

    def close(self):
        """ calls reload method for deserializing
            the JSON file to objects
        """
        self.reload()
