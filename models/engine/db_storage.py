#!/usr/bin/python3
"""
Database storage engine
"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    __engine = None
    __session = None
    classes = ["Amenity", "User", "Place", "State", "City", "Review"]

    def __init__(self):
        """ Initialization of Database """
        self.user = getenv('HBNB_MYSQL_USER', 'hbnb_test')
        self.pwd = getenv('HBNB_MYSQL_PWD', 'hbnb_test_pwd')
        self.host = getenv('HBNB_MYSQL_HOST', 'localhost')
        self.db = getenv('HBNB_MYSQL_DB', 'hbnb_test_db')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(self.user, self.pwd,
                                             self.host, self.db),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        dictionary = {}

        if cls:
            for instance in self.__session.query(cls).all():
                key = f"{cls.__name__}.{instance.id}"
                dictionary[key] = instance
        else:
            for name in self.classes:
                c_name = eval(name)
                for instance in self.__session.query(c_name).all():
                    key = f"{c_name.__name__}.{instance.id}"
                    dictionary[key] = instance
        return dictionary

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        """
        calls close on the class Session
        """
        self.__session.close()
