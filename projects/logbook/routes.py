from fastapi import FastAPI
import sqlite3
from datetime import datetime


def add_logbook_routes(router: FastAPI):
    @router.post("/log_message")
    async def log_message(message: str):
        con = sqlite3.connect('hive.db')
        cur = con.cursor()
        cur.execute("""
            INSERT INTO log_book (type, message)
            VALUES ('message', '{message}');
        """.format(message=message))
        con.commit()
        con.close()
        return

    @router.post("/log_rbs_start")
    async def log_rbs_start(rbs_name: str):
        con = sqlite3.connect('hive.db')
        cur = con.cursor()

        answer = cur.execute("""
            INSERT INTO log_book (type, message)
            VALUES ('rbs_service', 'RBS {rbs_name} started');
        """.format(rbs_name=rbs_name))
        con.commit()
        con.close()
        return answer.lastrowid

    @router.post("/log_rbs_end")
    async def log_rbs_end(rbs_name: str):
        con = sqlite3.connect('hive.db')
        cur = con.cursor()
        cur.execute("""
            INSERT INTO log_book (type, message)
            VALUES ('rbs_service', 'RBS {rbs_name} finished');
        """.format(rbs_name=rbs_name))
        con.commit()
        con.close()

    @router.post("/log_rbs_recipe_finish")
    async def log_rbs_recipe_finish(row_id: str, rbs: str, recipe_name: str):
        con = sqlite3.connect('hive.db')
        cur = con.cursor()

        answer = cur.execute("""
            INSERT INTO rbs_service_log (message_id, rbs_name, recipe_name)
            VALUES ('{id}', '{rbs}', '{recipe}');
        """.format(id=row_id, rbs=rbs, recipe=recipe_name))

        con.commit()
        con.close()

    @router.post("/log_trend")
    async def log_trend(trends: dict):
        columns = ",".join(list(trends.keys()))
        surround_values = ",".join(["'" + str(values) + "'" for values in trends.values()])

        print(columns)
        print(surround_values)

        con = sqlite3.connect('hive.db')
        cur = con.cursor()

        answer = cur.execute("""
             INSERT INTO trend ({columns})
             VALUES ({values});
        """.format(columns=columns, values=surround_values))

        con.commit()
        con.close()

    @router.get("/check_trending")
    async def check_trending():
        con = sqlite3.connect('hive.db')
        cur = con.cursor()

        answer = cur.execute("""
            SELECT name FROM pragma_table_info('trend');
        """)

        con.commit()
        response = answer.fetchall()
        column_list = [''.join(item) for item in response]
        con.close()
        return column_list

    @router.get("/get_trend")
    async def get_trend(start: datetime, end: datetime, id: str):
        con = sqlite3.connect('hive.db')
        cur = con.cursor()

        answer = cur.execute("""
           select datetime(utc, 'localtime') as timestamp, {id} from trend where datetime(utc, 'localtime') between '{start}' and '{end}'
        """.format(id=id, start=start, end=end))

        con.commit()
        response = answer.fetchall()
        con.close()
        return response
