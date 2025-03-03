import yaml


def get_config():
    with open("config.d/config.yml", "r") as file:
        config = yaml.safe_load(file)
    return config
