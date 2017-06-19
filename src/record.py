import os

if os.name == "nt":
    # DIRTY workaround from stackoverflow
    # when using scipy, a keyboard interrup will kill python
    # so nothing after catching the keyboard interrupt will
    # be executed

    import imp
    import ctypes
    import thread
    import win32api

    basepath = imp.find_module('numpy')[1]
    ctypes.CDLL(os.path.join(basepath, 'core', 'libmmd.dll'))
    ctypes.CDLL(os.path.join(basepath, 'core', 'libifcoremd.dll'))

    def handler(dwCtrlType, hook_sigint=thread.interrupt_main):
        if dwCtrlType == 0:
            hook_sigint()
            return 1
        return 0

    win32api.SetConsoleCtrlHandler(handler, 1)


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
