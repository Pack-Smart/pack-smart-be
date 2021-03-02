from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean
from api import db
from sqlalchemy.orm import relationship, backref
class Item(db.Model):
    """
    Item Model
    """
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    item = Column(String(80), nullable=False)
    category = Column(String(100), nullable=False)
    weather = Column(String(80), nullable=False)
    gender = Column(String(80), nullable=False)

    packing_lists = relationship("PackingLists", secondary="item_lists")

    def insert(self):
        db.session.add(self)
        db.session.commit()

class Users(db.Model):
    """
    User Model
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)

    packing_lists = relationship("PackingLists")

    def insert(self):
        db.session.add(self)
        db.session.commit()

class PackingLists(db.Model):
    """
    Packing Lists Model
    """
    __tablename__ = 'packing_lists'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    num_of_days = Column(Integer, nullable=False)
    destination = Column(String(80), nullable=False)

    custom_items = relationship("CustomItem")
    items = relationship("Item",secondary="item_lists")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class ItemLists(db.Model):
    """
    Item Lists Model
    """
    __tablename__ = 'item_lists'

    id = Column(Integer, primary_key=True)
    packing_list_id = Column(Integer, ForeignKey('packing_lists.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    quantity = Column(Integer, nullable=False)
    is_checked = Column(Boolean, nullable=False)

    packing_lists = relationship(PackingLists, backref=backref("item_lists", cascade="all, delete-orphan"))
    items = relationship(Item, backref=backref("item_lists", cascade="all, delete-orphan"))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class CustomItem(db.Model):
    """
    Custom Item Model
    """
    __tablename__ = 'custom_items'

    id = Column(Integer, primary_key=True)
    item = Column(String(20), nullable=False)
    quantity = Column(Integer, nullable=False)
    is_checked = Column(Boolean, nullable=False)
    category = Column(String(20), nullable=False)
    packing_list_id = Column(Integer, ForeignKey('packing_lists.id'))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()