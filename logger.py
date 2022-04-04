#log liftime of objects in the queue - time created, to time finished, to detect delays and jams
#ping connection to detect loss of connection
#log storage use
#import event

class Logger(object):
    
    def log_event(self, created, done):
        logfilename = 'log.txt'
        #print(event.created)
        #print(event.done)
        #print(event.done-event.created)
        logfile = open(logfilename, 'a+')
        line = str(created) + ' ' + str(done-created) + '\n' #str(created) + ' ' + str(done)# + ' ' + str(done-created)
        print(line, file=logfile)
        logfile.close()
