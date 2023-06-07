import time
import sys
import json
import subprocess
from datetime import datetime
from threading import Thread
from playsound import playsound
from pathlib import Path
from collections import OrderedDict

from pomodoro import paths

full_periods = 0

def on_work():
    Thread(target=playsound, args=(paths.sounds["ringbell"], )).start()
    subprocess.call(["notify-send",
        "Pomodoro", "Break has finished, go back to work!",
        f"--icon={paths.icon}"])


def on_break():
    global full_periods

    Thread(target=playsound, args=(paths.sounds["ringbell"], )).start()
    subprocess.call(["notify-send",
        "Pomodoro", "Take a break!",
        f"--icon={paths.icon}"])
    full_periods += 1


def on_selftest():
    Thread(target=playsound, args=(paths.sounds["ringbell"], )).start()
    subprocess.call(["notify-send",
        "Pomodoro", "Make an assignment!",
        f"--icon={paths.icon}"])

def states_sequencer():
    global states
    while True:
        key, val = next(iter(states.items()))
        yield key, val
        states.move_to_end(key)

def spinner():
    components = ("|", "/", "-", "\\")
    idx = 0

    while True:
        yield components[idx]
        idx = (idx + 1) % len(components)

class Timer:
    spinner_gen = spinner()

    def __init__(self, description, interval_sec, period):
        self.desc = description
        self.interval_sec = interval_sec
        self.period = period
        self.completed = False
        self.sec_elapsed = 0

    def run(self):
        if self.completed:
            self.completed = False
            self.sec_elapsed = 0

        while self.sec_elapsed < self.interval_sec:

            minutes = int(self.sec_elapsed)//60
            seconds = int(self.sec_elapsed)%60
            print("\r" + 80*" "+ f"\r🍅 🍅 🍅 ( {next(Timer.spinner_gen)} ) {self.desc : ^15} "
                f"{minutes:02d}:{seconds:02d}\t"
                f"({self.interval_sec//60}:{(self.interval_sec%60):02d})", end="")
            time.sleep(self.period)
            self.sec_elapsed += self.period

        self.completed = True

    def reset(self):
        self.completed = False
        self.sec_elapsed = 0

def get_current_time_formatted():
    return datetime.now().strftime("%Y:%m:%d-%H:%M:%S")

def cli():
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

    for state, interval in intervals.items():
        if interval == 0:
            del(states[state])


def save_stats(start_time: str, end_time: str, stats_file: Path, periods: int):

    with open(stats_file, "w") as logfile:
        log_data = {"session-start" : start_time,
                    "session-finish" : end_time,
                    "full-periods" : periods }
        json.dump(log_data, logfile)


intervals = {
        "work" : 600,
        "break" : 300,
        "selftest" : 450
        }


states = OrderedDict({
        "work" : on_work,
        "selftest" : on_selftest,
        "break": on_break
        })

interface_keys = {
    "n" : "Switch forward to the next sequence.",
    "c" : "Continue already started sequence.",
    "r" : "Repeat current sequence.",
    "s" : "Save stats and exit.",
    "any key" : "Exit."
}

exit_prompt = """I hope your work was fruitful. Thanks for using Pomodoro!"""

def main():
    cli()

    try:
        start_time = get_current_time_formatted()
        sequencer = states_sequencer()
        state_active = False

        while True:
            try:
                if not state_active:
                    state, action = next(sequencer)
                    timer = Timer(state, intervals[state], 0.3)
                    state_active = True

                action()
                timer.run()
                state_active = False
            except KeyboardInterrupt:
                prompt = "\n".join([f"{k: ^7} - {desc}" for k, desc in interface_keys.items()])
                user_input = input(f"\r\nTimer paused!\n{prompt}\nYour choice: ")

                if user_input == "n":
                    state_active = False
                elif user_input == "c":
                    pass
                elif user_input == "r":
                    timer.reset()
                    state_active = True
                elif user_input == "s":
                    current_time = get_current_time_formatted()
                    stats_file_path = Path(f"{paths.stats_dir}/{current_time}.json")
                    save_stats(start_time, current_time, stats_file_path, full_periods)
                    break
                else:
                    break

    except KeyboardInterrupt:
        # No specific handler for ctrl-c
        pass

    finally:
        print(f"\r{exit_prompt}")

if "__main__" == __name__:
    main()
