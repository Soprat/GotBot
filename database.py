import psycopg2
import logging
from dotenv import dotenv_values

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel('DEBUG')


class Database:
    file_ids: list
    caption: str = None
    config = dotenv_values('.env')

    def __init__(self):

        self.connection = psycopg2.connect(database=self.config['DATABASE'],
                                           host=self.config['HOST'],
                                           user=self.config['USER'],
                                           password=self.config['PASSWORD'],
                                           port=5432)
        self.cursor = self.connection.cursor()

    def create_cluster(self, cluster_id: int,
                       targets: list[int | str],
                       donors: list[int | str],
                       text_to_delete: str,
                       text_to_set: str) -> str | Exception:

        tables = ["targets", "donors", "texts"]
        args = (targets, donors, (text_to_delete, text_to_set))
        response = ''
        try:

            for table in tables:
                if table == 'texts':
                    self.cursor.execute(
                        f"INSERT INTO {table} "
                        f"VALUES ({cluster_id}, '{text_to_delete}', '{text_to_set}')")
                    print(table, cluster_id, text_to_delete, text_to_set)
                    self.connection.commit()
                else:
                    for arg in args[tables.index(table)]:
                        print(table, cluster_id, arg)
                        self.cursor.execute(f'INSERT INTO {table} '
                                            f'VALUES ({cluster_id},{arg})')
                        self.connection.commit()

            return f'cluster {cluster_id} created successfully'
        except Exception as e:
            return e

    def get_cluster(self, cluster_id: int) -> list[tuple] | None:
        try:
            self.cursor.execute(
                f'SELECT donors.cluster_id, donors.donor_id, targets.target_id, texts.del_text,texts.set_text '
                f'FROM donors '
                f'RIGHT JOIN targets ON {cluster_id} = targets.cluster_id '
                f'RIGHT JOIN texts ON {cluster_id} = texts.cluster_id;')
            values = self.cursor.fetchall()
            return values

        except Exception as e:
            logger.error(e)
            return None

    def get_cluster_id(self, donor: int | str) -> int:
        """tables: donors, targets, texts
           columns: (cluster_id, donor_id), (cluster_id, target_id), (cluster_id, black_text, text_to_set) """
        try:
            self.cursor.execute(f"SELECT cluster_id "
                                f"FROM donors "
                                f"WHERE donor_id = '{donor}';")
            values = self.cursor.fetchone()[0]
            return values
        except Exception as e:
            logger.error(e)
            return -1

    def get_max_id(self) -> int:
        print('seeking of max')
        try:
            self.cursor.execute(f"SELECT MAX(cluster_id) "
                                f"FROM donors;")
            maximum = self.cursor.fetchone()[0]
            if maximum is not None:
                return maximum
            else:
                return 0
        except Exception as e:
            logger.error(e)
            return 0

    def edit_text(self, cluster_id: int, new_text_to_set: str, new_text_to_del: str) -> dict[str, str] | None:
        try:
            self.cursor.execute(
                f"UPDATE TABLE texts "
                f"SET del_text={new_text_to_del}, new_text={new_text_to_set} "
                f"WHERE cluster_id={cluster_id};")
            self.cursor.commit()
            return {'cluster_id': cluster_id, 'text_to_set': new_text_to_set, 'text_to_del': new_text_to_del}
        except Exception as e:
            logger.error(e)
            return None

    def get_all_donors(self):
        try:
            self.cursor.execute(
                f"SELECT donors FROM donors;")
            response = self.cursor.fetchall()
            return [*response]
        except Exception as e:
            logger.error(e)
            return None
