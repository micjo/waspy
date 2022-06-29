from pathlib import Path
from logbook.sqlite_db import SqliteDb


def make_trend(sql_db):
    sql_db.sql_insert("""create table trend
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
    );""")
    sql_db.sql_insert("""create unique index trend_id_uindex
    on trend (id);""")


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
            job    text
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
            recipe      text,
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
        create table rbs_single_step_book
        (
            recipe_id integer
                references recipe_book,
            axis      float,
            position  float
        );
    """)

    sql_db.sql_insert("""
        create table rbs_stepwise_book
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
        create table rbs_stepwise_least_book
        (
            recipe_id            integer
                references recipe_book,
            axis                 text,
            start                float,
            end                  float,
            step                 float,
            yield_positions      text,
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



def make_imec_db(filename:str):
    sql_db = SqliteDb(Path(filename))
    make_trend(sql_db)
    make_log_book(sql_db)
    make_job_book(sql_db)
    make_recipe_book(sql_db)
    make_rbs_recipe_books(sql_db)
