from sqlalchemy import create_engine, String, text, Float
from sqlalchemy import Column, Integer, Text, MetaData, Table
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from alembic.migration import MigrationContext
from alembic.operations import Operations


engine = create_engine('sqlite:///file.db')
Session = sessionmaker(bind=engine)
session = Session()

conn = engine.connect()
ctx = MigrationContext.configure(conn)
op = Operations(ctx)

def automap():
    Base = automap_base()
    Base.prepare(autoload_with=engine)


def decl_base():
    Base = declarative_base()

    class Accelerator(Base):
        __tablename__ = "Accelerator"
        id = Column('id', Integer, primary_key=True)
        area = Column('area', String)
        power = Column('power', Float)
        date = Column('date', Integer, server_default=text("(strftime(\'%s\', \'now\')) not null"))

    Base.metadata.create_all(bind=engine)
    params = session.query(Accelerator).all()
    for entry in params:
        print(entry.__dict__)


def without_decl_base():
    metadata = MetaData()
    messages = Table('messages', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('message',Text))

    messages.create(bind=engine)
    insert_message = messages.insert().values(message='Hello, World!')
    engine.execute(insert_message)

    from sqlalchemy import select
    stmt = select([messages.c.message])
    message, = engine.execute(stmt).fetchone()
    print(message)


def add_and_drop_column():
    op.add_column('Accelerator',
                  Column('oven_power_percentage', String())
                  )
    op.drop_column('Accelerator', 'oven_power_percentage')


decl_base()
automap()
