import pyodbc
import logging

logger = logging.getLogger("sqlci.modules.connect")


def connect(config):
    """
    Example of yaml config

    version: 1
    source:
        dsn: PROD
    target:
        driver: ODBC Driver 18 for SQL Server
        server: DESKTOP-F1E0DKV\SQL2022
        database: master
        trusted: "yes"
        encrypt: "no"
    """
    logger.debug(f"args: {config}")
    connection_string = ""
    try:
        if "driver" in config and "server" in config:
            connection_string = f"DRIVER={config['driver']};SERVER={config['server']}"
        if "dsn" in config:
            connection_string = f"DSN={config['dsn']}"
        if "database" in config:
            connection_string = f"{connection_string};DATABASE={config['database']}"
        if "trusted" in config:
            connection_string = (
                f"{connection_string};Trusted_Connection={config['trusted']}"
            )
        if "encrypt" in config:
            connection_string = f"{connection_string};Encrypt={config['encrypt']}"

        connection_string = f"{connection_string};APP=sqlci"

        logger.debug(f"connection_string: {connection_string}")
        return pyodbc.connect(connection_string)
    except pyodbc.InterfaceError as e:
        logger.exception(e)
        if e.args[0] == "IM002":
            logger.error("Data source name not found and no default driver specified")
            logger.info(f"dns: {pyodbc.dataSources()}")
            logger.info(f"drivers: {pyodbc.drivers()}")
        if e.args[0] == "28000":
            logger.error("Invalid authorization specification")
            logger.info("Do you have access to database, does database exists?")

        else:
            logger.error(type(e))
            logger.error(e)
    except Exception as e:
        logger.exception(e)
        logger.info(type(e))
