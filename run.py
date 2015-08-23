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
conn2boylogin = pymysql.connect(host='boylogin.me', port=3306, user='boy', passwd='boylogin', db='mydb')
cur2boylogin = conn2boylogin.cursor()
conn2local = pymysql.connect(host='boylogin.me', port=3306, user='boy', passwd='boylogin', db='mydb')
cur2local = conn2local.cursor()


class SeaofBTCapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, CreditReport):
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
        printcolor = tk.Button(self, text="Print")
        printcolor.place(x=345, y=50)

        # write_slogan(printcolor)
        registerbutton = tk.Button(self, text="Register", command=lambda: controller.show_frame(PageOne))
        registerbutton.place(x=100, y=240)
        creditreportbutton = tk.Button(self, text="Credit report", command=lambda: controller.show_frame(CreditReport))
        creditreportbutton.place(x=200, y=240)

        # Show label list
        job1 = tk.Label(self, font=LIST_FONT)
        getjobfrom(job1)


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(CreditReport))
        button2.pack()


class CreditReport(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        headlabel = tk.Label(self, text="Credit report", font=LARGE_FONT)
        headlabel.pack(pady=10, padx=10)
        stdidlable = tk.Label(self, text="Student ID : ", font=LARGE_FONT)
        stdidlable.place(x=20, y=50)
        creditlable = tk.Label(self, text="Balanace : ", font=LARGE_FONT)
        creditlable.place(x=20, y=100)

        def checkcredit():
            global stdidlable
            global creditlable
            x, y = readcard()
            cur2boylogin.execute("SELECT credit_balance FROM CREDIT WHERE student_id = %s", x)
            row = cur2boylogin.fetchone()
            if row[0] > 0:
                stdidlable = tk.Label(self, text=x, font=LARGE_FONT)
                stdidlable.place(x=170, y=50)
                creditlable = tk.Label(self, text=row[0], font=LARGE_FONT)
                creditlable.place(x=145, y=100)

        readcardbutton = tk.Button(self, text="Read card", command=checkcredit)
        readcardbutton.place(x=340, y=180)
        backtohomebutton = tk.Button(self, text="Back", command=lambda: controller.show_frame(PageOne))
        backtohomebutton.place(x=350, y=230)

app = SeaofBTCapp()
app.geometry('480x300')
app.mainloop()
