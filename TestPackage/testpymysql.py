__author__ = 'BoyChaiwat'

import pymysql

conn2boylogin = pymysql.connect(host='boylogin.me', user='print', passwd='boylogin', db='mydb')
cur2boylogin = conn2boylogin.cursor()
cur2boylogin.execute("SELECT status FROM CREDIT WHERE student_id = %s", datarx)
row = cur2boylogin.fetchone()
print(row)