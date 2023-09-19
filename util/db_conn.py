import pymysql
from warnings import filterwarnings

filterwarnings("ignore", category=pymysql.Warning)


class MysqlDB:

    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="12345678", database="test")
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def query(self, sql, state=None):
        self.cur.execute(sql)
        if state == "all":
            date = self.cur.fetchall()
        else:
            date = self.cur.fetchone()
        return date

    def execute(self, sql):
        try:
            rows = self.cur.execute(sql)
            self.conn.commit()
            return rows
        except Exception as e:
            print("{0}".format(e))
            self.conn.rollback()


if __name__ == "__main__":
    mydb = MysqlDB()
    # r = mydb.query("select * from `case`")
    r = mydb.execute("insert into `case` (`app`) values('xd')")
    print(r)
