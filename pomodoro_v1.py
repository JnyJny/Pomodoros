# Pomodoro Timer

try:
    import winsound
except BaseException:
    pass

# Soundtrack: https://itunes.apple.com/us/album/emperor-of-sand/1195230194

from datetime import datetime
from time import sleep
from sys import stdout
from enum import Enum
from collections import OrderedDict


class PomodoroAlarm:
    _sndfile = {'countdown': 'C:/Windows/media/Speech On.wav',
                'warning': 'C:/Windows/media/Speech Off',
                'switch': 'C:/Windows/media/Windows Unlock'}

    COUNTDOWN = 'countdown'
    WARNING = 'warning'
    SWITCH = 'switch'

    def countdown(self, count=5, interval=1):
        """Play the break countdown sound.
        """
        for _ in range(count):
            self._play(self.COUNTDOWN)
            sleep(interval)

    def warning(self):
        """Play the warning sound.
        """
        self._play(self.WARNING)

    def switch(self):
        """Play the switch sound.
        """
        self._play(self.SWITCH)

    def _play(self, key):
        """
        """
        sndfile = self._sndfile[key]
        try:
            winsound.PlaySound(sndfile, winsound.SND_FILENAME)
        except BaseException:
            print(f'{key.upper()} Alarm!')


class State(Enum):
    # see pydoc3 Enum
    IDLE = 0
    WORKING = 1
    BREAK = 2
    WARNING = 3
    COUNTDOWN = 4
    DONE = 5


class PomodoroTimer:
    """
    """

    def __init__(self, periods=4, work_length=25, break_length=10):
        """Pomodoro Timer

             periods : optional integer
         work_length : optional integer
        break_length : optional integer

        This function initializes a PomodoroTimer object.
        """
        self.state = State.IDLE
        self.nperiods = 4
        self.work_length = work_length
        self.break_length = break_length
        self.alarm = PomodoroAlarm()

    def __str__(self):
        """This function is called whenever the object is used in a string
        context or the argument to the "str" function. It returns the string
        that should be printed.
        """

        if self.state == State.IDLE:
            return '\n'.join([f'    state: {self.state}',
                              f'# periods: {self.nperiods}',
                              f'     work: {self.work_length} minutes',
                              f'    break: {self.break_length} minutes', ])

        if self.state == State.WORKING:
            self.alarm.switch()
            return f'POMODORO #{self.period}/{self.nperiods} @ {self.now}'

        if self.state == State.BREAK:
            self.alarm.switch()
            return f"You've earned a {self.break_length} minute break!"

        if self.state == State.WARNING:
            self.alarm.warning()
            return f'30 Second Warning!'

        if self.state == State.COUNTDOWN:
            return f'5 Second Countdown!'

        if self.state == State.DONE:
            return f"Good work {self.nperiods} pomodoro's accomplished!"

        raise Exception(f'unknown state {self.state}')

    @property
    def state_machine(self):
        """Returns a list of State elements repeated nperiod times.
        The boundary conditions (IDLE and DONE) are trimmed from the
        repeated list.
        """

        l = [x for x in State if x not in [State.IDLE, State.DONE]]

        return l * self.nperiods

    def __iter__(self):
        """This function identifies the PomodoroTimer as an iterator
        object. When the object is used in a list or called with the
        "next" function it will iterate thru a list of values. The
        __next__ determines what values are returned.
        """
        self._states = self.state_machine
        self.period = 0
        return self

    def __next__(self):
        """This function is called when the object is used in an
        iterator context, like in a for loop or is the argument to
        the "next" function.  This function decides if it's time to
        complete the iteration (signaled by raising StopIteration) or
        returns a value to the caller.
        """
        try:
            self.state = self._states.pop(0)
            if self.state == State.WORKING:
                self.period += 1
            return self.state
        except IndexError:
            self.state = State.DONE
            raise StopIteration()

    @property
    def now(self):
        """Returns a string representation of the time HH:MM am/pm"""
        return datetime.now().strftime('%I:%M %p')

    @property
    def worktime(self):
        """Returns the number seconds in a work period."""
        return (self.work_length * 60) - (self.warntime + self.countdowntime)

    @property
    def breaktime(self):
        """Returns the number seconds in a break period."""
        return (self.break_length * 60) - (self.warntime + self.countdowntime)

    @property
    def warntime(self):
        """Number of seconds in a warning epoch.

        This is defined as a property to make it a read-only quantity
        instead of defining it in __init__.
        """
        return 25

    @property
    def countdowntime(self):
        """Number of seconds in a countdown.

        This is defined as a property to make it a read-only quantity
        instead of defining it in __init__.
        """
        return 5

    def start(self):
        """Begins a set of Pomodoro work/break intervals with a
        30 seconds warning before each state change and a 5 second
        countdown to the state change.
        """
        for state in self:

            print(self)

            if state == State.WORKING:
                sleep(self.worktime)
                continue

            if state == State.BREAK:
                sleep(self.breaktime)
                continue

            if state == State.WARNING:
                sleep(self.warntime)
                continue

            if state == State.COUNTDOWN:
                self.alarm.countdown(self.countdowntime)
                continue


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-i', '--intervals', type=int, default=4)
    parser.add_argument('-w', '--worktime', type=int, default=25)
    parser.add_argument('-b', '--breaktime', type=int, default=5)

    args = parser.parse_args()

    pomodoroTimer = PomodoroTimer(periods=args.intervals,
                                  work_length=args.worktime,
                                  break_length=args.breaktime)
    pomodoroTimer.start()
