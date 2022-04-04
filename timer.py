#class to generate regular events

#every minute:
#every hour: adjust risk?
#every day/end of day: create report
#every morning: create daily outlook
#every month: earnings report?
#every year: taxation

import datetime as dt
import event

class Timer(object):
    def __init__(self):
        self.live = False
        self.hour = None
        self.day = None
        self.week = None
        self.month = None
        self.year = None

    def chkTimer(self, env, time):
        if self.live:
            if time.hour > self.hour:
                self.event=event.HourEvent()
                env['queue'].put(self.event)
            if time.day > self.day:
                self.event=event.DayEvent()
                env['queue'].put(self.event)
            if time.isocalendar()[1] > self.week:
                self.event=event.WeekEvent()
                env['queue'].put(self.event)
            if time.month > self.month:
                self.event=event.MonthEvent()
                env['queue'].put(self.event)
            if time.year > self.year:
                self.event=event.YearEvent()
                env['queue'].put(self.event)

        elif self.live == False:    #avoiding event call on first tick
            self.hour = time.hour
            self.day = time.day
            self.week = time.isocalendar()[1]
            self.month = time.month
            self.year = time.year