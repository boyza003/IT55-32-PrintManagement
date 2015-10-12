__author__ = 'PC-B1301'
import os.path
import time

while True:
    with open('/var/log/cups/page_log') as myfile:
        print(list(myfile)[-1])
    time.sleep(2)


