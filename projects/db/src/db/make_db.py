from pathlib import Path

from db.db_orm import Base
from db.sqlite_db import SqliteDb
import sys
from sqlalchemy import create_engine


def make_log_book(sql_db):
    sql_db.sql_insert("""
        create table log_book
        (
            log_id integer not null
                constraint log_book_pk
                    primary key autoincrement,
            epoch  integer default (strftime('%s', 'now')) not null,
            mode   text,
            note   text,
            meta   blob);
    """)
    sql_db.sql_insert("""
        create unique index log_book_log_id_uindex
            on log_book (log_id);
    """)


def make_job_book(sql_db):
    sql_db.sql_insert("""
        create table job_book
        (
            log_id integer
                references log_book,
            job_id integer
                references job_name_book
        );
    """)

    sql_db.sql_insert("""
        create table job_name_book
        (
            job_id integer not null
                constraint log_book_pk
                    primary key autoincrement,
            name text
        );
    """)


def make_recipe_book(sql_db):
    sql_db.sql_insert("""
        create table recipe_book
        (
            recipe_id   integer
                constraint job_book_pk
                    primary key autoincrement,
            log_id      integer
                references log_book,
            job_id      integer
                references job_name_book,
            name      text,
            type        text,
            sample      text,
            start_epoch integer,
            end_epoch   integer
        );
    """)

    sql_db.sql_insert("""
            create unique index job_book_recipe_id_uindex
            on recipe_book (recipe_id);
    """)

def make_rbs_recipe_books(sql_db):

    sql_db.sql_insert("""
        create table rbs_random_book
        (
            recipe_id integer
                references recipe_book,
            axis      text,
            start     float,
            end       float,
            step      float
        );
    """)

    sql_db.sql_insert("""
        create table rbs_angular_yield_book
        (
            recipe_id            integer
                references recipe_book,
            axis                 text,
            start                float,
            end                  float,
            step                 float,
            least_yield_position float
        );
    """)

    sql_db.sql_insert("""
        create table rbs_yield_book
        (
            recipe_id            integer
                references recipe_book,
            angle                float,
            yield                int
        );
    """)


def make_erd_recipe_book(sql_db):
    sql_db.sql_insert("""
        create table erd_book
        (
            recipe_id integer
                references recipe_book,
            beam_type            text,
            beam_energy_MeV     float,
            sample_tilt_degrees float,
            measuring_time_sec int,
            theta float,
            z_start float,
            z_end float,
            z_increment float,
            z_repeat int,
            average_terminal_voltage float
        );
    """)


def make_imec_trend(sql_db):
    sql_db.sql_insert("""
    create table trend
    (
        id                   integer
            constraint trend_pk
                primary key autoincrement,
        epoch                int default (strftime('%s', 'now')),
        rbs_x                float,
        rbs_y                float,
        rbs_phi              float,
        rbs_zeta             float,
        rbs_current          float,
        erd_ad1_count_rate   float,
        erd_ad2_count_rate   float,
        erd_z                float,
        erd_theta            float,
        any_sf6_temperature  float,
        any_sf6_pressure     float,
        any_motor_current    float,
        any_terminal_voltage float,
        any_magnet_current   float
    );
    """)

    sql_db.sql_insert("""
    create unique index trend_id_uindex
        on trend (id);
        """)



def make_vdg_trend(sql_db):
    sql_db.sql_insert(
    """
    create table trend
    (
        id                     integer
            constraint trend_pk
                primary key autoincrement,
        epoch                  INTEGER default (strftime('%s', 'now')),
        vdg_current            float,
        vdg_accumulated_charge float,
        vdg_terminal_voltage   float,
        vdg_radiation_us_h     float,
        vdg_charge_timestamp   TEXT
    );
    """)

    sql_db.sql_insert("""
    create unique index trend_id_uindex
        on trend (id);
    """)


def make_day_book(sql_db):
    sql_db.sql_insert("""
        create table day_book
    (
        id    INTEGER not null
            constraint day_book_pk
                primary key autoincrement,
        epoch INTEGER default (strftime('%s', 'now')) not null,
        entry TEXT
    );
    """)
    sql_db.sql_insert("""
    create unique index day_book_id_uindex
        on day_book (id);
    """)


def make_accelerator(engine):
    Base.metadata.create_all(bind=engine)


def make_imec_db(filename:str):
    sql_db = SqliteDb(Path(filename))
    make_log_book(sql_db)
    make_job_book(sql_db)
    make_recipe_book(sql_db)
    make_rbs_recipe_books(sql_db)
    make_erd_recipe_book(sql_db)
    make_imec_trend(sql_db)


def make_vdg_db(filename:str):
    sql_db = SqliteDb(Path(filename))
    make_vdg_trend(sql_db)


if __name__ == "__main__":
    if sys.argv[1] == "imec":
        print("Generating sqlite db for imec lab")
        make_imec_db("imec.db")
        engine = create_engine('sqlite:///imec.db')
        make_accelerator(engine)
    elif sys.argv[1] == "vdg":
        print("Generating sqlite db for vdg lab")
        make_vdg_db("vdg.db")


