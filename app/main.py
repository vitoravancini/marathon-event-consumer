from marathon_event_consumer import eventProcessor
from pluginsDir import *
import sys
import logging


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(levelname)s  %(message)s')
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)

    if (len(sys.argv)) >= 2:
        logging.info("App started")

        marathon_host = sys.argv[1]
        logging.info("Marathon host: " + marathon_host)
        eventProcessor.attach_to_marathon(marathon_host)
    else:
        logging.info("marathon host required")
