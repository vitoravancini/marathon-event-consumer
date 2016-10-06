import sys
import requests
import json
import math
import logging
import time
from marathon import Marathon
from marathon_app import MarathonApp
from sseclient import SSEClient

# shouldbe configurable
autoscale_label = "autoscale"


class EventProcessor(object):
    """Class for processing marathon events for EventProcessor"""

    def __init__(self):
        # map from marathon event to array of plugins
        self.plugins_dict = {}

    def register_plugin(self, plugin):
        plugin_instance = plugin()

        plugin_event = plugin_instance.get_event_to_attach()
        self.plugins_dict.setdefault(plugin_event, []).append(plugin_instance)
        return plugin

    def attach_to_marathon(self, marathon_host):
        logging.info("Plugins loaded: {}".format(self.plugins_dict))
        self.marathon = Marathon(marathon_host)

        messages = SSEClient("http://" + marathon_host + ":8080/v2/events")
        msg_json = {}

        for msg in messages:
            try:
                msg_json = json.loads(msg.data)
            except Exception as e:
                logging.info("not json message: " + msg.data)

            if 'eventType' in msg_json:
                self.handle_message(msg_json)

    def handle_message(self, msg):
        logging.info('\n\nEVENT: ' + msg['eventType'])
        # fetch all marathon apps with specified labels

        new_feteched_apps = self.get_monitored_apps()
        event_plugins = self.plugins_dict.get(msg['eventType'], [])
        logging.info("Plugins triggered: ")
        logging.info(event_plugins)

        for plugin in event_plugins:
            try:
                monitored_apps_changed = plugin.apps_changed(new_feteched_apps)
            except Exception as e:
                logging.error("Plugin exception on apps comparison: {}".format(e))
                continue

            if monitored_apps_changed:
                logging.info("Apps with changes: {}, plugin {} taking action."
                             .format(monitored_apps_changed, plugin))
                try:
                    plugin.action(new_feteched_apps)
                except Exception as e:
                    logging.error("Plugin exception on action: {}".format(e))

    def print_marathon_apps(self, apps):
        logging.info("  Found Marathon apps: ")
        for app in apps:
            logging.info(app.appid)

    def get_monitored_apps(self):
        return self.marathon.get_all_apps()

eventProcessor = EventProcessor()
register_plugin = eventProcessor.register_plugin
