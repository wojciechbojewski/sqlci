import yaml
import logging

logger = logging.getLogger("sqlci.modules.load_config")


def load_config(filename):
    try:
        with open(filename, "r") as file:
            return yaml.safe_load(file)
    except yaml.composer.ComposerError as e:
        logger.exception(e)
        print("See log. exit(1)")
        exit(1)
    except Exception as e:
        logger.exception(e)
        print("See log. exit(1)")
        exit(1)
