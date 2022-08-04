from sqlalchemy import String, Column, Float, Integer, text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///imec.db')
Session = sessionmaker(bind=engine)
session = Session()


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
    oven_power_percentage = Column("oven_power_percentage", Integer)
    oven_temperature_celsius = Column("oven_temperature_celsius", Integer)
    ionizer_current_A = Column("ionizer_current_A", Float)
    ionizer_voltage_V = Column("ionizer_voltage_V", Float)
    cathode_probe_voltage_kV = Column("cathode_probe_voltage_kV", Float)
    cathode_probe_current_mA = Column("cathode_probe_current_mA", Float)
