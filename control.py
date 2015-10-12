__author__ = 'BoyChaiwat'

import serial
import pymysql
import time
import os


check = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.2)
#check = serial.Serial("/dev/tty.SLAB_USBtoUART", 115200, timeout=0.1)
selectkey = bytes([0xBA, 0x02, 0x01, 0xB9])
ledon = bytes([0xBA, 0x03, 0x40, 0x01, 0xF8])
ledoff = bytes([0xBA, 0x03, 0x40, 0x00, 0xF9])

conn2boylogin = pymysql.connect(host='boylogin.me', port=3306, user='boy', passwd='boylogin', db='mydb')
count = 0
checklast = 0
checkloopcreditcut = 0
cutstatus = 0
status = 0


'''def cutcredit(stdid, jobfrom, jobid):
    global check
    global checklast
    global checkloopcreditcut
    checkoutloop = "get-" + str(jobid)
    while True:
        check = os.popen("sudo lpstat -o").read()
        f = open('/var/log/cups/page_log', 'r', encoding='utf-8')
        linelist = f.readlines()
        f.close()
        if linelist[len(linelist) - 1] != checklast:
            print("goto cut")
            x = jobfrom + " " + str(jobid)
            if linelist[len(linelist) - 1].find(x) > 0:
                cur2boylogin.execute("UPDATE JOB SET page = page + 1 WHERE job_id = %s", jobid)
                cur2boylogin.execute("UPDATE CREDIT SET credit_balance = credit_balance -1, credit_used = credit_used +1, last_print = NOW() WHERE student_id = %s", stdid)
                checklast = linelist[len(linelist) - 1]
                print("cut", checkloopcreditcut)
                print(linelist[len(linelist) - 1] == linelist)
                checkloopcreditcut = 1
        elif (checkloopcreditcut == 1) & (check.find(checkoutloop) == -1):
            print("out creditcut()")
            checkloopcreditcut = 0
            break
        print("def cutcredit(stdid, jobfrom, jobid):")
        #print(checkloopcreditcut)
        #print(check.find(checkoutloop))
        time.sleep(2)
'''
'''def cutcredit(stdid, jobfrom, jobid):
    os.popen("sudo service cups restart").read()
    global cutstatus
    while True:
        check = os.popen("sudo lpstat -o").read()
        f = open('/var/log/cups/page_log', 'r', encoding='utf-8')
        linelist = f.readlines()
        strr = linelist[len(linelist) - 1]
        f.close()
        if check.find("get-"+str(jobid)) >= 0:
            cutstatus += 1
            print("cusstatus")
        elif (check.find("get-"+str(jobid)) <= 0) and (cutstatus >= 1):
            print("page count ", int(strr[strr.find("+0700]")+7:strr.find("+0700]")+8])*int(strr[strr.find("+0700]")+9:strr.find("+0700]")+10]))
            page = int(int(strr[strr.find("+0700]")+7:strr.find("+0700]")+8])*int(strr[strr.find("+0700]")+9:strr.find("+0700]")+10]))
            print("sum page", page)
            conn2boylogin = pymysql.connect(host='boylogin.me', port=3306, user='boy', passwd='boylogin', db='mydb')
            cur2boylogin = conn2boylogin.cursor()
            cur2boylogin.execute("UPDATE JOB SET page = %s WHERE job_id = %s", (page, jobid))
            cur2boylogin.execute("UPDATE CREDIT SET credit_balance = credit_balance - %s, credit_used = credit_used + %s, last_print = NOW() WHERE student_id = %s", (page, page, stdid))
            cutstatus = 0
            return
        time.sleep(2)
'''


