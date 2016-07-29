from jinja2 import Environment, PackageLoader
import os

class TemplateEngine(object):
    """Render templates configured in templates folder"""
    def __init__(self):
        env = Environment(loader=PackageLoader('template', 'templates'))
        self.template = env.get_template('rsyslog.conf')

    def reload_rsyslog_template(self, apps):
        for app in apps:
            f = open('/etc/rsyslog.d/49-logentries-{}.conf'.format(app.appid), 'w+')
            f.write(self.template.render(app=app))
            f.close()
            os.system("sudo service rsyslog restart")
