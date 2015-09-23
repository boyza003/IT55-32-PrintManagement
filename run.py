__author__ = 'BoyChaiwat'

from control import *
import tkinter as tk
import os
import time
import pymysql

LARGE_FONT = ("Verdana", 18)
TITLE_FONT = ("Helvetica", 16, "bold")
LIST_FONT = ("Helvetica", 24)
TIME_FONT = ("Helvetica", 14, "italic")

# Database connection
conn2local = pymysql.connect(host='boylogin.me', user='boy', passwd='boylogin', db='mydb')

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
        detailjobdate.place(x=200, y=2)
        detailjobdate.pi = detailjobdate.place_info()
        delailjobink = tk.Label(self, text="", font=TIME_FONT)
        delailjobink.place(x=390, y=2)
        delailjobink.pi = delailjobink.place_info()

        # Job1
        def getjobfrom(label):
            def looppoolmanagement():
                global getText
                global jobinpool1
               # global cur2local
                #cur2local = conn2local.cursor()
                
                # Pool1
               #cur2local.execute("SELECT * FROM POOL WHERE id = 1")
                #row = cur2local.fetchone()
                #labeljob1from = tk.Label(self, text=row[2], font=LIST_FONT)
                #labeljob1from.place(x=20, y=25)
                #lablejob1time = tk.Label(self, text=row[3], font=TIME_FONT)
                #lablejob1time.place(x=200, y=35)

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
                check = os.popen("lpstat -o").read()
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
                        strmove = "lpmove " + getjobid + " pool1"
                        strhold = "lp -i " + getjobid + " -H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=CURTIME() WHERE id = 1",
                                          (int(getjobid), gethostname))
                        labeljob1from = tk.Label(self, text=gethostname, font=LIST_FONT)
                        labeljob1from.place(x=20, y=25)
                        lablejob1time = tk.Label(self, text=str(time.strftime("%H:%M:%S")), font=TIME_FONT)
                        lablejob1time.place(x=200, y=35)

                    elif row[0] == 2:
                        strmove = "lpmove " + getjobid + " pool2"
                        strhold = "lp -i " + getjobid + " -H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=CURTIME() WHERE id = 2",
                                          (int(getjobid), gethostname))
                        labeljob1from = tk.Label(self, text=gethostname, font=LIST_FONT)
                        labeljob1from.place(x=20, y=70)
                        lablejob1time = tk.Label(self, text=str(time.strftime("%H:%M:%S")), font=TIME_FONT)
                        lablejob1time.place(x=200, y=80)

                    elif row[0] == 3:
                        strmove = "lpmove " + getjobid + " pool3"
                        strhold = "lp -i " + getjobid + " -H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=CURTIME() WHERE id = 3",
                                          (int(getjobid), gethostname))
                        labeljob1from = tk.Label(self, text=gethostname, font=LIST_FONT)
                        labeljob1from.place(x=20, y=115)
                        lablejob1time = tk.Label(self, text=str(time.strftime("%H:%M:%S")), font=TIME_FONT)
                        lablejob1time.place(x=200, y=127)

                    elif row[0] == 4:
                        jobinpool1 = getjobid
                        strmove = "lpmove " + getjobid + " pool4"
                        strhold = "lp -i " + getjobid + " -H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=CURTIME() WHERE id = 4",
                                          (int(getjobid), gethostname))
                        labeljob1from = tk.Label(self, text=gethostname, font=LIST_FONT)
                        labeljob1from.place(x=20, y=160)
                        lablejob1time = tk.Label(self, text=str(time.strftime("%H:%M:%S")), font=TIME_FONT)
                        lablejob1time.place(x=200, y=173)

                else:
                    print("I have no job")
                label.config(text=str(getText))
                label.after(1000, looppoolmanagement)
            looppoolmanagement()

        def print1():
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

        def restartcups():
            os.popen("sudo service cups restart").read()

        # Print button zone
        printjob1 = tk.Button(self, text="Print", command=print1)
        printjob1.place(x=395, y=30)
        printjob2 = tk.Button(self, text="Print", command=print2)
        printjob2.place(x=395, y=80)
        printjob3 = tk.Button(self, text="Print", command=print3)
        printjob3.place(x=395, y=130)
        printjob4 = tk.Button(self, text="Print", command=print4)
        printjob4.place(x=395, y=180)

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