def cutcredit(stdid, jobfrom, jobid):
    global conn2boylogin
    os.popen("sudo service cups restart").read()
    global status
    strgetpage = "snmpgetnext -Oqv -v 2c -c public 10.4.7.202 1.3.6.1.4.1.11.2.3.9.4.2.1.4.1.2.5"
    strgetstatus = "snmpgetnext -Oqv -v 2c -c public 10.4.7.202 1.3.6.1.4.1.11.2.3.9.1.1.3"
    currentpagecountbefore = os.popen(strgetpage).read()
    while True:
        print("waiting")
        printerstatusbefore = os.popen(strgetstatus).read()
        print(printerstatusbefore)
        if printerstatusbefore.find("Printing") >= 0:
            status = 1
            while True:
                print("waiting print complete")
                printerstatusafter = os.popen(strgetstatus).read()
                currentpagecountafter = os.popen(strgetpage).read()
                if printerstatusafter.find("Printing") < 0:
                    print(int(currentpagecountafter)-int(currentpagecountbefore))
                    page = int(currentpagecountafter)-int(currentpagecountbefore)
                    conn2boylogin = conn2boylogin.cursor()
                    conn2boylogin.execute("UPDATE JOB SET page = %s,job_out = NOW(), STUDENT_id = %s WHERE job_id = %s", (int(page), stdid, jobid))
                    conn2boylogin.execute("UPDATE CREDIT SET credit_balance = credit_balance - %s, credit_used = credit_used + %s, last_print = NOW() WHERE student_id = %s", (page, page, stdid))
                    status = 0
                    return
                time.sleep(1)
        elif status == 1:
            status = 0
            return
        time.sleep(1)


def creditreport():
    global conn2boylogin
    x, y = readcard()
    try:
        cur2boylogin = conn2boylogin.cursor()
        cur2boylogin.execute("SELECT STUDENT.firstname, STUDENT.lastname, STUDENT.stdid, CREDIT.credit_balance FROM  STUDENT LEFT JOIN  CREDIT ON STUDENT.id = CREDIT.student_id WHERE STUDENT.id LIKE %s", x)
        row = cur2boylogin.fetchone()
        return row[2], str(row[0] + " " + row[1]), row[3]
    except Exception as e:
        print(e)
        return


'''def cutcredit(stdid, jobid):
    global count
    os.popen("sudo service cups restart").read()
    while True:
        check = os.popen("sudo lpstat -o").read()
        print(check.find("get-"+str(jobid)))
        print("get-"+str(jobid))
        if check.find("get-"+str(jobid)) >= 0:
            count += 1
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        elif count > 0:
            count = count / 15
            print(count)
            conn2boylogin = pymysql.connect(host='boylogin.me', port=3306, user='boy', passwd='boylogin', db='mydb')
            cur2boylogin = conn2boylogin.cursor()
            cur2boylogin.execute(
                "UPDATE CREDIT SET credit_balance = credit_balance - %s, credit_used = credit_used + %s, last_print = NOW() WHERE student_id = %s",
                (int(count), int(count), stdid))
            cur2boylogin.execute("UPDATE JOB SET page = %s,job_out = NOW(), STUDENT_id = %s WHERE job_id = %s",
                                 (int(count), stdid, jobid))
            count = 0
            return
        print("def cutcredit(stdid, jobid)")
        time.sleep(1)'''


def readcard():
    # Return (x, y) x=datarx and y=status(100=no credit, 101=have credit, 102=card not found)
    global count
    global conn2boylogin
    while True:
        # count == 100 because (0.1*3)*50 = 15sec, by 0.1=timeout and 3 data to write(ledon, ledoff, selectcard)
        # Must read rx data before write next tx data
        check.write(bytearray(selectkey))
        datarx = ''.join(format(x, '02x') for x in check.read(128))
        try:
            if count == 10:
                check.write(bytearray(ledoff))
                check.read()
                #print("No card comming")
                count = 0
                return datarx, 102
            elif datarx != "bd030101be":
                check.write(bytearray(ledoff))
                check.read(128)
                conn2boylogin = conn2boylogin.cursor()
                conn2boylogin.execute("SELECT status FROM CREDIT WHERE student_id = %s", datarx)
                row = conn2boylogin.fetchone()
                #print(datarx)
                count = 0
                return datarx, row[0]
            elif (count % 2) == 0:
                check.write(bytearray(ledon))
                check.read(128)
            elif (count % 2) != 0:
                check.write(bytearray(ledoff))
                check.read(128)
            count += 1
        except Exception as e:
            #print("Excaption readcard@Controlfile :", e)
            count = 0
            return datarx, 102
