import time
import sys
import json
import subprocess
from datetime import datetime
from threading import Thread
from playsound import playsound
from pathlib import Path
from collections import OrderedDict

app_path_abs = Path(__file__).resolve().parent
pomodoro_icon_path = app_path_abs.joinpath("icons/tomato.png")


def on_work():
    Thread(target=playsound, args=(sounds["ringbell"], )).start()
    subprocess.call(["notify-send",
        "Pomodoro", "Break has finished, go back to work!",
        f"--icon={pomodoro_icon_path}"])


def on_break():
    Thread(target=playsound, args=(sounds["ringbell"], )).start()
    subprocess.call(["notify-send",
        "Pomodoro", "Take a break!",
        f"--icon={pomodoro_icon_path}"])


def on_selftest():
    Thread(target=playsound, args=(sounds["ringbell"], )).start()
    subprocess.call(["notify-send",
        "Pomodoro", "Make an assignment!",
        f"--icon={pomodoro_icon_path}"])


def states_sequencer():
    global states
    while True:
        key, val = next(iter(states.items()))
        yield key, val
        states.move_to_end(key)

def infinite_spinner(direction):
    components = ("|", "/", "-", "\\")
    idx = 0

    while True:
        yield components[idx]
        if direction == "right":
            idx = (idx + 1) % len(components)
        else:
            idx = (idx - 1) % len(components)

left_spinner = infinite_spinner("left")
right_spinner = infinite_spinner("right")

def timer(description, interval_sec, period):

    sec_elapsed = 0

    while sec_elapsed < interval_sec:

        minutes = int(sec_elapsed)//60
        seconds = int(sec_elapsed)%60
        print("\r" + 80*" "+ f"\r🍅 🍅 🍅 ( {next(left_spinner)} ) {description : ^15} "
              f"{minutes:02d}:{seconds:02d}\t"
              f"({interval_sec//60}:{(interval_sec%60):02d})", end="")
        time.sleep(period)
        sec_elapsed += period

def parse_args():
    global intervals
    if len(sys.argv) == 4:
        try:
            intervals["work"] = int(sys.argv[1])
            intervals["break"] = int(sys.argv[2])
            intervals["selftest"] = int(sys.argv[3])
        except ValueError:
            print(f"Bad arguments provided. Use following way:\n"\
                   "pomodoro [[work] [break] [selftest]]\n"\
                   "Intervals are expressed in seconds")
            quit()

    work_time_m = intervals["work"]//60
    work_time_s = intervals["work"]%60
    break_time_m = intervals["break"]//60
    break_time_s = intervals["break"]%60
    selftest_time_m = intervals["selftest"]//60
    selftest_time_s = intervals["selftest"]%60
    print(f"Working with following settings:\n"
          f"work -> ({work_time_m:02d}:{work_time_s:02d}) "
          f"break -> ({break_time_m:02d}:{break_time_s:02d}) "
          f"selftest -> ({selftest_time_m:02d}:{selftest_time_s:02d})\n\n")


intervals = {
        "work" : 600,
        "break" : 300,
        "selftest" : 450
        }


sounds = {
        "ringbell" : str(app_path_abs.joinpath("sounds/bell_sound.mp3"))
        }


states = OrderedDict({
        "work" : on_work,
        "selftest" : on_selftest,
        "break": on_break
        })

if "__main__" == __name__:

    parse_args()
    begin_time = datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
    full_periods = 0

    try:
        for state, func in states_sequencer():
            func()
            timer(state, intervals[state], 0.3)
            full_periods += 1
    except KeyboardInterrupt:
        current_time = datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
        filename = f"{current_time}.json"
        with open(f"stats/{filename}", "w") as logfile:
            log_data = {"session-start" : begin_time,
                        "session-finish" : current_time,
                        "full-periods" : full_periods }
            json.dump(log_data, logfile)
