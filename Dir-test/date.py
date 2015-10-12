__author__ = 'BoyChaiwat'
import time
x = "1"
xx = "1"

times = ["11:13:13", "03:13:13", "01:11:11", "11:12:01"]

print(times.index(min(times)))
print(time.strftime("%H:%M:%S"))
print(times)
times[2] = time.strftime("%H:%M:%S")
print(times)
