#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
from models.review import Review


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    """ Adding SQLAlchemy Table """
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True,
                                 nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True,
                                 nullable=False)
                          )

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship('Review',
                               cascade='all, delete', backref='place')
        amenities = relationship('Amenity',
                                 secondary='place_amenity', viewonly=False)
    else:
        @property
        def reviews(self):
            reviewslist = models.storage.all(Review)
            new_list = []
            for obj in reviewslist.values():
                if obj.place_id == self.id:
                    new_list.append(obj)
            return (new_list)

        @property
        def amenities(self):
            """ Returns the list of Amenities """
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            if type(obj) is Amenity and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
