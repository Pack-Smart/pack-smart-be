from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api import create_app, db
from api.database.models import Item
from tests import db_drop_everything

import psycopg2

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

    conn = psycopg2.connect("host=localhost dbname=pack_smart_dev user=postgres")
    cur = conn.cursor()
    with open('items.csv', 'r') as f:
        next(f) # Skip the header row.
        cur.copy_from(f, 'items', sep=',')

    conn.commit()

    db.session.commit()

    conn = psycopg2.connect("host=localhost dbname=pack_smart_test user=postgres")
    cur = conn.cursor()
    with open('items.csv', 'r') as f:
        next(f) # Skip the header row.
        cur.copy_from(f, 'items', sep=',')

    conn.commit()

    db.session.commit()
    print(f'obj count: {len(db.session.query(Item).all())}')


if __name__ == "__main__":
    manager.run()
