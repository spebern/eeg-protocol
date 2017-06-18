import libmushu
import time
import atexit
import numpy as np

record_data = []
start_time = int(time.time())


def exit_handler():
    np.save("record_data_{}.npy".format(start_time), record_data)
    amp.stop()


atexit.register(exit_handler)

available_amps = libmushu.get_available_amps()

ampname = available_amps[0]
amp = libmushu.get_amp(ampname)

amp.start()
while True:
    data, trigger = amp.get_data()
    np.append(record_data, [data, trigger])
