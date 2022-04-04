import event
import logging

class Strategy(object):
    def __init__(self, queue):
        self.queue=queue
        self.dat = 0

        self.event=event.TickEvent(self.dat) #signal order
        self.queue.put(self.event)