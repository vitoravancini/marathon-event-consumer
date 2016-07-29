from jinja2 import Environment, PackageLoader


class TemplateEngine(object):
    """Render templates configured in templates folder"""
    def __init__(self):
        env = Environment(loader=PackageLoader('template', 'templates'))
        self.template = env.get_template('rsyslog.conf')

    def reload_rsyslog_template(self, apps):
        print self.template.render(apps=apps)
