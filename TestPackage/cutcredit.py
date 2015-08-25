__author__ = 'BoyChaiwat'

import time
import pymysql

conn2boylogin = pymysql.connect(host='boylogin.me', user='boy', passwd='boylogin', db='mydb')
cur2boylogin = conn2boylogin.cursor()

checklast = 0
checkloopcreditcut = 0
def cutcredit(stdid, jobfrom, jobid):
    global checklast
    global checkloopcreditcut
    while True:
        f = open('page_log', 'r')
        linelist = f.readlines()
        f.close()
        if linelist[len(linelist) - 1] != checklast:
            x = jobfrom + " " + str(jobid)
            if linelist[len(linelist) - 1].find(x) > 0:
                cur2boylogin.execute("UPDATE JOB SET page = page + 1 WHERE job_id = %s", jobid)
                cur2boylogin.execute("UPDATE CREDIT SET credit_balance = credit_balance -1, credit_used = credit_used +1, last_print = NOW() WHERE student_id = %s", stdid)
                checklast = linelist[len(linelist) - 1]
                checkloopcreditcut = 1
            elif (linelist[len(linelist) - 1].find(x) < 0) & checkloopcreditcut == 1:
                print("out creditcut()")
                checkloopcreditcut = 0
                break
            else:
                print("Wait cutcreadit() job :", jobid)

        time.sleep(1)


cutcredit("bd080100e368316804622", "BoyChaiwat", 24)
