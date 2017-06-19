import pylsl
import atexit
import time
import scipy.io as sio
from utils import time_str

record_data = []
start_time = 0


def exit_handler():
    if start_time != 0:
        sio.savemat("recording_" + time_str() + ".mat", {"data" : record_data})


atexit.register(exit_handler)

streams = pylsl.resolve_stream('type', 'EEG')
inlet = pylsl.stream_inlet(streams[0])
start_time = time.time()

while True:
    sample, time_stamp = inlet.pull_sample()
    time_stamp += inlet.time_correction()

    # first col of one row of the record_data matrix is time_stamp,
    # the following cols are the sampled channels
    row = [time_stamp]
    row.extend(list(sample))
    record_data.append(row)
