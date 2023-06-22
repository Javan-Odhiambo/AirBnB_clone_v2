#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship

place_amenity = Table('place_amenity',
                      Base.metadata, Column('place_id', String(60),
                                            ForeignKey('places.id'),
                                            primary_key=True,
                                            nullable=False), Column(
                                                'amenity_id', String(60),
                                                ForeignKey('amenities.id'),
                                                primary_key=True,
                                                nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    if models.storage_type == 'db':
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship('Review', backref='place',
                               cascade='all, delete')
        amenities = relationship('Amenity', secondary='place_amenity',
                                 back_populates='place_amenities',
                                 viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """returns the list of Review instances with
            place_id equals to the current Place.id"""
            from models import storage
            from models.review import Review
            related_reviews = []
            reviews = storage.all(Review)
            for review in reviews.values():
                if review.place_id == self.id:
                    related_reviews.append(review)
            return related_reviews

        @property
        def amenities(self):
            """returns the list of Amenity instances based on the attribute
            amenity_ids that contains all Amenity.id linked to the Place"""
            from models import storage
            from models.amenity import Amenity
            related_amenities = []
            amenities = storage.all(Amenity)
            for amenity in amenities.values():
                if amenity.id in self.amenity_ids:
                    related_amenities.append(amenity)
            return related_amenities
