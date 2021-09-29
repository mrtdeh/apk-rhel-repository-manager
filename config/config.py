import os
import yaml

dir_path = os.path.dirname(os.path.abspath(__file__))
dir_path = "/etc/apk_reprepro/"
config_path = os.path.join(dir_path, "config.yml")
config_app = yaml.safe_load(open(config_path, "r"))


def set_config(config):
    config_to_save = yaml.safe_dump(config)
    with open(config_path, "w") as file:
        file.write(config_to_save)


def get_config():
    return config_app
