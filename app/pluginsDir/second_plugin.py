from marathon_rsyslog_forward import plugin_decorator


@plugin_decorator
class SecondPlugin(object):
    """docstring for TestPlugin"""

    def __init__(self):
        self.pluginName = "SecondPlugin"

    def action(self):
        print "{} acting!".format(self.pluginName)
