#!/usr/bin/env python3

import sched
import time
from datetime import datetime

class PomodoroAlarm:

    def __init__(self, message=None, delay=0):
        self.msg = message or ''
        self.delay = delay

    def __str__(self):
        now = datetime.now().strftime('%I:%m %p')
        return f'{self.msg} @ {now}'
    
    def __call__(self):
        print(self)

        
class WorkAlarm(PomodoroAlarm):

    def __init__(self, duration, delay):
        super().__init__(f'{duration} Minute Work Pomodoro', delay)

    def __call__(self, phase):
        self.msg += f' #{phase} Starting'
        super().__call__()
        
class RestAlarm(PomodoroAlarm):
    
    def __init__(self, duration, delay):
        super().__init__(f'{duration} Minute Rest Pomodoro Starting', delay)

class WarnAlarm(PomodoroAlarm):
    
    def __init__(self, duration, delay):
        super().__init__(f'{duration} seconds left', delay)

class CountdownAlarm(PomodoroAlarm):
    
    def __init__(self, duration, delay):
        self.duration = duration
        self.delay = delay
        
    def __call__(self):
        for t in range(self.duration, 0, -1):
            print(f'{t} ', end='' if t != 1 else '\n', flush=True)
            time.sleep(1)

class PomodoroTimer:
    def __init__(self, work=25, rest=5, intervals=4):
        """
             work : optional integer, work period in minutes
             rest : optional integer, rest period in minutes
        intervals : optional integer, number of work/rest periods
        """
        self.intervals = intervals
        self.work = work
        self.rest = rest
        self.warn = 30          # seconds
        self.countdown = 5      # seconds
        self.sched = sched.scheduler(time.time, time.sleep)

    def __repr__(self):

        s = [ self.__class__.__name__, '(',
              f'work={self.work}, ',
              f'rest={self.rest}, ',
              f'intervals={self.intervals})']
        return ''.join(s)

    @property
    def work_alarm(self):
        try:
            return self._work_alarm
        except AttributeError:
            pass
        self._work_alarm = WorkAlarm(self.work, 0)
        return self._work_alarm

    @property
    def warn_alarm(self):
        try:
            return self._warn_alarm
        except AttributeError:
            pass

        self._warn_alarm = WarnAlarm(self.warn,
                                     (self.work * 60) - self.warn)
        return self._warn_alarm

    @property
    def rest_alarm(self):
        try:
            return self._rest_alarm
        except AttributeError:
            pass
        self._rest_alarm = RestAlarm(self.rest, self.work * 60)
        return self._rest_alarm
    
    @property
    def countdown_alarm(self):
        try:
            return self._countdown_alarm
        except AttributeError:
            pass
        self._countdown_alarm = CountdownAlarm(self.countdown,
                                               (self.work*60)-self.countdown)
        return self._countdown_alarm

    def start(self):
        
        for interval in range(self.intervals):
            # The priority argument in sched.enter is used to make
            # sure that scheduled jobs are completed in order.
            self.sched.enter(self.work_alarm.delay, 1,
                             self.work_alarm, (interval+1,))

            self.sched.enter(self.warn_alarm.delay, 2,
                             self.warn_alarm, ())
            
            self.sched.enter(self.countdown_alarm.delay, 3,
                             self.countdown_alarm, ())
            
            self.sched.enter(self.rest_alarm.delay, 4,
                             self.rest_alarm, ())
            
            self.sched.enter(self.warn_alarm.delay, 5,
                             self.warn_alarm, ())
            
            self.sched.enter(self.countdown_alarm.delay, 6,
                             self.countdown_alarm, ())
            # Only one interval is scheduled at a time to avoid
            # having to calculate all the accumulated delays.
            # We could but it's error prone. It's easier to prove
            # to ourselves that this interval is scheduled correctly.
            self.sched.run()
            
    
if __name__ == '__main__':

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-w', '--work', type=int, default=25)
    parser.add_argument('-r', '--rest', type=int, default=10)
    parser.add_argument('-i', '--intervals', type=int, default=4)

    args = parser.parse_args()
    
    pomodoroTimer = PomodoroTimer(work=args.work,
                                  rest=args.rest,
                                  intervals=args.intervals)
    pomodoroTimer.start()
