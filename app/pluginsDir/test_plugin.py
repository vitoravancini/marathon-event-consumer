from marathon_rsyslog_forward import plugin_decorator
from template.template_engine import TemplateEngine


@plugin_decorator
class RsyslogLogentriesPlugin(object):
    """Plugin for forwarding logs to logentries using rsyslog forward """

    def __init__(self):
        self.template_engine = TemplateEngine()
        self.plugin_name = "PrimeiroPlugin"

    def init(self, apps):
        print("TESTINIT")
        self.template_engine.reload_rsyslog_template(apps)

    def action(self):
        print "{} acting!".format(self.pluginName)

    def apps_changed(self, last_fetched_apps, new_fecthed_apps):
        # if number of monitored apps changed return false.
        if len(last_fetched_apps) != len(new_fecthed_apps):
            return False

        set_apps_1 = set()
        for app in last_fetched_apps:
            appid = app.appid
            set_apps_1.add((appid, tuple(app.labels.items())))

        set_apps_2 = set()
        for app in new_fecthed_apps:
            appid = app.appid
            set_apps_2.add((appid, tuple(app.labels.items())))

        return set_apps_2 != set_apps_1

    def action(self, apps):
        self.template_engine.reload_rsyslog_template(apps)
