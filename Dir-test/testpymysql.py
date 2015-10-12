import pymysql
from random import randint
import time
import datetime
i = 0


def testdb():
    global i
    inp = randint(1, 4)
    cur2boylogin = pymysql.connect(host='128.199.201.78', port=3306, user='boy', passwd='boylogin', db='mydb')
    cur2boylogin = cur2boylogin.cursor()
    cur2boylogin.execute("SELECT * FROM POOL WHERE id = %s", str(inp))
    row = cur2boylogin.fetchone()
    i += 1
    print(str(i), datetime.datetime.now(), row)


while True:
    testdb()
    time.sleep(1)
