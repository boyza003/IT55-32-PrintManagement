__author__ = 'BoyChaiwat'

from control import *
import tkinter as tk
import os
import time
import pymysql

LARGE_FONT = ("Verdana", 18)
TITLE_FONT = ("Helvetica", 16, "bold")
LIST_FONT = ("Helvetica", 22)
TIME_FONT = ("Helvetica", 14, "italic")

# Database connection
conn2local = pymysql.connect(host='boylogin.me', user='boy', passwd='boylogin', db='mydb')

# Time frist job
times = ["00:00:01", "00:00:02", "00:00:03", "00:00:04"]

# Pool array = ["jobfrom", "jobid", "jobfromupdate", "time", "timeupdate"]
pool1 = ["", "", "", "", " "]
pool2 = ["", "", "", "", " "]
pool3 = ["", "", "", "", " "]
pool4 = ["", "", "", "", " "]

class SeaofBTCapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Register, CreditReport):
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
        detailjobfrom.place(x=50, y=2)
        detailjobfrom.pi = detailjobfrom.place_info()
        detailjobdate = tk.Label(self, text="Print time", font=TIME_FONT)
        detailjobdate.place(x=265, y=2)
        detailjobdate.pi = detailjobdate.place_info()
        delailjobink = tk.Label(self, text="", font=TIME_FONT)
        delailjobink.place(x=390, y=2)
        delailjobink.pi = delailjobink.place_info()

        # List lable
        def getjobfrom(label):
            def looppoolmanagement():
                global getText
                global times
                global pool1
                global pool2
                global pool3
                global pool4

                # List 1 ["jobfrom", "jobid", "jobfromupdate", "time", "timeupdate"]
                labeljob1from = tk.Label(self, font=LIST_FONT)
                labeljob1from.place(x=20, y=25)
                lablejob1time = tk.Label(self, font=LIST_FONT)
                lablejob1time.place(x=250, y=25)
                if pool1[3] != pool1[4]:
                    labeljob1from.config(text=pool1[2])
                    lablejob1time.config(text=pool1[4])
                    pool1[0] = pool1[2]
                    pool1[3] = pool1[4]

                # List 2
                labeljob2from = tk.Label(self, font=LIST_FONT)
                labeljob2from.place(x=20, y=70)
                lablejob2time = tk.Label(self, font=LIST_FONT)
                lablejob2time.place(x=250, y=70)
                if pool2[3] != pool2[4]:
                    labeljob2from.config(text=pool2[2])
                    lablejob2time.config(text=pool2[4])
                    pool2[0] = pool2[2]
                    pool2[3] = pool2[4]

                # List 3
                labeljob3from = tk.Label(self, font=LIST_FONT)
                labeljob3from.place(x=20, y=115)
                lablejob3time = tk.Label(self, font=LIST_FONT)
                lablejob3time.place(x=250, y=115)
                if pool3[3] != pool3[4]:
                    labeljob3from.config(text=pool3[2])
                    lablejob3time.config(text=pool3[4])
                    pool3[0] = pool3[2]
                    pool3[3] = pool3[4]

                # List 4
                labeljob4from = tk.Label(self, font=LIST_FONT)
                labeljob4from.place(x=20, y=160)
                lablejob4time = tk.Label(self, font=LIST_FONT)
                lablejob4time.place(x=250, y=160)
                if pool4[3] != pool4[4]:
                    labeljob4from.config(text=pool4[2])
                    lablejob4time.config(text=pool4[4])
                    pool4[0] = pool4[2]
                    pool4[3] = pool4[4]

                getText = ""

                # Pool management
                print("Pool management")
                check = os.popen("sudo  lpstat -o").read()
                print(check)
                print(check.find("print"))
                print(check[check.find("print") + 6:check.find("print") + 15])
                if check.find("print") >= 0:
                    cur2local = conn2local.cursor()
                    #getdate = os.popen("date").read()
                    print("I have a new job")
                    getjobid = str(check[check.find("print") + 6:check.find("print") + 15]).strip()
                    gethostname = str(check[check.find("print") + 24:check.find("print") + 39]).strip()
                    cur2local.execute("INSERT INTO  JOB (job_id, page, job_in ) VALUES (%s, 0, NOW())", getjobid)
                    print(getjobid)
                    print(gethostname)
                    # print(row[0])
                    if times.index(min(times)) == 0:
                        times[0] = time.strftime("%H:%M:%S")
                        strmove = "sudo lpmove " + getjobid + " pool1"
                        strhold = "sudo lp -i " + getjobid + " -H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=CURTIME() WHERE id = 1",
                                          (int(getjobid), gethostname))
                        pool1[1] = getjobid
                        pool1[2] = gethostname
                        pool1[4] = str(time.strftime("%H:%M:%S"))

                    elif times.index(min(times)) == 1:
                        times[1] = time.strftime("%H:%M:%S")
                        strmove = "sudo lpmove " + getjobid + " pool2"
                        strhold = "sudo lp -i " + getjobid + " -H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=CURTIME() WHERE id = 2",
                                          (int(getjobid), gethostname))
                        pool2[1] = getjobid
                        pool2[2] = gethostname
                        pool2[4] = str(time.strftime("%H:%M:%S"))


                    elif times.index(min(times)) == 2:
                        times[2] = time.strftime("%H:%M:%S")
                        strmove = "sudo lpmove " + getjobid + " pool3"
                        strhold = "sudo lp -i " + getjobid + " -H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=CURTIME() WHERE id = 3",
                                          (int(getjobid), gethostname))
                        pool3[1] = getjobid
                        pool3[2] = gethostname
                        pool3[4] = str(time.strftime("%H:%M:%S"))

                    elif times.index(min(times)) == 3:
                        times[3] = time.strftime("%H:%M:%S")
                        strmove = "sudo lpmove " + getjobid + " pool4"
                        strhold = "sudo lp -i " + getjobid + " -H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=CURTIME() WHERE id = 4",
                                          (int(getjobid), gethostname))
                        pool4[1] = getjobid
                        pool4[2] = gethostname
                        pool4[4] = str(time.strftime("%H:%M:%S"))

                else:
                    print("I have no job")
                label.config(text=str(getText))
                label.after(1000, looppoolmanagement)
            looppoolmanagement()

        def print1():
            global pool1
            stdid, ststusid = readcard()
            print(ststusid)
            if ststusid == 101:
                strmove = "sudo lpmove " + pool1[1] + " get"
                strhold = "sudo lp -i " + pool1[1] + " -H resume"
                os.popen(strmove).read()
                os.popen(strhold).read()
                print(stdid)
                print(pool1[0])
                print(pool1[1])
                cutcredit(stdid, pool1[0], pool1[1])
                times[0] = "00:00:01"
                pool1[2] = "                            "
                pool1[4] = "                            "

        def print2():
            global pool2
            stdid, ststusid = readcard()
            print(ststusid)
            if ststusid == 101:
                strmove = "sudo lpmove " + pool2[1] + " get"
                strhold = "sudo lp -i " + pool2[1] + " -H resume"
                os.popen(strmove).read()
                os.popen(strhold).read()
                cutcredit(stdid, pool2[1])
                times[1] = "00:00:02"
                pool2[2] = "                            "
                pool2[4] = "                            "

        def print3():
            global pool3
            stdid, ststusid = readcard()
            print(ststusid)
            if ststusid == 101:
                strmove = "sudo lpmove " + pool3[1] + " get"
                strhold = "sudo lp -i " + pool3[1] + " -H resume"
                os.popen(strmove).read()
                os.popen(strhold).read()
                cutcredit(stdid, pool3[1])
                times[2] = "00:00:03"
                pool3[2] = "                            "
                pool3[4] = "                            "

        def print4():
            global pool4
            stdid, ststusid = readcard()
            print(ststusid)
            if ststusid == 101:
                strmove = "sudo lpmove " + pool4[1] + " get"
                strhold = "sudo lp -i " + pool4[1] + " -H resume"
                os.popen(strmove).read()
                os.popen(strhold).read()
                cutcredit(stdid, pool4[1])
                times[3] = "00:00:04"
                pool4[2] = "                            "
                pool4[4] = "                            "

        def restartcups():
            os.popen("sudo service cups restart").read()

        # Print button zone
        printjob1 = tk.Button(self, text="Print", command=print1)
        printjob1.place(x=395, y=30)
        printjob2 = tk.Button(self, text="Print", command=print2)
        printjob2.place(x=395, y=75)
        printjob3 = tk.Button(self, text="Print", command=print3)
        printjob3.place(x=395, y=120)
        printjob4 = tk.Button(self, text="Print", command=print4)
        printjob4.place(x=395, y=165)

        registerbutton = tk.Button(self, text="Register", command=lambda: controller.show_frame(Register))
        registerbutton.place(x=55, y=220)
        creditreportbutton = tk.Button(self, text="Credit report", command=lambda: controller.show_frame(CreditReport))
        creditreportbutton.place(x=165, y=220)
        restartcupsbutton = tk.Button(self, text="Reload printer", command=restartcups)
        restartcupsbutton.place(x=300, y=220)

        # Show label list
        showjob = tk.Label(self, font=LIST_FONT)
        getjobfrom(showjob)


