import sys
import requests
import json
import math
import time
from marathon import Marathon
from marathon_app import MarathonApp
from sseclient import SSEClient
from template.template_engine import TemplateEngine

# shouldbe configurable
autoscale_label = "autoscale"
# input("Enter the DNS hostname or IP of your Marathon Instance : ")
marathon_host = '172.23.70.147'
MARATHON_POST_EVENT = 'api_post_event'


class EventProcessor(object):
    """Class for processing marathon events for EventProcessor"""

    def __init__(self):
        self.marathon = Marathon(marathon_host)
        self.monitored_labels = ['logentries']
        self.last_fetched_apps = self.get_monitored_apps()
        self.template_engine = TemplateEngine()


    def attach_to_marathon(self):
        messages = SSEClient("http://" + marathon_host + ":8080/v2/events")
        for msg in messages:
            try:
                msg_json = json.loads(msg.data)
            except Exception as e:
                print ("not json message: " + msg.data)

            if 'eventType' in msg_json and msg_json['eventType'] == MARATHON_POST_EVENT:
                self.handle_message(msg_json)

    def handle_message(self, msg):
        # fetch all marathon apps with specified labels
        current_apps = self.get_monitored_apps()
        self.print_marathon_apps(current_apps)

        monitored_apps_changed = not self.are_equal(current_apps, self.last_fetched_apps)
        print monitored_apps_changed
        if monitored_apps_changed:
            self.reload_rsyslog_config(current_apps)
            self.last_fetched_apps = current_apps
        else:
            print 'nothing changed'

    def print_marathon_apps(self, apps):
        print ("  Found Marathon apps: ")
        for app in apps:
            print(app.appid)

    def are_equal(self, apps1, apps2):
        # if number of monitored apps changed return false.
        if len(apps1) != len(apps2):
            return False

        set_apps_1 = set()
        for app in apps1:
            appid = app.appid
            set_apps_1.add((appid, tuple(app.labels.items())))

        set_apps_2 = set()
        for app in apps2:
            appid = app.appid
            set_apps_2.add((appid, tuple(app.labels.items())))

        return set_apps_2 == set_apps_1

    def reload_rsyslog_config(self, apps):
        self.template_engine.reload_rsyslog_template(apps)

    def get_monitored_apps(self):
        monitored_apps = []
        for label in self.monitored_labels:
            monitored_apps = monitored_apps + self.marathon.get_all_apps_with_label(label)
        return monitored_apps

if __name__ == "__main__":
    print ("This application tested with Python3 only")
    # temp_engine = TemplateEngine()
    # app1 = (MarathonApp('nginx-helloworld', "172.23.70.147"))
    # apps = [app1]
    # temp_engine.reload_rsyslog_template(apps)

    EventProcessor().attach_to_marathon()
