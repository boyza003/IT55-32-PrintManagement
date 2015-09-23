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

# List job
job1from = ""
job1time = ""
job1fromupdate = ""
job1timeupdate = ""
job2from = ""
job2time = ""
job2fromupdate = ""
job2timeupdate = ""
job3from = ""
job3time = ""
job3fromupdate = ""
job3timeupdate = ""
job4from = ""
job4time = ""
job4fromupdate = ""
job4timeupdate = ""

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
        detailjobdate.place(x=225, y=2)
        detailjobdate.pi = detailjobdate.place_info()
        delailjobink = tk.Label(self, text="", font=TIME_FONT)
        delailjobink.place(x=390, y=2)
        delailjobink.pi = delailjobink.place_info()

        # List lable
        def getjobfrom(label):
            def looppoolmanagement():
                global getText
                global job1from
                global job1time
                global job1fromupdate
                global job1timeupdate
                global job2from
                global job2time
                global job2fromupdate
                global job2timeupdate
                global job3from
                global job3time
                global job3fromupdate
                global job3timeupdate
                global job4from
                global job4time
                global job4fromupdate
                global job4timeupdate
                #global cur2local
                #cur2local = conn2local.cursor()

                # Pool1
                #cur2local.execute("SELECT * FROM POOL WHERE id = 1")
                #row = cur2local.fetchone

                # List 1
                labeljob1from = tk.Label(self, font=LIST_FONT)
                labeljob1from.place(x=20, y=25)
                lablejob1time = tk.Label(self, font=LIST_FONT)
                lablejob1time.place(x=200, y=25)
                if job1from != job1fromupdate:
                    labeljob1from.config(text=job1fromupdate)
                    lablejob1time.config(text=job1timeupdate)
                    job1from = job1fromupdate
                    job1time = job1timeupdate

                # List 2
                labeljob2from = tk.Label(self, font=LIST_FONT)
                labeljob2from.place(x=20, y=70)
                lablejob2time = tk.Label(self, font=LIST_FONT)
                lablejob2time.place(x=200, y=70)
                if job2from != job2fromupdate:
                    labeljob2from.config(text=job2fromupdate)
                    lablejob2time.config(text=job2timeupdate)
                    job2from = job2fromupdate
                    job2time = job2timeupdate

                # List 3
                labeljob3from = tk.Label(self, font=LIST_FONT)
                labeljob3from.place(x=20, y=115)
                lablejob3time = tk.Label(self, font=LIST_FONT)
                lablejob3time.place(x=200, y=115)
                if job3from != job3fromupdate:
                    labeljob3from.config(text=job3fromupdate)
                    lablejob3time.config(text=job3timeupdate)
                    job3from = job3fromupdate
                    job3time = job3timeupdate

                # List 4
                labeljob4from = tk.Label(self, font=LIST_FONT)
                labeljob4from.place(x=20, y=160)
                lablejob4time = tk.Label(self, font=LIST_FONT)
                lablejob4time.place(x=200, y=160)
                if job4from != job4fromupdate:
                    labeljob4from.config(text=job4fromupdate)
                    lablejob4time.config(text=job4timeupdate)
                    job4from = job4fromupdate
                    job4time = job4timeupdate

                # Pool2
                #cur2local.execute("SELECT * FROM POOL WHERE id = 2")
                #row = cur2local.fetchone()
                #labeljob2from = tk.Label(self, text=row[2], font=LIST_FONT)
                #labeljob2from.place(x=20, y=70)
                #lablejob2time = tk.Label(self, text=row[3], font=TIME_FONT)
                #lablejob2time.place(x=200, y=80)

                # Pool3
                #cur2local.execute("SELECT * FROM POOL WHERE id = 3")
                #row = cur2local.fetchone()
                #labeljob3from = tk.Label(self, text=row[2], font=LIST_FONT)
                #labeljob3from.place(x=20, y=115)
                #lablejob3time = tk.Label(self, text=row[3], font=TIME_FONT)
                #lablejob3time.place(x=200, y=127)

                # Pool4
                #cur2local.execute("SELECT * FROM POOL WHERE id = 4")
                #row = cur2local.fetchone()
                #labeljob1from = tk.Label(self, text=row[2], font=LIST_FONT)
                #labeljob1from.place(x=20, y=160)
                #lablejob1time = tk.Label(self, text=row[3], font=TIME_FONT)
                #lablejob1time.place(x=200, y=173)

                getText = ""
                #label.config(text=str(getText))
                #label.after(5000, looppoolmanagement)

                # Pool management
                print("Pool management")
                check = os.popen("sudo  lpstat -o").read()
                print(check)
                print(check.find("print"))
                print(check[check.find("print") + 6:check.find("print") + 15])
                if check.find("print") >= 0:
                    cur2local = conn2local.cursor()
                    getdate = os.popen("date").read()
                    print("I have a new job")
                    cur2local.execute("SELECT id, JOB_ID FROM POOL WHERE time = (SELECT MIN(time) FROM POOL)")
                    row = cur2local.fetchone()
                    getjobid = str(check[check.find("print") + 6:check.find("print") + 15]).strip()
                    gethostname = str(check[check.find("print") + 24:check.find("print") + 39]).strip()
                    cur2local.execute("INSERT INTO  JOB (job_id, page, job_in ) VALUES (%s, 0, NOW())", getjobid)
                    print(getjobid)
                    print(gethostname)
                    # print(row[0])
                    if row[0] == 1:
                        strmove = "sudo lpmove " + getjobid + " pool1"
                        strhold = "sudo lp -i " + getjobid + " -H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=CURTIME() WHERE id = 1",
                                          (int(getjobid), gethostname))
                        #labeljob1from = tk.Label(self, text=gethostname, font=LIST_FONT)
                        #labeljob1from.place(x=20, y=25)
                        #lablejob1time = tk.Label(self, text=str(time.strftime("%H:%M:%S")), font=LIST_FONT)
                        #lablejob1time.place(x=200, y=25)
                        job1fromupdate = gethostname
                        job1timeupdate = str(time.strftime("%H:%M:%S"))

                    elif row[0] == 2:
                        strmove = "sudo lpmove " + getjobid + " pool2"
                        strhold = "sudo lp -i " + getjobid + " -H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=CURTIME() WHERE id = 2",
                                          (int(getjobid), gethostname))
                        #labeljob2from = tk.Label(self, text=gethostname, font=LIST_FONT)
                        #labeljob2from.place(x=20, y=70)
                        #lablejob2time = tk.Label(self, text=str(time.strftime("%H:%M:%S")), font=LIST_FONT)
                        #lablejob2time.place(x=200, y=70)
                        job2fromupdate = gethostname
                        job2timeupdate = str(time.strftime("%H:%M:%S"))

                    elif row[0] == 3:
                        strmove = "sudo lpmove " + getjobid + " pool3"
                        strhold = "sudo lp -i " + getjobid + " -H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=CURTIME() WHERE id = 3",
                                          (int(getjobid), gethostname))
                        #labeljob3from = tk.Label(self, text=gethostname, font=LIST_FONT)
                        #labeljob3from.place(x=20, y=115)
                        #lablejob3time = tk.Label(self, text=str(time.strftime("%H:%M:%S")), font=LIST_FONT)
                        #lablejob3time.place(x=200, y=115)
                        job3fromupdate = gethostname
                        job3timeupdate = str(time.strftime("%H:%M:%S"))

                    elif row[0] == 4:
                        jobinpool1 = getjobid
                        strmove = "sudo lpmove " + getjobid + " pool4"
                        strhold = "sudo lp -i " + getjobid + " -H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=CURTIME() WHERE id = 4",
                                          (int(getjobid), gethostname))
                        #labeljob1from = tk.Label(self, text=gethostname, font=LIST_FONT)
                        #labeljob1from.place(x=20, y=160)
                        #lablejob1time = tk.Label(self, text=str(time.strftime("%H:%M:%S")), font=LIST_FONT)
                        #lablejob1time.place(x=200, y=160)
                        job4fromupdate = gethostname
                        job4timeupdate = str(time.strftime("%H:%M:%S"))

                else:
                    print("I have no job")
                label.config(text=str(getText))
                label.after(1000, looppoolmanagement)
            looppoolmanagement()

        def print1():
            global job1fromupdate
            global job1timeupdate
            global job2fromupdate
            global job2timeupdate
            global job3fromupdate
            global job3timeupdate
            global job4fromupdate
            global job4timeupdate
            stdid, ststusid = readcard()
            print(ststusid)
            if ststusid == 101:
                print("get")
                cur2local = pymysql.connect(host='boylogin.me', user='boy', passwd='boylogin', db='mydb')
                cur2local = cur2local.cursor()
                cur2local.execute("SELECT job_id, job_from FROM POOL WHERE id = 1")
                row = cur2local.fetchone()
                strmove = "sudo lpmove " + str(row[0]) + " get"
                strhold = "sudo lp -i " + str(row[0]) + " -H resume"
                os.popen(strmove).read()
                os.popen(strhold).read()
                cutcredit(stdid, row[0])
                job1fromupdate = "                            "
                job1timeupdate = "                            "

        def print2():
            stdid, ststusid = readcard()
            print(ststusid)
            if ststusid == 101:
                print("get")
                cur2local = pymysql.connect(host='boylogin.me', user='boy', passwd='boylogin', db='mydb')
                cur2local = cur2local.cursor()
                row = cur2local.fetchone()
                strmove = "sudo lpmove " + str(row[0]) + " get"
                strhold = "sudo lp -i " + str(row[0]) + " -H resume"
                os.popen(strmove).read()
                os.popen(strhold).read()
                cutcredit(stdid, row[0])
                job2fromupdate = "                            "
                job2timeupdate = "                            "

        def print3():
            stdid, ststusid = readcard()
            print(ststusid)
            if ststusid == 101:
                print("get")
                cur2local = pymysql.connect(host='boylogin.me', user='boy', passwd='boylogin', db='mydb')
                cur2local = cur2local.cursor()
                row = cur2local.fetchone()
                strmove = "sudo lpmove " + str(row[0]) + " get"
                strhold = "sudo lp -i " + str(row[0]) + " -H resume"
                os.popen(strmove).read()
                os.popen(strhold).read()
                cutcredit(stdid, row[0])
                job3fromupdate = "                            "
                job3timeupdate = "                            "

        def print4():
            stdid, ststusid = readcard()
            print(ststusid)
            if ststusid == 101:
                print("get")
                cur2local = pymysql.connect(host='boylogin.me', user='boy', passwd='boylogin', db='mydb')
                cur2local = cur2local.cursor()
                cur2local.execute("SELECT job_id, job_from FROM POOL WHERE id = 4")
                row = cur2local.fetchone()
                strmove = "sudo lpmove " + str(row[0]) + " get"
                strhold = "sudo lp -i " + str(row[0]) + " -H resume"
                os.popen(strmove).read()
                os.popen(strhold).read()
                cutcredit(stdid, row[0])
                job4fromupdate = "                            "
                job4timeupdate = "                            "

        def restartcups():
            os.popen("sudo service cups restart").read()

        # Print button zone
        printjob1 = tk.Button(self, text="Print", command=print1)
        printjob1.place(x=395, y=33)
        printjob2 = tk.Button(self, text="Print", command=print2)
        printjob2.place(x=395, y=80)
        printjob3 = tk.Button(self, text="Print", command=print3)
        printjob3.place(x=395, y=127)
        printjob4 = tk.Button(self, text="Print", command=print4)
        printjob4.place(x=395, y=174)

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
        readcardbutton.place(x=250, y=180)
        clearbutton = tk.Button(self, text="Clear", command=cleartext)
        clearbutton.place(x=370, y=180)
        backtohomebutton = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        backtohomebutton.place(x=370, y=230)


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
                '''x, y = readcard()
                cur2boylogin.execute("SELECT STUDENT.firstname, STUDENT.lastname, STUDENT.stdid, CREDIT.credit_balance FROM  STUDENT LEFT JOIN  CREDIT ON STUDENT.id = CREDIT.student_id WHERE STUDENT.id LIKE %s", x)
                row = cur2boylogin.fetchone()
                stdidlable2.config(text=row[2])
                stdname2.config(text=)
                creditlable2.config(text=row[3])'''
                x, y, z = creditreport()
                stdidlable2.config(text=x)
                stdname2.config(text=y)
                creditlable2.config(text=z)

            except Exception as e:
                print(e)
        readcardbutton = tk.Button(self, text="Read card", command=checkcredit)
        readcardbutton.place(x=250, y=180)
        clearbutton = tk.Button(self, text="Clear", command=cleartext)
        clearbutton.place(x=370, y=180)
        backtohomebutton = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        backtohomebutton.place(x=370, y=230)


app = SeaofBTCapp()
app.title("IT55-32")
app.geometry('480x300')
app.mainloop()
