import argparse
import logging
import logging.config
from modules.connect import connect
from modules.load_config import load_config
from modules.parse_object import parse_object
from modules.sql_server import db_name, use, ddl


logger = logging.getLogger("sqlci")
logging.config.dictConfig(load_config("sqlci.logger.yaml"))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="The tool to sync and test part of database SQL Server",
        epilog="GitHub: https://github.com/wojciechbojewski/sqlci",
    )
    parser.add_argument("config_file", help="yaml file, see examples folder")
    # args = parser.parse_args()
    args = parser.parse_args(["./examples/sync_procedure.yaml"])
    # args = parser.parse_args(["-h"])

    config = load_config(args.config_file)
    logger.debug(f"read config: {config}")
    prod = connect(config["source"])
    dev = connect(config["target"])
    if prod and dev:
        logger.info("Processing objects")
        if "objects" in config:
            for object in config["objects"]:
                logger.info(f"Processing {object}")
                parsed_object = parse_object(object, config)
                with prod.cursor() as curr:
                    result = ddl(curr, parsed_object)
                    logger.debug(result)
        else:
            logger.warning("No objects to process")
    else:
        print("See log. exit(1)")
        exit(1)

    print("...done...")
    exit(0)
