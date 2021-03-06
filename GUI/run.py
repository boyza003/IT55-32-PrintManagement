__author__ = 'PC-B1301'
__author__ = 'BoyChaiwat'

import tkinter as tk
import os
import time

import serial
import pymysql

LARGE_FONT = ("Verdana", 24)
TITLE_FONT = ("Helvetica", 16, "bold")
LIST_FONT = ("Helvetica", 24)
TIME_FONT = ("Helvetica", 16, "italic")

# Database connection
conn2boylogin = pymysql.connect(host='boylogin.me', port=3306, user='boy', passwd='boylogin', db='mydb')
cur2boylogin = conn2boylogin.cursor()
conn2local = pymysql.connect(host='boylogin.me', port=3306, user='boy', passwd='boylogin', db='mydb')
cur2local = conn2local.cursor()

#check = serial.Serial("/dev/tty.SLAB_USBtoUART", 115200, timeout=1)
checkled = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
selectkey = bytes([0xBA, 0x02, 0x01, 0xB9])
ledon = bytes([0xBA, 0x03, 0x40, 0x01, 0xF8])
ledoff = bytes([0xBA, 0x03, 0x40, 0x00, 0xF9])
ledtime = 0
lastlog = ""
jobid = 24
stdid = 0
jobinpool1 = ""


class SeaofBTCapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, Printpool1):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Header
        detailjobfrom = tk.Label(self, text="Print from", font=TIME_FONT)
        detailjobfrom.place(x=50, y=10)
        detailjobfrom.pi = detailjobfrom.place_info()
        detailjobdate = tk.Label(self, text="Print time", font=TIME_FONT)
        detailjobdate.place(x=200, y=10)
        detailjobdate.pi = detailjobdate.place_info()
        delailjobink = tk.Label(self, text="Ink", font=TIME_FONT)
        delailjobink.place(x=360, y=10)
        delailjobink.pi = delailjobink.place_info()

        # Job1
        def getjobfrom(label):
            def looppoolmanagement():
                global getText
                global jobinpool1
                # Pool1
                cur2local.execute("SELECT * FROM POOL WHERE id = 1")
                row = cur2local.fetchone()
                labeljob1from = tk.Label(self, text=row[2], font=LIST_FONT)
                labeljob1from.place(x=20, y=45)
                lablejob1time = tk.Label(self, text=row[3], font=TIME_FONT)
                lablejob1time.place(x=200, y=45)

                # Pool2
                cur2local.execute("SELECT * FROM POOL WHERE id = 2")
                row = cur2local.fetchone()
                labeljob2from = tk.Label(self, text=row[2], font=LIST_FONT)
                labeljob2from.place(x=20, y=95)
                lablejob2time = tk.Label(self, text=row[3], font=TIME_FONT)
                lablejob2time.place(x=200, y=95)

                # Pool3
                cur2local.execute("SELECT * FROM POOL WHERE id = 3")
                row = cur2local.fetchone()
                labeljob3from = tk.Label(self, text=row[2], font=LIST_FONT)
                labeljob3from.place(x=20, y=145)
                lablejob3time = tk.Label(self, text=row[3], font=TIME_FONT)
                lablejob3time.place(x=200, y=145)

                # Pool4
                cur2local.execute("SELECT * FROM POOL WHERE id = 4")
                row = cur2local.fetchone()
                labeljob1from = tk.Label(self, text=row[2], font=LIST_FONT)
                labeljob1from.place(x=20, y=195)
                lablejob1time = tk.Label(self, text=row[3], font=TIME_FONT)
                lablejob1time.place(x=200, y=195)

                getText = row[0]
                label.config(text=str(getText))
                label.after(5000, looppoolmanagement)

                # Pool management
                # print("Pool management")
                Now = time.time()
                check = os.popen("sudo lpstat -o").read()
                print(check.find("print"))
                print(check[check.find("print") + 6:check.find("print") + 15])
                if check.find("print") >= 0:
                    getdate = os.popen("date").read()
                    # print("I have a new job")
                    cur2local.execute("SELECT id, JOB_ID FROM POOL WHERE time = (SELECT MIN(time) FROM POOL)")
                    row = cur2local.fetchone()
                    # print(row[0])
                    if row[0] == 1:
                        jobinpool1 = check[check.find("print") + 6:check.find("print") + 15]
                        strmove = "sudo lpmove " + check[check.find("print") + 6:check.find("print") + 15] + " pool1"
                        strhold = "sudo lp -i " + check[check.find("print") + 6:check.find("print") + 15] + "-H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=%s WHERE id = 1",
                                          (int(check[check.find("print") + 6:check.find("print") + 15]),
                                           check[check.find("print") + 24:check.find("print") + 40], getdate[11:19]))
                    elif row[0] == 2:
                        strmove = "sudo lpmove " + check[check.find("print") + 6:check.find("print") + 15] + " pool2"
                        strhold = "sudo lp -i " + check[check.find("print") + 6:check.find("print") + 15] + "-H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        # strmove = "sudo lpmove " + check[check.find("print") + 6:check.find("print") + 15] + " pool2"
                        # os.popen(strmove).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=%s WHERE id = 2",
                                          (int(check[check.find("print") + 6:check.find("print") + 15]),
                                           check[check.find("print") + 24:check.find("print") + 40], getdate[11:19]))
                    elif row[0] == 3:
                        print("pool3")
                        strmove = "sudo lpmove " + check[check.find("print") + 6:check.find("print") + 15] + " pool3"
                        strhold = "sudo lp -i " + check[check.find("print") + 6:check.find("print") + 15] + "-H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        # strmove = "lpmove " + check[check.find("print") + 6:check.find("print") + 15] + " pool3"
                        # os.popen(strmove).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=%s WHERE id = 3",

                                          (int(check[check.find("print") + 6:check.find("print") + 15]),
                                           check[check.find("print") + 24:check.find("print") + 40], getdate[11:19]))
                    elif row[0] == 4:
                        strmove = "sudo lpmove " + check[check.find("print") + 6:check.find("print") + 15] + " pool4"
                        strhold = "sudo lp -i " + check[check.find("print") + 6:check.find("print") + 15] + "-H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        # strmove = "lpmove " + check[check.find("print") + 6:check.find("print") + 15] + " pool4"
                        # os.popen(strmove).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=%s WHERE id = 4",
                                          (int(check[check.find("print") + 6:check.find("print") + 15]),
                                           check[check.find("print") + 24:check.find("print") + 40], getdate[11:19]))
                else:
                    print("I have no job")

            looppoolmanagement()

        # Button zone
        printcolor = tk.Button(self, text="Print", command=lambda: controller.show_frame(Printpool1))
        printcolor.place(x=345, y=50)
        # write_slogan(printcolor)
        registerbutton = tk.Button(self, text="Register", command=lambda: controller.show_frame(PageOne))
        registerbutton.place(x=100, y=240)
        creditreportbutton = tk.Button(self, text="Credit report", command=lambda: controller.show_frame(PageTwo))
        creditreportbutton.place(x=200, y=240)

        # Show label list
        job1 = tk.Label(self, font=LIST_FONT)
        getjobfrom(job1)

    def printpool1(button):
        # check.write(bytearray(ledon))
        # check.close()
        # check.open()

        def cutcredit(stdid, jobid):
            #return print("Good job", stdid, jobid)
            '''file = open('page_log', 'r')  # specify file to open
            data = file.readlines()  # read lines in file and put into
            if lastlog != data[len(data) - 1]:
                lastlog = data[len(data) - 1]
                print("Student ID : ", stdid, "Crdit -1 At job : ", jobid)
                return True
            else:
                return False
                # file.close()  # good practice to close files after use'''

        def loopcheckcredit():
            global ledtime
            check.write(bytearray(selectkey))
            datarx = ''.join(format(x, '02x') for x in check.read(128))
            print("led time", ledtime)
            try:
                if ledtime == 150:
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
                elif (ledtime % 2) == 0:
                    check.write(bytearray(ledon))
                    check.read(128)
                elif (ledtime % 2) != 0:
                    check.write(bytearray(ledoff))
                    check.read(128)
                ledtime += 1
            except Exception as e:
                print("Excaption readcard() :", e)
                return datarx, 102
            app.after(100, loopcheckcredit)

        loopcheckcredit()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        toplabel = tk.Label(self, text="Register from", font=LARGE_FONT)
        toplabel.pack(pady=10, padx=10)
        footlabel = tk.Label(self, text="Please Tap your ID Card", font=LARGE_FONT)
        footlabel.place(x=80, y=200)

        button1 = tk.Button(self, text="Back to list", command=lambda: controller.show_frame(StartPage))
        button1.place(x=350, y=250)
        # button2 = tk.Button(self, text="Print", command=self.checkcredit)
        # button2.pack()


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        toplable = tk.Label(self, text="Credit report", font=LARGE_FONT)
        toplable.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to list", command=lambda: controller.show_frame(StartPage))
        button1.place(x=350, y=250)
        # button2 = tk.Button(self, text="Page One", command=lambda: controller.show_frame(PageOne))
        # button2.pack()


