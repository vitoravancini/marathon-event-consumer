# Class that represents the marathon api
import logging
import requests
from marathon_app import MarathonApp


class Marathon(object):

    def __init__(self, marathon_host):
        self.host = marathon_host
        self.uri = ("http://" + marathon_host + ":8080")

    def get_all_apps(self):
        autoscale_endpoint = "/v2/apps"
        response = requests.get(self.uri + autoscale_endpoint).json()

        if response['apps'] == []:
            logging.info("No Apps found on Marathon")
        else:
            marathon_apps = []

            for app in response['apps']:
                appid = app['id'].strip('/')
                marathon_apps.append(MarathonApp(appid, self.host))

            return marathon_apps

    def get_all_apps_with_label(self, label):
        endpoint = "/v2/apps?label={}".format(label)
        response = requests.get(self.uri + endpoint).json()

        if response['apps'] == []:
            logging.info("No Apps found on Marathon for label {}".format(label))
            return []
        else:
            apps = []
            for i in response['apps']:
                appid = i['id'].strip('/')
                apps.append(MarathonApp(appid, self.host))

        return apps
