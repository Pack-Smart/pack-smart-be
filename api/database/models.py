import bleach
from sqlalchemy import Column, String, Integer
from api import db


class Item(db.Model):
    """
    Item Model
    """
    __tablename__ = 'items'

    # Auto-incrementing, unique primary key
    id = Column(Integer, primary_key=True)
    # unique item
    name = Column(String(80), nullable=False)
    # category
    category = Column(String(100), nullable=False)
    # weather
    weather = Column(String(80), nullable=False)
    # gender
    gender = Column(String(80), nullable=False)

    def __init__(self, name, category, weather, gender):
        if name is not None:
            name = bleach.clean(name).strip()
            if name == '':
                name = None

        if category is not None:
            category = bleach.clean(category).strip()
            if category == '':
                category = None

        if weather is not None:
            weather = bleach.clean(weather).strip()
            if weather == '':
                weather = None

        if gender is not None:
            gender = bleach.clean(gender).strip()
            if gender == '':
                gender = None

        self.name = name
        self.category = category
        self.weather = weather
        self.gender = gender

    def insert(self):
        """
        inserts a new model into a database
        the model must have a unique username
        the model must have a unique id or null id
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        updates a new model into a database
        the model must exist in the database
        """
        db.session.commit()

    def delete(self):
        """
        deletes model from database
        the model must exist in the database
        """
        db.session.delete(self)
        db.session.commit()
