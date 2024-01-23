import psycopg2
from aiogram.types import PhotoSize


class Database:
    def __init__(self):

        self.file_ids = []
        self.caption = None

        connection = psycopg2.connect(database="aichrrdb",
                                      host="surus.db.elephantsql.com",
                                      user="aichrrdb",
                                      password="cghCrs8TTwRTpxXsBT_yD7FaIaBYMAey",
                                      port=5432)
        self.cursor = connection.cursor()

        message_columns_list = ['caption', 'file0_id', 'file1_id', 'file2_id',
                                'file3_id', 'file4_id', 'file5_id', 'file6_id',
                                'file7_id', 'file8_id', 'file9_id', 'media_group']

        self.message_columns = ''
        for x in message_columns_list:
            self.message_columns += x

    def send(self, file_ids: list[list[PhotoSize]], caption: str, media_group: int) -> str | Exception:
        file_ids = file_ids[0]
        values_list = [caption, file_ids[0].file_id, file_ids[1].file_id, file_ids[2].file_id,
                       file_ids[3].file_id, file_ids[4].file_id, file_ids[5].file_id, file_ids[6].file_id,
                       file_ids[7].file_id, file_ids[8].file_id, file_ids[9].file_id, media_group]
        values = ''
        for x in values_list:
            values += x
        try:
            self.cursor.execute(f"INSERT INTO message ({self.message_columns}) VALUES ({values})")
            return values
        except Exception as e:
            return e