class Register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        headlabel = tk.Label(self, text="Register", font=LARGE_FONT)
        headlabel.pack(pady=10, padx=10)
        stdidlable = tk.Label(self, text="Student ID : ", font=LARGE_FONT)
        stdidlable.place(x=20, y=50)
        creditlable = tk.Label(self, text="Balanace : ", font=LARGE_FONT)
        creditlable.place(x=20, y=100)

        stdidlable2 = tk.Label(self, font=LARGE_FONT)
        stdidlable2.place(x=170, y=50)
        creditlable2 = tk.Label(self, font=LARGE_FONT)
        creditlable2.place(x=145, y=100)

        def cleartext():
            stdidlable2.config(text="")
            creditlable2.config(text="")

        def clickregister():
            global con2boylogin
            try:
                conn2boylogin = pymysql.connect(host='boylogin.me', port=3306, user='boy', passwd='boylogin', db='mydb')
                cur2boylogin = conn2boylogin.cursor()
                x, y = readcard()
                cur2boylogin.execute("SELECT * FROM STUDENT WHERE id=%s", x)
                row = cur2boylogin.fetchone()
                if row[0] == x:
                    cur2boylogin.execute(
                        "INSERT INTO CREDIT(credit_balance , status, credit_used, student_id) VALUES (100, 101, 0,%s)",
                        x)
                    stdidlable2.config(text=x)
                    creditlable2.config(text="100")
            except Exception as e:
                print(e)

        readcardbutton = tk.Button(self, text="Read card", command=clickregister)
        readcardbutton.place(x=150, y=220)
        clearbutton = tk.Button(self, text="Clear", command=cleartext)
        clearbutton.place(x=280, y=220)
        backtohomebutton = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        backtohomebutton.place(x=370, y=220)


