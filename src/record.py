import pylsl
import scipy.io as sio
from utils import time_str

record_data = []
streams     = pylsl.resolve_stream('type', 'EEG')
inlet       = pylsl.stream_inlet(streams[0])


while True:
    try:
        sample, time_stamp = inlet.pull_sample()
        time_stamp += inlet.time_correction()

        # first col of one row of the record_data matrix is time_stamp,
        # the following cols are the sampled channels
        row = [time_stamp]
        row.extend(list(sample))
        record_data.append(row)
    except KeyboardInterrupt:
        sio.savemat("recording_" + time_str() + ".mat", {"data" : record_data})
        break
