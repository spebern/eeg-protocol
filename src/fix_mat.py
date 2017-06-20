import scipy.io as sio
import argparse
from record_data import RecordData

parser = argparse.ArgumentParser(description="eeg experiment with pygame visualisation")
parser.add_argument("-m", "--mat", help="mat file to fix", required=True)

args = vars(parser.parse_args())

mat_file = args["mat"]

mat = sio.loadmat(mat_file)

# forgot age for on subject
if "age" not in mat:
    mat["age"] = 25

record_data = RecordData(mat["Fs"], mat["age"], gender=mat["gender"])

record_data.add_info          = mat["add_info"]
record_data.X                 = mat["X"]
record_data.Y                 = mat["Y"]
record_data.time_stamps       = mat["time_stamps"][0]
record_data.trial_time_stamps = mat["trial"][0]

record_data.stop_recording_and_dump(mat_file)
