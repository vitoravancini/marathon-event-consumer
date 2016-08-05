from jinja2 import Environment, PackageLoader
import os


class TemplateEngine(object):
    """Render templates configured in templates folder"""
    def __init__(self):
        env = Environment(loader=PackageLoader('template', 'templates'))
        self.template = env.get_template('rsyslog.conf')

    def reload_rsyslog_template(self, apps):
        f = open('/etc/rsyslog.d/49-logentries-apps.conf', 'w+')
        f.write(self.template.render(apps=apps))
        f.close()

        os.system("sudo service rsyslog restart")
