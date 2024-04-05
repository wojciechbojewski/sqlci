import re
import logging

logger = logging.getLogger("sqlci.modules.parse_object")


def parse(part: str) -> str:
    try:
        _output = part
        if " " in _output and "[" != _output[0] and "]" != _output[-1]:
            raise ValueError("Invalid part of object: {part}")
        if "[" == _output[0]:
            _output = _output[1:]
        if "]" == _output[-1]:
            _output = _output[:-1]
        return _output
    except ValueError as ex:
        logger.exception(ex)
        logger.info(
            f"Value with space in name should be in square brackets [some name]"
        )
        return None


def parse_object(o: str, config=None):
    logger.info(f"args: {o}")
    _output = dict(database=None, schema=None, object=None)
    _tmp = o
    _tmp = _tmp.split(".")
    _database = "master"
    if "source" in config and "database" in config["source"]:
        _database = config["source"]["database"]

    match _tmp:
        case (database, schema, object):
            _output["database"] = parse(database)
            _output["schema"] = parse(schema)
            _output["object"] = parse(object)
            logger.info(f"return: {_output}")
            return _output
        case (schema, object):
            _output["database"] = _database
            _output["schema"] = parse(schema)
            _output["object"] = parse(object)
            logger.info(f"return: {_output}")
            return _output
        case _:
            _output["database"] = _database
            _output["schema"] = "dbo"
            _output["object"] = parse(object)

    logger.info(f"return: {_output}")
    return _output
