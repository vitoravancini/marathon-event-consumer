from marathon_event_consumer import eventProcessor
from pluginsDir import *
import sys

if __name__ == "__main__":
    if (len(sys.argv)) >= 2:
        marathon_host = sys.argv[1]
        print marathon_host
        eventProcessor.attach_to_marathon(marathon_host)
    else:
        print "marathon host required"
