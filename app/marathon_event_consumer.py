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


class EventProcessor(object):
    """Class for processing marathon events for EventProcessor"""

    def __init__(self):
        self.marathon = Marathon(marathon_host)
        self.monitored_labels = ['logentries']

        # map from marathon event to array of plugins
        self.plugins_dict = {}

    def register_plugin(self, plugin):
        print ("register")
        plugin_instance = plugin()

        plugin_event = plugin_instance.get_event_to_attach()
        self.plugins_dict.setdefault(plugin_event, []).append(plugin_instance)
        return plugin

    def attach_to_marathon(self):
        print "Plugins loaded: {}".format(self.plugins_dict)

        messages = SSEClient("http://" + marathon_host + ":8080/v2/events")
        for msg in messages:
            try:
                msg_json = json.loads(msg.data)
            except Exception as e:
                print ("not json message: " + msg.data)

            if 'eventType' in msg_json:
                self.handle_message(msg_json)

    def handle_message(self, msg):
        print('\n\nEVENT: ' + msg['eventType'])
        # fetch all marathon apps with specified labels
        new_feteched_apps = self.get_monitored_apps()
        event_plugins = self.plugins_dict.get(msg['eventType'], [])
        print event_plugins
        for plugin in event_plugins:
            try:
                monitored_apps_changed = plugin.apps_changed(new_feteched_apps)
            except Exception as e:
                print "Plugin exception on apps comparison: {}".format(e)
                continue

            print monitored_apps_changed
            if monitored_apps_changed:
                print "Apps Changed for: {}".format(plugin)
                try:
                    plugin.action(new_feteched_apps)
                except Exception as e:
                    print "Plugin exception on action: {}".format(e)

    def print_marathon_apps(self, apps):
        print ("  Found Marathon apps: ")
        for app in apps:
            print(app.appid)

    def get_monitored_apps(self):
        return self.marathon.get_all_apps()

eventProcessor = EventProcessor()
register_plugin = eventProcessor.register_plugin
