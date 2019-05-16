from stoplight import Stoplight
from time import sleep
import threading


def blink(pin, interval, duration):
    oscilations = duration/(interval * 2)
    for i in range(int(oscilations)):
        print("pin ON")
        sleep(interval)
        print("pin OFF")
        sleep(interval)


thread = threading.Thread(target=blink, args=("", 0.75, 10))
thread.start()
print("Spun off thread")
sleep(3)
print("multithreaded!")

# blink("", 0.75, 10)
