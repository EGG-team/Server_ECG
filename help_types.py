# -*- coding: utf-8 -*-
import pymysql


class DbWorker:
    """
    docs here
    """
    # TODO remove data
    host = 'localhost'
    user = 'root'
    password = 'myivan'
    db_name = 'ecg_db'

    def __init__(self, host=host, user=user, password=password,
                 db_name=db_name):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name

    def create_db(self):
        con = self.__get_con()
        cursor = con.cursor()

        cursor.execute(
            """-- auto-generated definition
CREATE TABLE IF NOT EXISTS users
(
  id          BIGINT UNSIGNED AUTO_INCREMENT
    PRIMARY KEY,
  name     VARCHAR(150)   NOT NULL,
  password VARCHAR(255)   NOT NULL,
  CONSTRAINT users_id_name_uindex
  UNIQUE (id, name)
)
  ENGINE = InnoDB;

"""
        )
        con.commit()

    def __get_con(self):
        con = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db_name,
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )

        return con

    def get_all_users(self):
        con = self.__get_con()
        cursor = con.cursor()

        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()

        cursor.close()
        con.close()

        return data

    def get_user(self, user_id):
        con = self.__get_con()
        cursor = con.cursor()

        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id, ))
        data = cursor.fetchone()

        cursor.close()
        con.close()

        return data

    def add_new_user(self, username, password):
        con = self.__get_con()
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO users (name, password) "
                           "VALUES (%s, %s)", (username, password))

            con.commit()

            cursor.execute("SELECT LAST_INSERT_ID()")
            user_id = cursor.fetchone()['LAST_INSERT_ID()']
        except pymysql.IntegrityError:
            con.rollback()
            user_id = -1
        finally:
            cursor.close()
            con.close()

        return self.get_user(user_id)


if __name__ == '__main__':
    worker = DbWorker()

    worker.create_db()
