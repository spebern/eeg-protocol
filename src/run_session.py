import pygame
import re
import sys
import time
import random
import json
import argparse
import screeninfo
import pylsl
from utils import time_str

parser = argparse.ArgumentParser(description="eeg experiment with pygame visualisation")
parser.add_argument("-f", "--Fs"           , help="sampling frequency"      , required=True, type=int)
parser.add_argument("-a", "--age"          , help="age of the subject"      , required=True, type=int)
parser.add_argument("-g", "--gender"       , help="gender of the subject"   , required=True)
parser.add_argument("-w", "--with_feedback", help="with additional feedback", type=bool)


args = vars(parser.parse_args())


def get_screen_width_and_height():
    monitor_info = screeninfo.get_monitors()[0]
    if not monitor_info:
        sys.exit("couldn't find monitor")
    m = re.match("monitor\((\d+)x(\d+)\+\d+\+\d+\)", str(monitor_info))

    screen_width, screen_height = int(m.group(1)), int(m.group(2))
    return screen_width, screen_height


screen_width, screen_height = get_screen_width_and_height()

black   = (0,   0, 0)
green   = (0, 255, 0)
radius  = 100
mid_pos = (screen_width // 2, screen_height // 2)

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("sounds/beep.mp3")

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
screen.fill(black)

red_arrow       = pygame.image.load("images/red_arrow.png")
red_arrow_left  = pygame.transform.rotate(red_arrow, 270)
red_arrow_right = pygame.transform.rotate(red_arrow, 90)

red_arrow_width, red_arrow_height = red_arrow_left.get_size()
red_arrow_right_pos = (screen_width - red_arrow_width, (screen_height - red_arrow_height) // 2)
red_arrow_left_pos  = (0                             , (screen_height - red_arrow_height) // 2)

happy_smiley = pygame.image.load("images/happy_smiley.png")
sad_smiley   = pygame.image.load("images/sad_smiley.png")

smiley_width, smiley_height = happy_smiley.get_size()
smiley_mid_pos = ((screen_width - smiley_width) // 2, (screen_height - smiley_height) // 2)


class RecordData():
    def __init__(self, trial_count, Fs, age, gender="male", with_feedback="with no feeback"):
        # timepoints when the subject starts imagination
        self.trial = []

        # containts the lables of the trials:
        # 1: left
        # 2: right
        # 3: both hands
        self.Y = []

        # sampling frequncy
        self.Fs = Fs

        self.gender   = gender
        self.age      = age
        self.add_info = "with feedback" if with_feedback else "with no feedback"
        self.i_trial = 0

    def __iter__(self):
        yield 'trial'   , self.trial
        yield 'Y'       , self.Y
        yield 'Fs'      , self.Fs
        yield 'gender'  , self.gender
        yield 'add_info', self.add_info

    def add_trial(self, label):
        self.trial.append(pylsl.local_clock())
        self.Y.append(label)

    def dump(self):
        file_name = "session_" + time_str() + ".json"
        print(file_name)

        with open(file_name, "w") as session_file:
            json.dump(dict(self), session_file)


def play_beep():
    pygame.mixer.music.play()


def run_trial(record_data, cue_pos_choices, with_feedback=False):
    screen.fill(black)
    pygame.display.update()
    time.sleep(3)

    pygame.draw.circle(screen, green, mid_pos, radius)
    pygame.display.update()
    time.sleep(1)

    # ensure that each cue pos will be equally chosen
    cue_pos = random.choice(list(cue_pos_choices.keys()))
    cue_pos_choices[cue_pos] -= 1
    if cue_pos_choices[cue_pos] == 0:
        del cue_pos_choices[cue_pos]

    if cue_pos == "left":
        screen.blit(red_arrow_left, red_arrow_left_pos)
        record_data.add_trial(1)
    elif cue_pos == "right":
        screen.blit(red_arrow_right, red_arrow_right_pos)
        record_data.add_trial(2)
    elif cue_pos == "both":
        screen.blit(red_arrow_right, red_arrow_right_pos)
        screen.blit(red_arrow_left, red_arrow_left_pos)
        record_data.add_trial(3)
    pygame.display.update()
    play_beep()

    time.sleep(6)
    play_beep()

    screen.fill(black)
    pygame.display.update()
    time.sleep(2)

    if with_feedback:
        smiley = random.choice([happy_smiley, sad_smiley])
        screen.blit(smiley, smiley_mid_pos)
        pygame.display.update()
        time.sleep(3)


def run_session(trial_count, Fs, age, gender="male", with_feedback=False):
    if trial_count % 3:
        raise ValueError("'trials' must be devisable by 3")

    record_data = RecordData(trial_count, Fs, age, gender, with_feedback)

    trial_count_for_each_cue_pos = trial_count // 3
    cue_pos_choices = {
        "left"  : trial_count_for_each_cue_pos,
        "right" : trial_count_for_each_cue_pos,
        "both"  : trial_count_for_each_cue_pos
    }

    for trial in range(0, trial_count):
        run_trial(record_data, cue_pos_choices, with_feedback=with_feedback)

    record_data.dump()


if __name__ == "__main__":
    run_session(75, args["Fs"], args["age"], \
                gender=args["gender"], with_feedback=args["with_feedback"])
