import os
from config.config import get_config
config_app = get_config()
_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../..'))
_VAR = os.path.join(_ROOT, 'var')
_ETC = os.path.join(_ROOT, 'etc')
loglevel = config_app["logger"]["log_level"]
bind = config_app["app"]["bind"]
workers = config_app["app"]["worker"]
timeout = config_app["app"]["request_timeout"]
keyfile = os.path.join(os.path.dirname(__file__), "certs/selfsigned.key")
certfile = os.path.join(os.path.dirname(__file__), "certs/selfsigned.crt")
keepalive = 24 * 60 * 60
capture_output = True
