import os
import datetime

file = open("file.txt", "w")
# while True:
file.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
file.flush()





