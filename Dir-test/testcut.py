__author__ = 'BoyChaiwat'

import os
import time
import pymysql

conn2boylogin = pymysql.connect(host='128.199.132.148', port=3306, user='boy', passwd='boylogin', db='mydb')
cur2boylogin = conn2boylogin.cursor()
count = 121

def cutcredit(stdid, jobid):
    global count
    while True:
        check = os.popen("sudo lpstat -o").read()
        if check.find("EPSON_T13") >= 0:
            count += 1
            print("+")
        elif count > 0:
            count = count/15
            print(count)
            cur2boylogin.execute("UPDATE CREDIT SET credit_balance = credit_balance - %s, credit_used = credit_used + %s, last_print = NOW() WHERE student_id = %s", (int(count), int(count), stdid))
            cur2boylogin.execute("UPDATE JOB SET page = %s,job_out = NOW(), STUDENT_id = %s WHERE job_id = %s", (int(count), stdid, jobid))
            break
    time.sleep(1)

cutcredit("bd080100a6a2793304fe", "1000")