class CreditReport(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        headlabel = tk.Label(self, text="Credit report", font=LARGE_FONT)
        headlabel.pack(pady=10, padx=10)
        stdidlable = tk.Label(self, text="Student ID : ", font=LARGE_FONT)
        stdidlable.place(x=20, y=50)
        stdname = tk.Label(self, text="Name : ", font=LARGE_FONT)
        stdname.place(x=20, y=100)
        creditlable = tk.Label(self, text="Balanace : ", font=LARGE_FONT)
        creditlable.place(x=20, y=150)

        stdidlable2 = tk.Label(self, font=LARGE_FONT)
        stdidlable2.place(x=170, y=50)
        stdname2 = tk.Label(self, font=LARGE_FONT)
        stdname2.place(x=110, y=100)
        creditlable2 = tk.Label(self, font=LARGE_FONT)
        creditlable2.place(x=145, y=150)

        def cleartext():
            stdidlable2.config(text="")
            stdname2.config(text="")
            creditlable2.config(text="")

        def checkcredit():
            try:
                x, y, z = creditreport()
                stdidlable2.config(text=x)
                stdname2.config(text=y)
                creditlable2.config(text=z)

            except Exception as e:
                print(e)
        readcardbutton = tk.Button(self, text="Read card", command=checkcredit)
        readcardbutton.place(x=150, y=220)
        clearbutton = tk.Button(self, text="Clear", command=cleartext)
        clearbutton.place(x=280, y=220)
        backtohomebutton = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        backtohomebutton.place(x=370, y=220)


app = SeaofBTCapp()
app.title("IT55-32")
app.geometry('480x300')
app.mainloop()
