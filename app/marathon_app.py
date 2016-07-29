import requests
# Class that represents an Marathon App


class MarathonApp(object):

    def __init__(self, appid, marathon_host):
        self.appid = appid
        self.marathon_host = marathon_host
        self.uri = "http://{}:8080/v2/apps/{}".format(marathon_host, appid)
        self.average_usages = None
        self.tasks = {}
        self.get_app_details()

    def get_app_details(self):
        response = requests.get(self.uri).json()
        if (response['app']['tasks'] == []):
            print ('No task data on Marathon for App ! ', self.appid)
        else:
            self.instances_count = response['app']['instances']
            self.labels = response['app']['labels']

            try:
                self.image = response['app']['container']['docker']['image']
            except Exception as e:
                print ('probably not docker, setting app image to "" ')
                self.image = ""

            app_task_dict = {}
            for i in response['app']['tasks']:
                taskid = i['id']
                hostid = i['host']
                # print ('DEBUG - taskId=', taskid +' running on '+hostid)
                app_task_dict[str(taskid)] = str(hostid)
            self.tasks = app_task_dict
            return app_task_dict

    def is_suspended(self):
        if not self.tasks:
            return True
        return False
