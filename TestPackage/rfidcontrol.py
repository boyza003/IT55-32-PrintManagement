__author__ = 'BoyChaiwat'

import serial
import pymysql

conn2boylogin = pymysql.connect(host='boylogin.me', port=3306, user='boy', passwd='boylogin', db='mydb')
cur2boylogin = conn2boylogin.cursor()
check = serial.Serial("/dev/tty.SLAB_USBtoUART", 115200, timeout=0.1)
# checkled = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
selectkey = bytes([0xBA, 0x02, 0x01, 0xB9])
ledon = bytes([0xBA, 0x03, 0x40, 0x01, 0xF8])
ledoff = bytes([0xBA, 0x03, 0x40, 0x00, 0xF9])


def readcard():
    # Return (x, y) x=datarx and y=status(100=no credit, 101=have credit, 102=card not found)
    count = 0
    while True:

        # count == 100 because (0.1*3)*50 = 15sec, by 0.1=timeout and 3 data to write(ledon, ledoff, selectcard)
        # Must read rx data before write next tx data
        check.write(bytearray(selectkey))
        datarx = ''.join(format(x, '02x') for x in check.read(128))
        try:
            if count == 150:
                check.write(bytearray(ledoff))
                check.read()
                print("No card comming")
                return datarx, 102
            if datarx != "bd030101be":
                cur2boylogin.execute("SELECT status FROM CREDIT WHERE student_id = %s", datarx)
                row = cur2boylogin.fetchone()
                check.write(bytearray(ledoff))
                check.read(128)
                return datarx, row[0]
            elif (count % 2) == 0:
                check.write(bytearray(ledon))
                check.read(128)
            elif (count % 2) != 0:
                check.write(bytearray(ledoff))
                check.read(128)
            count += 1
        except Exception as e:
            print("Excaption readcard() :", e)
            return datarx, 102


stdid, stdstatus = readcard()
print(stdid)
print(stdstatus)
