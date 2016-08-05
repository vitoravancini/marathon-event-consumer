import sys
import requests
import json
import math
import time
from marathon import Marathon
from marathon_app import MarathonApp
from sseclient import SSEClient

# shouldbe configurable
autoscale_label = "autoscale"
# input("Enter the DNS hostname or IP of your Marathon Instance : ")
marathon_host = '172.23.70.106'
MARATHON_POST_EVENT = 'api_post_event'


class EventProcessor(object):
    """Class for processing marathon events for EventProcessor"""

    def __init__(self):
        self.marathon = Marathon(marathon_host)
        self.monitored_labels = ['logentries']
        self.last_fetched_apps = self.get_monitored_apps()
        self.plugins = []
        # Reload on first run

    def plugin_decorator(self, plugin):
        self.plugins.append(plugin())
        return plugin

    def attach_to_marathon(self):
        print "Plugins loaded: {}".format(self.plugins)
        # Initilalize plugins
        for plugin in self.plugins:
            plugin_init = getattr(plugin, "init", None)
            if callable(plugin_init):
                plugin_init(self.last_fetched_apps)

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
        new_feteched_apps = self.get_monitored_apps()
        self.print_marathon_apps(new_feteched_apps)

        for plugin in self.plugins:
            try:
                monitored_apps_changed = plugin.apps_changed(self.last_fetched_apps, new_feteched_apps)
            except Exception as e:
                print "Plugin exception on apps comparison: {}".format(e)
                continue

            if monitored_apps_changed:
                print "Apps Changed due to: {}".format(plugin)
                try:
                    plugin.action(new_feteched_apps)
                except Exception as e:
                    print "Plugin exception on action: {}".format(e)

        self.last_fetched_apps = new_feteched_apps

    def print_marathon_apps(self, apps):
        print ("  Found Marathon apps: ")
        for app in apps:
            print(app.appid)

    def get_monitored_apps(self):
        monitored_apps = []
        for label in self.monitored_labels:
            monitored_apps = monitored_apps + self.marathon.get_all_apps_with_label(label)
        return monitored_apps

eventProcessor = EventProcessor()
plugin_decorator = eventProcessor.plugin_decorator
