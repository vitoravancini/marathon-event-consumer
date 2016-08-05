from marathon_event_consumer import eventProcessor
from pluginsDir import *

if __name__ == "__main__":
    print ("This application tested with Python3 onlyxx")
    eventProcessor.attach_to_marathon()
