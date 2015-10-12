__author__ = 'BoyChaiwat'

# Print status : snmpwalk -v1 -c public 10.4.7.201 1.3.6.1.4.1.11.2.3.9.1.1.3.0
# Current page count : snmpwalk -v1 -c public 10.4.7.201 1.3.6.1.4.1.11.2.3.9.4.2.1.4.1.2.5.0

import os
import time

printerstatus = os.popen("snmpgetnext -Oqv -v 2c -c public 10.4.7.202 1.3.6.1.4.1.11.2.3.9.1.1.3").read()
currentpagecount = os.popen("snmpgetnext -Oqv -v 2c -c public 10.4.7.202 1.3.6.1.4.1.11.2.3.9.4.2.1.4.1.2.5").read()
print(printerstatus)
print(currentpagecount)
status = 0


def snmpprinter():
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
                    return
                time.sleep(1)
        elif status == 1:
            status = 0
            return
        time.sleep(1)


snmpprinter()
