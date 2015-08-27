__author__ = 'BoyChaiwat'

from control import *
import tkinter as tk
import os
import time
import pymysql

LARGE_FONT = ("Verdana", 22)
TITLE_FONT = ("Helvetica", 16, "bold")
LIST_FONT = ("Helvetica", 24)
TIME_FONT = ("Helvetica", 16, "italic")

# Database connection
conn2boylogin = pymysql.connect(host='128.199.132.148', user='boy', passwd='boylogin', db='mydb')
cur2boylogin = conn2boylogin.cursor()
conn2local = pymysql.connect(host='128.199.132.148', user='boy', passwd='boylogin', db='mydb')
cur2local = conn2local.cursor()


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
                check = os.popen("sudo lpstat -o").read()
                print(check.find("print"))
                print(check[check.find("print") + 6:check.find("print") + 15])
                if check.find("print") >= 0:
                    getdate = os.popen("date").read()
                    # print("I have a new job")
                    cur2local.execute("SELECT id, JOB_ID FROM POOL WHERE time = (SELECT MIN(time) FROM POOL)")
                    row = cur2local.fetchone()
                    jobx = str(check[check.find("print") + 6:check.find("print") + 15]).strip()
                    joby = str(check[check.find("print") + 24:check.find("print") + 39]).strip()
                    cur2local.execute("INSERT INTO  JOB (job_id, page, job_in ) VALUES (%s, 0, NOW())", jobx)
                    print(jobx)
                    print(joby)
                    # print(row[0])
                    if row[0] == 1:
                        jobinpool1 = jobx
                        strmove = "sudo lpmove " + jobx + " pool1"
                        strhold = "sudo lp -i " + jobx + "-H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=CURTIME() WHERE id = 1", (int(jobx), joby))
                    elif row[0] == 2:
                        strmove = "sudo lpmove " + check[check.find("print") + 6:check.find("print") + 15] + " pool2"
                        strhold = "sudo lp -i " + check[check.find("print") + 6:check.find("print") + 15] + "-H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=%s WHERE id = 2",
                                          (int(check[check.find("print") + 6:check.find("print") + 15]),
                                           check[check.find("print") + 24:check.find("print") + 40], getdate[11:19]))
                    elif row[0] == 3:
                        print("pool3")
                        strmove = "sudo lpmove " + check[check.find("print") + 6:check.find("print") + 15] + " pool3"
                        strhold = "sudo lp -i " + check[check.find("print") + 6:check.find("print") + 15] + "-H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=%s WHERE id = 3",

                                          (int(check[check.find("print") + 6:check.find("print") + 15]),
                                           check[check.find("print") + 24:check.find("print") + 40], getdate[11:19]))
                    elif row[0] == 4:
                        strmove = "sudo lpmove " + check[check.find("print") + 6:check.find("print") + 15] + " pool4"
                        strhold = "sudo lp -i " + check[check.find("print") + 6:check.find("print") + 15] + "-H 06:00"
                        os.popen(strmove).read()
                        os.popen(strhold).read()
                        cur2local.execute("UPDATE POOL SET job_id=%s, job_from=%s, time=%s WHERE id = 4",
                                          (int(check[check.find("print") + 6:check.find("print") + 15]),
                                           check[check.find("print") + 24:check.find("print") + 40], getdate[11:19]))
                else:
                    print("I have no job")

            looppoolmanagement()

        def printjob1():
            stdid, ststusid = readcard()
            print(ststusid)
            if ststusid == 101:
                print("get")
                cur2local.execute("SELECT job_id, job_from FROM POOL WHERE id = 1")
                row = cur2local.fetchone()
                strmove = "sudo lpmove " + str(row[0]) + " get"
                strhold = "sudo lp -i " + str(row[0]) + " -H resume"
                os.popen(strmove).read()
                os.popen(strhold).read()
                cutcredit(stdid, row[1], row[0])

        # Button zone
        printcolor = tk.Button(self, text="Print", command=printjob1)
        printcolor.place(x=345, y=50)

        # write_slogan(printcolor)
        registerbutton = tk.Button(self, text="Register", command=lambda: controller.show_frame(Register))
        registerbutton.place(x=100, y=240)
        creditreportbutton = tk.Button(self, text="Credit report", command=lambda: controller.show_frame(CreditReport))
        creditreportbutton.place(x=200, y=240)

        # Show label list
        job1 = tk.Label(self, font=LIST_FONT)
        getjobfrom(job1)


class Register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        headlabel = tk.Label(self, text="Register", font=LARGE_FONT)
        headlabel.pack(pady=10, padx=10)
        stdidlable = tk.Label(self, text="Student ID : ", font=LARGE_FONT)
        stdidlable.place(x=20, y=50)
        creditlable = tk.Label(self, text="Balanace : ", font=LARGE_FONT)
        creditlable.place(x=20, y=100)

        def clickregister():
            try:
                x, y = readcard()
                cur2boylogin.execute("SELECT * FROM STUDENT WHERE id=%s", x)
                row = cur2boylogin.fetchone()
                if row[0] == x:
                    cur2boylogin.execute("INSERT INTO CREDIT(credit_balance, status,student_id) VALUES (100,101,%s)",
                                         row[0])
                    stdidlable = tk.Label(self, text=x, font=LARGE_FONT)
                    stdidlable.place(x=170, y=50)
                    creditlable = tk.Label(self, text="100", font=LARGE_FONT)
                    creditlable.place(x=145, y=100)
            except Exception as e:
                print(e)

        button1 = tk.Button(self, text="Read card", command=clickregister)
        button1.place(x=340, y=180)
        button2 = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        button2.place(x=350, y=230)


class CreditReport(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        headlabel = tk.Label(self, text="Credit report", font=LARGE_FONT)
        headlabel.pack(pady=10, padx=10)
        stdidlable = tk.Label(self, text="Student ID : ", font=LARGE_FONT)
        stdidlable.place(x=20, y=50)
        creditlable = tk.Label(self, text="Balanace : ", font=LARGE_FONT)
        creditlable.place(x=20, y=100)

        stdidlable2 = tk.Label(self, font=LARGE_FONT)
        stdidlable2.place(x=170, y=50)
        creditlable2 = tk.Label(self, font=LARGE_FONT)
        creditlable2.place(x=145, y=100)

        def checkcredit():
            stdidlable2.config(text="")
            creditlable2.config(text="")
            try:
                x, y = readcard()
                cur2boylogin.execute("SELECT credit_balance FROM CREDIT WHERE student_id = %s", x)
                row = cur2boylogin.fetchone()
                if row[0] > 0:
                    stdidlable2.config(text=x)
                    creditlable2.config(text=y)
            except Exception as e:
                print(e)

        readcardbutton = tk.Button(self, text="Read card", command=checkcredit)
        readcardbutton.place(x=340, y=180)
        backtohomebutton = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        backtohomebutton.place(x=350, y=230)


app = SeaofBTCapp()
app.geometry('480x300')
app.mainloop()

#comment