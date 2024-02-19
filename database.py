import psycopg2
from aiogram.types import PhotoSize


class Database:
    def __init__(self):

        self.file_ids = []
        self.caption = None

        self.connection = psycopg2.connect(database="aichrrdb",
                                           host="surus.db.elephantsql.com",
                                           user="aichrrdb",
                                           password="cghCrs8TTwRTpxXsBT_yD7FaIaBYMAey",
                                           port=5432)
        self.cursor = self.connection.cursor()

    def send(self, caption: str, file_ids: list[str], file_formats: list[str]) -> tuple | Exception:
        values_list = (caption, *(file_ids[:10]), *(file_formats[:10]))
        try:
            self.cursor.execute(f"INSERT INTO message VALUES {values_list}")
            self.connection.commit()
            return values_list
        except Exception as e:
            return e

    def get(self, caption: str) -> tuple | Exception:
        try:
            self.cursor.execute(f"SELECT * FROM message WHERE caption = '{caption}'")
            values = self.cursor.fetchone()
            return values
        except Exception as e:
            return e
