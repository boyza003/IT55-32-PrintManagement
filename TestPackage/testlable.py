import tkinter as tk
import time
import serial

check = serial.Serial("/dev/tty.SLAB_USBtoUART", 115200, timeout=0.1)
selectkey = bytes([0xBA, 0x02, 0x01, 0xB9])

i = 0
rx = ""
datarx = ""
def update_timeText():
    global i
    global rx
    global datarx
    # Get the current time, note you can change the format as you wish
    #current = time.strftime("%H:%M:%S")
    # Update the timeText Label box with the current time
    #timeText.configure(text=current)
    # Call the update_timeText() function after 1 second

    check.write(bytearray(selectkey))
    datarx = ''.join(format(x, '02x') for x in check.read(128))
    if datarx != "bd030101be":
        rx = datarx
        i = 5
        timeText.configure(text=rx)
    elif i == 0:
        i = 0
        timeText.configure(text="")
    elif i > 0:
        i -= 1
        timeText.configure(text=rx)
        print(rx)
    root.after(1000, update_timeText)


root = tk.Tk()
root.wm_title("Simple Clock Example")

# Create a timeText Label (a text box)
timeText = tk.Label(root, text="", font=("Helvetica", 15))
timeText.pack()
update_timeText()
root.mainloop()