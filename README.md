## Pomodoro Timer

The **Pomodoro** is a tool aimed to boost your productivity. It is used just like a traditional timer when following the [pomodoro technique](https://en.wikipedia.org/wiki/Pomodoro_Technique) while working/studying/researching. This particular tool introduces yet another step that can be added to each session - *self check*. It helps to solve some small tasks to apply the gained knowledge right away.


### Installation
```
$ pip install -r requirements.txt
$ pip install -e .
```

### Usage
```
$ pomodoro # to run with default intervals
```
...
or
...
```
$ pomodoro <work> <break> <self-check> # to run with your own intervals (seconds)
```

During each run you can pause the timer using *[CTRL-C]* and choose one of the following options:

* n : Switch forward to the next interval
* c : Continue paused interval
* r : Repeat current interval
* s : Save and exit
* any other key will result in exit without saving.

### Statistics
Whenever you exit Pomodoro and save the stats (*s*) they will be saved
in the **stats** directory located in the directory where Pomodoro was cloned to. Each session is
saved in the json file named after the time of the session's beginning.
