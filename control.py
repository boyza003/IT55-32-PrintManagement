__author__ = 'BoyChaiwat'

import serial
import pymysql
import time
import os

conn2boylogin = pymysql.connect(host='128.199.132.148', port=3306, user='boy', passwd='boylogin', db='mydb')
cur2boylogin = conn2boylogin.cursor()
#check = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.1)
check = serial.Serial("/dev/tty.SLAB_USBtoUART", 115200, timeout=0.1)
selectkey = bytes([0xBA, 0x02, 0x01, 0xB9])
ledon = bytes([0xBA, 0x03, 0x40, 0x01, 0xF8])
ledoff = bytes([0xBA, 0x03, 0x40, 0x00, 0xF9])

checklast = 0
checkloopcreditcut = 0
def cutcredit(stdid, jobfrom, jobid):
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

def readcard():
    # Return (x, y) x=datarx and y=status(100=no credit, 101=have credit, 102=card not found)
    count = 0
    while True:
        # count == 100 because (0.1*3)*50 = 15sec, by 0.1=timeout and 3 data to write(ledon, ledoff, selectcard)
        # Must read rx data before write next tx data
        check.write(bytearray(selectkey))
        datarx = ''.join(format(x, '02x') for x in check.read(128))
        try:
            if count == 10:
                check.write(bytearray(ledoff))
                check.read()
                print("No card comming")
                return datarx, 102
            if datarx != "bd030101be":
                cur2boylogin.execute("SELECT status FROM CREDIT WHERE student_id = %s", datarx)
                row = cur2boylogin.fetchone()
                check.write(bytearray(ledoff))
                check.read(128)
                print(datarx)
                return datarx, row[0]
            elif (count % 2) == 0:
                check.write(bytearray(ledon))
                check.read(128)
            elif (count % 2) != 0:
                check.write(bytearray(ledoff))
                check.read(128)
            count += 1
        except Exception as e:
            print("Excaption readcard@Controlfile :", e)
            return datarx, 102