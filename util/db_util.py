import pymysql

conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="12345678", database="test")
cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
try:
    cur.execute("select * from `case`;")
    data = cur.fetchall()
    print(data)
except Exception as e:
    print(e)

finally:
    conn.close()
