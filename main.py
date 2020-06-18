import time
from datetime import datetime
import subprocess
from playsound import playsound
import sys


intervals = {
        "work" : 1500,
        "break": 300
        }

sounds = {
        "ringbell":"sounds/bell_sound.mp3"
        }

def on_work():
    playsound(sounds["ringbell"])
    current_time = datetime.now().strftime("%H:%M:%S") 
    subprocess.call(["notify", f"{current_time} Break has finished, go back to work!"])

def on_break():
    playsound(sounds["ringbell"])
    current_time = datetime.now().strftime("%H:%M:%S") 
    subprocess.call(["notify", f"{current_time} Take a break!"])

def next_state(state):
    if state == "work":
        return "break"
    else:
        return "work"

def timer(description, interval_sec):
    
    sec_elapsed = 0

    while sec_elapsed < interval_sec:
        time.sleep(1)
        sec_elapsed += 1
        minutes = sec_elapsed//60
        seconds = sec_elapsed%60
        print(f"\r{description} - {minutes:02d}:{seconds:02d}   ({interval_sec//60}:{(interval_sec%60):02d})", end="")

states = {
        "work" : on_work,
        "break": on_break
        }

def parse_args():
    if len(sys.argv) == 3:
        try:
            intervals["work"] = int(sys.argv[1])
            intervals["break"] = int(sys.argv[2])
        except ValueError:
            print("Bad arguments provided")
            quit()
    
    work_time = intervals["work"]//60
    break_time = intervals["break"]//60
    print(f"Using work: {work_time}mins break: {break_time}mins")

if "__main__" == __name__:


    parse_args()
    state = "work"
    full_periods = 0

    try:
        while True:
            states[state]()
            # time.sleep(intervals[state]) 
            timer(state ,intervals[state])
            state = next_state(state)
            full_periods += 1
    except KeyboardInterrupt:
        current_time = datetime.now().strftime("%H:%M:%S")
        filename = f"{current_time}_stat.log"
        with open(f"stats/{filename}", "w") as logfile:
            logfile.write(f"Session ended at {current_time}\nFull periods: {full_periods}")

