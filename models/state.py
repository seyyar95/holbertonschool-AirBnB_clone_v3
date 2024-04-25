#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.city import City
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    name = Column(
            String(128),
            nullable=False
            )
    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", cascade="all, delete", backref="state")
    else:
        @property
        def cities(self):
            """ Returns the list of City instances with state_id """
            from models import storage
            city_instances = []
            cities = storage.all(City)
            for obj in cities.values():
                if obj.state_id == self.id:
                    city_instances.append(obj)
            return city_instances
