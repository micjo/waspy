import copy
from typing import Dict

from sqlalchemy import String, Column, Float, Integer, text, create_engine, insert, cast, JSON, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db.entities import Accelerator

Base = declarative_base()
engine = create_engine('sqlite:///imec.db')
Session = sessionmaker(bind=engine)
session = Session()


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


class DbDayBook(Base):
    __tablename__ = "day_book"
    id = Column('id', Integer, primary_key=True)
    epoch = Column('epoch', Integer, server_default=text("(strftime(\'%s\', \'now\')) not null"))
    entry = Column("entry", JSON)


class DbDayBookAccountFormat(Base):
    __tablename__ = "day_book_account_format"
    account = Column('account', String, primary_key=True)
    format = Column("format", JSON)


def add_account_entry(account, new_entry: Dict):
    entry_with_account = new_entry
    entry_with_account["account"] = account

    account_format = session.query(DbDayBookAccountFormat).filter(DbDayBookAccountFormat.account == account).first().format
    account_formatted_entry = {"account": account}
    for key in account_format:
        if key in new_entry:
            account_formatted_entry[key] = new_entry[key]

    new_value = DbDayBook(entry=account_formatted_entry)
    session.add(new_value)
    session.commit()


def get_entry_from_daybook(account, nr_of_entries):
    query = session.query(DbDayBook).filter(DbDayBook.entry['account'] == f'"{account}"').order_by(DbDayBook.epoch.desc()).limit(nr_of_entries)
    records = query[:]
    return records


def update_account_format(account, format):
    new_value = DbDayBookAccountFormat(account=account, format=format)
    session.merge(new_value)
    session.commit()


def get_daybook_all_formats():
    query = session.query(DbDayBookAccountFormat)
    records = query.all()
    available_keys = []

    for record in records:
        for parameter in record.format:
            available_keys.append(f'{record.account}/{parameter}')

    return available_keys


class DbAccelerator(Base):
    __tablename__ = "accelerator"
    id = Column('id', Integer, primary_key=True)
    epoch = Column('epoch', Integer, server_default=text("(strftime(\'%s\', \'now\')) not null"))
    area = Column("area", String)
    beam_description = Column("beam_description", String)
    beam_energy_MeV = Column("beam_energy_MeV", Float)
    snics_cathode_target = Column("snics_cathode_target", String)
    bias_voltage_kV = Column("bias_voltage_kV", Float)
    bias_current_mA = Column("bias_current_mA", Float)
    focus_voltage_kV = Column("focus_voltage_kV", Float)
    focus_current_mA = Column("focus_current_mA", Float)
    oven_power_percentage = Column("oven_power_percentage", Float)
    oven_temperature_celsius = Column("oven_temperature_celsius", Float)
    ionizer_current_A = Column("ionizer_current_A", Float)
    ionizer_voltage_V = Column("ionizer_voltage_V", Float)
    cathode_probe_voltage_kV = Column("cathode_probe_voltage_kV", Float)
    cathode_probe_current_mA = Column("cathode_probe_current_mA", Float)


def fill_in_entry(new_entry: Accelerator) -> Dict:
    entry = session.query(DbAccelerator).order_by(DbAccelerator.epoch.desc()).first()
    copied_entry = row2dict(entry)
    del copied_entry['id']
    del copied_entry['epoch']

    for x, y in new_entry.dict().items():
        if y:
            copied_entry[x] = y
        if copied_entry[x] == "None":
            del copied_entry[x]

    return copied_entry


def insert_dict(entry):
    new_value = DbAccelerator(**entry)
    session.add(new_value)
    session.commit()




