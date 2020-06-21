import time
from datetime import datetime
import subprocess
from threading import Thread
from playsound import playsound
import sys
import json

POMODORO_PATH = "/home/filip/Projects/pomodoro"
ICON_PATH = f"{POMODORO_PATH}/icons/tomato.png"

def on_work():
    Thread(target=playsound, args=(sounds["ringbell"], )).start()
    subprocess.call(["notify-send", 
        "Pomodoro", "Break has finished, go back to work!",
        f"--icon={ICON_PATH}"])


def on_break():
    Thread(target=playsound, args=(sounds["ringbell"], )).start()
    subprocess.call(["notify-send", 
        "Pomodoro", "Take a break!",
        f"--icon={ICON_PATH}"])


def next_state(state):
    if state == "work":
        return "break"
    else:
        return "work"


def timer(description, interval_sec):
    
    sec_elapsed = 0

    while sec_elapsed < interval_sec:
        
        minutes = sec_elapsed//60
        seconds = sec_elapsed%60
        print("\r" + 80*" "+ f"\r{description} - {minutes:02d}:{seconds:02d}\t"
            f"({interval_sec//60}:{(interval_sec%60):02d})", end="")
        time.sleep(1)
        sec_elapsed += 1

def parse_args():
    if len(sys.argv) == 3:
        try:
            intervals["work"] = int(sys.argv[1])
            intervals["break"] = int(sys.argv[2])
        except ValueError:
            print("Bad arguments provided")
            quit()
    
    work_time_m = intervals["work"]//60
    work_time_s = intervals["work"]%60
    break_time_m = intervals["break"]//60
    break_time_s = intervals["break"]%60
    print(f"Using work: {work_time_m:02d}:{work_time_s:02d} "
        f"break: {break_time_m:02d}:{break_time_s:02d}")


intervals = {
        "work" : 1500,
        "break": 300
        }


sounds = {
        "ringbell":f"{POMODORO_PATH}/sounds/bell_sound.mp3"
        }


states = {
        "work" : on_work,
        "break": on_break
        }


if "__main__" == __name__:

    parse_args()
    begin_time = datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
    state = "work"
    full_periods = 0

    try:
        while True:
            states[state]()
            timer(state ,intervals[state])
            state = next_state(state)
            full_periods += 1
    except KeyboardInterrupt:
        current_time = datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
        filename = f"{current_time}.json"
        with open(f"stats/{filename}", "w") as logfile:
            log_data = {"session-start" : begin_time,
                        "session-finish" : current_time,
                        "full-periods" : full_periods }
            json.dump(log_data, logfile)

