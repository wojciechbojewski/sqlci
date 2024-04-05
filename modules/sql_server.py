import logging

logger = logging.getLogger("sqlci.modules.sql_server")


def sp_helptext(curr, name):
    _output = ""
    logger.debug(f"[sql] sp_helptext")
    result = curr.execute(f"exec sp_helptext '{name}'").fetchall()
    for line in result:
        _output = _output + line[0]
    return _output


def create_table(curr, name):
    _output = ""
    _columns = {}
    _clustered_index = ""
    _nonclustered_index = []
    _primary_key = ""
    logger.debug(f"[sql] sp_help")
    curr.execute(f"exec sp_help '{name}'")

    work = True
    while work:
        if curr.messages:
            logger.debug(curr.messages)
        if curr.description:
            logger.debug(curr.description)
            if "Column_name" in curr.description[0]:
                for row in curr.fetchall():
                    _columns[row[0]] = {}
                    match row[1]:  # Type
                        case "int" | "datetime" | "uniqueidentifier":
                            _columns[row[0]]["type"] = f"{row[1]}"
                        case "varchar" | "nvarchar":
                            _columns[row[0]]["type"] = f"{row[1]}({row[3]})"
                        case "numeric":
                            _columns[row[0]][
                                "type"
                            ] = f"{row[1]}({str(row[4]).strip()}, {str(row[5]).strip()})"

                    match row[6]:  # Nullable
                        case "yes":
                            _columns[row[0]]["nullable"] = f"NULL"
                        case "no":
                            _columns[row[0]]["nullable"] = f"NOT NULL"
            if "Identity" in curr.description[0]:
                for row in curr.fetchall():
                    _columns[row[0]]["identity"] = f"IDENTITY({row[1]},{row[2]})"
            if "index_name" in curr.description[0]:
                for row in curr.fetchall():
                    if "clustered, unique, primary key" in row[1]:
                        _clustered_index = (
                            f"CREATE CLUSTERED INDEX {row[0]} ON {name} ({row[2].replace("(-)"," DESC")})"
                        )
                    if "clustered, columnstore" in row[1]:
                        _clustered_index = (
                            f"CREATE CLUSTERED COLUMNSTORE INDEX {row[0]} ON {name}"
                        )
                    if "nonclustered located" in row[1]:
                        _nonclustered_index.append(f"CREATE NONCLUSTERED INDEX {row[0]} ON {name} ({row[2].replace("(-)"," DESC")})")
                    if "nonclustered, columnstore" in row[1]:
                        _nonclustered_index.append(f"CREATE NONCLUSTERED COLUMNSTORE INDEX {row[0]} ON {name}")


            if "constraint_type" in curr.description[0]:
                for row in curr.fetchall():
                    if "DEFAULT" in row[0]:
                        Column_name = row[0].replace("DEFAULT on column ", "")
                        _columns[Column_name]["default"] = f"DEFAULT {row[6]}"
                    if "PRIMARY KEY (clustered)" in row[0]:
                        _primary_key = f"PRIMARY KEY ( {row[6].replace("(-)"," DESC")} )"
                        _clustered_index = ""
                    else:
                        logger.info(curr.fetchall())
        work = curr.nextset()

    _output = f"CREATE TABLE {name}(\n"
    for column in _columns:
        _output = f"{_output}{column} {_columns[column]['type']}"
        if "identity" in _columns[column]:
            _output = f"{_output} {_columns[column]['identity']}"
        if "nullable" in _columns[column]:
            _output = f"{_output} {_columns[column]['nullable']}"
        if "default" in _columns[column]:
            _output = f"{_output} {_columns[column]['default']}"
        _output = f"{_output},\n"

    if _primary_key:
        _output = f"{_output}{_primary_key},\n"
    _output = f"{_output[:-2]}\n)"
    
    if _clustered_index:
        _output = f"{_output}\n{_clustered_index})"
    for nonclustered in _nonclustered_index:
        _output = f"{_output}\n{nonclustered})"

    # logger.info(_output)
    # logger.info(_columns)
    # logger.info(_clustered_index)
    # logger.info(_nonclustered_index)
    return _output


def db_name(curr):
    sql = f"select DB_NAME()"
    logger.info(f"[sql] {sql}")
    result = curr.execute(sql).fetchval()
    return result


def use(curr, database):
    sql = f"use {database}"
    logger.info(f"[sql] {sql}")
    result = curr.execute(sql)
    return True


def ddl(curr, o):
    database = o["database"]
    schema = o["schema"]
    object = o["object"]
    _output = ""

    if use(curr, database):
        result = curr.procedures(f"{object}", None, f"{schema}").fetchone()
        if result:  # and result.procedure_name == f"{object};1":
            sql = sp_helptext(curr, f"[{schema}].[{object}]")
            return dict(type="P", sql=sql)
        result = curr.tables(f"{object}", None, f"{schema}").fetchone()
        if result and result.table_type == "VIEW":
            sql = sp_helptext(curr, f"[{schema}].[{object}]")
            return dict(type="V", sql=sql)
        if result and result.table_type == "TABLE":
            sql = create_table(curr, f"[{schema}].[{object}]")
            return dict(type="T", sql=sql)
    return dict(type="T", sql=_output)