class Printpool1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        toplable = tk.Label(self, text="Print job at pool 1", font=LARGE_FONT)
        toplable.pack(pady=10, padx=10)

        def loopcheckcredit():
            global ledtime
            check.write(bytearray(selectkey))
            datarx = ''.join(format(x, '02x') for x in check.read(128))
            print("led time", ledtime)
            try:
                if ledtime == 150:
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
                elif (ledtime % 2) == 0:
                    check.write(bytearray(ledon))
                    check.read(128)
                elif (ledtime % 2) != 0:
                    check.write(bytearray(ledoff))
                    check.read(128)
                ledtime += 1
            except Exception as e:
                print("Excaption readcard() :", e)
                return datarx, 102
            app.after(100, loopcheckcredit)

        loopcheckcredit()

        printcolor = tk.Button(self, text="Print", command=self.loopcheckcredit)
        printcolor.place(x=345, y=50)
        button1 = tk.Button(self, text="Back to list", command=lambda: controller.show_frame(StartPage))
        button1.place(x=350, y=250)

app = SeaofBTCapp()
app.geometry('480x300')
app.mainloop()

'''
# TKk while loop
 def loopcheckcredit():

            # อ่านให้เข้าใจ
            app.after(1000, loopcheckcredit)
        loopcheckcredit()
'''
