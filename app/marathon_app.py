import requests
import logging
# Class that represents an Marathon App


class MarathonApp(object):

    def __init__(self, appid, marathon_host):
        self.appid = appid
        self.marathon_host = marathon_host
        self.uri = "http://{}:8080/v2/apps/{}".format(marathon_host, appid)
        self.average_usages = None
        self.tasks = {}
        self.labels = {}
        self.get_app_details()

    def get_app_details(self):
        response = requests.get(self.uri).json()
        if (response['app']['tasks'] == []):
            logging.info('No task data on Marathon for App ! ', self.appid)
        else:
            self.instances_count = response['app']['instances']
            self.labels = response['app'].get('labels', {})
            try:
                self.image = response['app']['container']['docker']['image']
            except Exception as e:
                logging.info('probably not docker, setting app image to "" ')
                self.image = ""

            app_task_dict = {}
            for i in response['app']['tasks']:
                taskid = i['id']
                hostid = i['host']

                app_task_dict[str(taskid)] = str(hostid)
            self.tasks = app_task_dict
            return app_task_dict

    def is_suspended(self):
        if not self.tasks:
            return True
        return False
