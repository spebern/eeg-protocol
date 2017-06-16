import pygame
import re
import sys
import time
import random
import argparse
import screeninfo

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

screen = pygame.display.set_mode((screen_width, screen_height))
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


def play_beep():
    pygame.mixer.music.play()


def run_trial(cue_pos_choices, with_feedback=False):
    screen.fill(black)
    pygame.display.update()
    time.sleep(3)

    pygame.draw.circle(screen, green, mid_pos, radius)
    pygame.display.update()
    time.sleep(1)

    play_beep()

    # ensure that each cue pos will be equally chosen
    cue_pos = random.choice(list(cue_pos_choices.keys()))
    cue_pos_choices[cue_pos] -= 1
    if cue_pos_choices[cue_pos] == 0:
        del cue_pos_choices[cue_pos]

    if cue_pos == "left":
        screen.blit(red_arrow_left, red_arrow_left_pos)
    elif cue_pos == "right":
        screen.blit(red_arrow_right, red_arrow_right_pos)
    elif cue_pos == "both":
        screen.blit(red_arrow_right, red_arrow_right_pos)
        screen.blit(red_arrow_left, red_arrow_left_pos)
    pygame.display.update()

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


def run_session(trials=75):
    if trials % 3:
        raise ValueError("'trials' must be devisable by 3")

    cue_pos_choices = {
        "left"  : trials // 3,
        "right" : trials // 3,
        "both"  : trials // 3,
    }
    for trial in range(0, trials):
        run_trial(cue_pos_choices)


if __name__ == "__main__":
    # run_session(75, args["Fs"], args["age"], args["gender"], args["with_feedback"])
    run_session(3, args["Fs"], args["age"], args["gender"], args["with_feedback"])
