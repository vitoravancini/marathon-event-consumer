import os

plugins = [f[0:-3] for f in os.listdir('./pluginsDir/') if f.endswith('py') and f != "__init__.py"]

__all__ = plugins
