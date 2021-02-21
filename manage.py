from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api import create_app, db
from api.database.models import Item
from tests import db_drop_everything

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)

# manage migrations
manager.add_command('db', MigrateCommand)


@manager.command
def routes():
    print(app.url_map)


@manager.command
def db_seed():
    db_drop_everything(db)
    db.create_all()

    # seed anything here we might need
    item1 = Item(name='beard trimmer', category='toiletries', weather='all', gender='male')
    item2 = Item(name='dress', category='clothing', weather='hot', gender='female')
    item3 = Item(name='underwear', category='clothing', weather='all', gender='all')
    item4 = Item(name='birth control', category='toiletries', weather='all', gender='female')
    item5 = Item(name='toothbrush', category='toiletries', weather='all', gender='all')
    item6 = Item(name='toothpaste', category='toiletries', weather='all', gender='all')
    item7 = Item(name='phone', category='essentials', weather='all', gender='all')
    item8 = Item(name='phone charger', category='essentials', weather='all', gender='all')
    item9 = Item(name='cologne', category='toiletries', weather='all', gender='male')
    item10 = Item(name='diapers', category='child 0-2', weather='all', gender='all')

    db.session.add(item1)
    db.session.add(item2)
    db.session.add(item3)
    db.session.add(item4)
    db.session.add(item5)
    db.session.add(item6)
    db.session.add(item7)
    db.session.add(item8)
    db.session.add(item9)
    db.session.add(item10)

    db.session.commit()
    print(f'obj count: {len(db.session.query(Item).all())}')


if __name__ == "__main__":
    manager.run()
