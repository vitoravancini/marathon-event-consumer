from marathon_event_consumer import eventProcessor
from pluginsDir import *
import sys
import logging


if __name__ == "__main__":
    if (len(sys.argv)) >= 2:
        logging.basicConfig(filename='/var/log/marathon-event-consumer.log', level=logging.INFO)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

        logging.info("App started")
        marathon_host = sys.argv[1]
        logging.info("Marathon host: " + marathon_host)
        eventProcessor.attach_to_marathon(marathon_host)
    else:
        logging.info("marathon host required")
