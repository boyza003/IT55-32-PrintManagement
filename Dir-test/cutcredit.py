__author__ = 'BoyChaiwat'

import time
import pymysql
import sys

conn2boylogin = pymysql.connect(host='boylogin.me', user='boy', passwd='boylogin', db='mydb')
cur2boylogin = conn2boylogin.cursor()

checklast = 0
checkloopcreditcut = 0
def cutcredit(stdid, jobfrom, jobid):
    global checklast
    global checkloopcreditcut
    while True:
        f = open('/var/log/cups/page_log', 'r', encoding='utf-8')
        linelist = f.readlines()
        f.close()
        if linelist[len(linelist) - 1] != checklast:
            x = jobfrom + " " + str(jobid)
            if linelist[len(linelist) - 1].find(x) > 0:
                cur2boylogin.execute("UPDATE JOB SET page = page + 1 WHERE job_id = %s", jobid)
                cur2boylogin.execute("UPDATE CREDIT SET credit_balance = credit_balance -1, credit_used = credit_used +1, last_print = NOW() WHERE student_id = %s", stdid)
                checklast = linelist[len(linelist) - 1]
                print("cut", checkloopcreditcut)
                print(linelist[len(linelist) - 1] == linelist)
        elif checkloopcreditcut == 500:
            print("out creditcut()")
            break
        print(checkloopcreditcut)
        checkloopcreditcut += 1
        time.sleep(2)

cutcredit("bd080100e36831680462", "BoyChaiwat", 75)
#, credit_used = credit_used +1, last_print = NOW()