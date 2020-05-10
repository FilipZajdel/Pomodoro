import time
from datetime import datetime
import subprocess
from playsound import playsound


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

states = {
        "work" : on_work,
        "break": on_break
        }

if "__main__" == __name__:
    state = "work"
    full_periods = 0

    try:
        while True:
            states[state]()
            time.sleep(intervals[state]) 
            state = next_state(state)
            full_periods += 1
    except KeyboardInterrupt:
        current_time = datetime.now().strftime("%H:%M:%S")
        filename = f"{current_time}_stat.log"
        with open(f"stats/{filename}", "w") as logfile:
            logfile.write(f"Session ended at {current_time}\nFull periods: {full_periods}")


        
