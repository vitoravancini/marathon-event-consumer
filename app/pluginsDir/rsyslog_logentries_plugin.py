from marathon_event_consumer import register_plugin
from template.template_engine import TemplateEngine
import os

MARATHON_POST_EVENT = 'api_post_event'
LOGS_ROOT_DIR = '/mnt/logs/docker/'

@register_plugin
class RsyslogLogentriesPlugin(object):
    """Plugin for forwarding logs to logentries using rsyslog forward """

    def __init__(self):
        self.template_engine = TemplateEngine()
        self.plugin_name = "RsyslogLogentriesPlugin"
        self.event_to_attach = MARATHON_POST_EVENT
        self.last_fetched_apps = []

    def apps_changed(self, new_fecthed_apps):
        # if number of monitored apps changed, app has changed.
        if len(self.last_fetched_apps) != len(new_fecthed_apps):
            return True

        set_apps_1 = set()
        for app in self.last_fetched_apps:
            appid = app.appid
            set_apps_1.add((appid, tuple(app.labels.items())))

        set_apps_2 = set()
        for app in new_fecthed_apps:
            appid = app.appid
            set_apps_2.add((appid, tuple(app.labels.items())))

        self.last_fetched_apps = new_fecthed_apps
        return set_apps_2 != set_apps_1

    def action(self, apps):
        logentries_apps = [app for app in apps if 'logentries-test' in app.labels]
        apps_with_logs = []
        for app in logentries_apps:
            app_logs_dir = os.path.join(LOGS_ROOT_DIR, app.image)

            if os.path.isdir(app_logs_dir):
                apps_with_logs.append(app)

        if apps_with_logs:
            self.template_engine.reload_rsyslog_template(apps_with_logs)

    def get_event_to_attach(self):
        return self.event_to_attach
