from fastapi import FastAPI
import sqlite3
from datetime import datetime


def add_logbook_routes(router: FastAPI):
    @router.post("/log_message")
    async def log_message(message: str):
        con = sqlite3.connect('hive.db')
        cur = con.cursor()

        answer = cur.execute("""
            INSERT INTO log_book (type, message)
            VALUES ('message', '{message}');
        """.format(message=message)
                             )

        con.commit()
        con.close()
        return

    @router.post("/log_rbs_start")
    async def log_message(rbs_name: str):
        con = sqlite3.connect('hive.db')
        cur = con.cursor()
        print("rbs start" + rbs_name)

        answer = cur.execute("""
            INSERT INTO log_book (type, message)
            VALUES ('rbs_service', 'RBS {rbs_name} started');
        """.format(rbs_name=rbs_name))
        con.commit()
        con.close()
        return answer.lastrowid

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
        return answer.lastrowid
