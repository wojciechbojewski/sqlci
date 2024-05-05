import pyodbc
import yaml
from modules.sqlserver import sqlserver
from modules.sqlbuilder import sqlbuilder
import os
import sys


def load_config(args):

    match args:
        case [_, file_name]:
            with open(file_name) as file:
                config = yaml.safe_load(file)
                return config
        case _:
            print(
                """usage > sqlci.py(z) [CONFIG_FILE_NAME_YAML]
"""
            )
            os._exit(0)


def read_dns(config):
    return f"DSN={config['source']['dsn']}"


def read_types(config):
    return config["dump"]


def read_items(config, type):
    return config["dump"][type]


def unpack_object(item):
    return list(item.keys())[0].split(".")


def add_columns(table, result):
    for column in result["columns"]:
        table.addColumn(column)
    return table


def add_identity(table, result):
    if "identity" in result:
        table.addIdentity(result["identity"])
    return table


def add_constraints(table, result):
    if "constraints" in result:
        for constraint in result["constraints"]:
            table.addConstraint(constraint)
    return table


def add_indexies(table, result):
    if "indexies" in result:
        for index in result["indexies"]:
            table.addIndex(index)
    return table


if __name__ == "__main__":
    os.system("cls")

    args = sys.argv
    # args = ["sqlci.py", "config.yaml"]

    config = load_config(args)
    dsn = read_dns(config)
    types = read_types(config)

    with open("output.sql", "w") as file:
        conn = pyodbc.connect(dsn)
        sqlserver = sqlserver()
        builder = sqlbuilder()

        for type in types:
            if type == "tables":
                for item in read_items(config, type):
                    database, schema, table = unpack_object(item)
                    result = sqlserver.sp_help(conn, f"{schema}.{table}")
                    table = builder.generate_table(f"{schema}.{table}")
                    table = add_columns(table, result)
                    table = add_identity(table, result)
                    table = add_constraints(table, result)
                    table = add_indexies(table, result)
                    file.write("\n\n" + table.build())
            if type == "views" or type == "procedures":
                for item in read_items(config, type):
                    database, schema, object = unpack_object(item)
                    result = sqlserver.sp_helptext(conn, f"{schema}.{object}")
                    file.write("\n")
                    file.write("".join(result))
        conn.close()
