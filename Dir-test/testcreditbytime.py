__author__ = 'BoyChaiwat'

import serial

check = serial.Serial("/dev/tty.SLAB_USBtoUART", 115200, timeout=0.1)
selectkey = bytes([0xBA, 0x02, 0x01, 0xB9])

i = 1
def get():
    global i
    while True:
        check.write(bytearray(selectkey))
        datarx = ''.join(format(x, '02x') for x in check.read(128))
        if datarx != "bd030101be":
            i += 1
        elif i > 1:
            print(i)
            i = 1

get()
