import copy
from typing import Dict

from sqlalchemy import String, Column, Float, Integer, text, create_engine, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from logbook.entities import Accelerator

Base = declarative_base()
engine = create_engine('sqlite:///imec.db')
Session = sessionmaker(bind=engine)
session = Session()


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


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




