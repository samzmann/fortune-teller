import time

def getMillis():
    ms = time.time_ns() // 1_000_000
    return ms