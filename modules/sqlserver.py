import pyodbc


class sqlserver:

    def use(self, conn, database):
        curr = conn.cursor()
        curr.execute(f"USE {database}")
        curr.close()

    def sp_helptext(self, conn, object=None):
        if object == None:
            raise NotImplementedError()
        text = []
        curr = conn.cursor()
        curr.execute(f"EXEC sp_helptext '{object}'")
        work = True
        while work:
            if curr.messages:
                raise TypeError("curr.messages")
            if curr.description:
                rows = map(lambda x: str(x[0]).replace("\r\n", "\n"), curr.fetchall())
                rows = filter(lambda x: x != "\n", rows)
                rows = list(rows)
                rows.append("GO\n")
                return rows
            work = curr.nextset()
        curr.close()
        return text

    def sp_help(self, conn, table=None):
        if table == None:
            raise NotImplementedError()
        resultset = {}
        curr = conn.cursor()
        curr.execute(f"EXEC sp_help '{table}'")
        work = True
        while work:
            if curr.messages:
                pass
            if curr.description:
                columns = [column[0] for column in curr.description]
                match columns:
                    case ["index_name", "index_description", "index_keys"]:
                        resultset["indexies"] = []
                        for index in curr.fetchall():
                            _tmp = {
                                "index_name": index.index_name,
                                "index_description": index.index_description,
                                "index_keys": index.index_keys,
                            }
                            resultset["indexies"].append(_tmp)

                    case [
                        "constraint_type",
                        "constraint_name",
                        "delete_action",
                        "update_action",
                        "status_enabled",
                        "status_for_replication",
                        "constraint_keys",
                    ]:
                        resultset["constraints"] = []
                        for constraint in curr.fetchall():
                            _tmp = {
                                "constraint_type": constraint.constraint_type,
                                "constraint_name": constraint.constraint_name,
                                "constraint_keys": constraint.constraint_keys,
                            }
                            resultset["constraints"].append(_tmp)

                    case ["Identity", "Seed", "Increment", "Not For Replication"]:
                        row = curr.fetchone()
                        if row.Identity != "No identity column defined.":
                            resultset["identity"] = {
                                "Identity": row.Identity,
                                "Seed": int(row.Seed),
                                "Increment": int(row.Increment),
                            }

                    case ["Name", "Owner", "Type", "Created_datetime"]:
                        row = curr.fetchone()
                        if row.Type == "stored procedure":
                            raise NotImplementedError()
                    case [
                        "Column_name",
                        "Type",
                        "Computed",
                        "Length",
                        "Prec",
                        "Scale",
                        "Nullable",
                        "TrimTrailingBlanks",
                        "FixedLenNullInSource",
                        "Collation",
                    ]:
                        resultset["columns"] = []
                        for row in curr.fetchall():
                            _tmp = {
                                "Column_name": row.Column_name,
                            }
                            match row.Type:
                                case (
                                    "int"
                                    | "tinyint"
                                    | "smallint"
                                    | "datetime"
                                    | "uniqueidentifier"
                                    | "float"
                                    | "double"
                                    | "bit"
                                ):
                                    _tmp["Type"] = row.Type
                                case (
                                    "char"
                                    | "varchar"
                                    | "nchar"
                                    | "nvarchar"
                                    | "binary"
                                    | "varbinary"
                                ):
                                    _tmp["Type"] = f"{row.Type}({row.Length})"
                                case "numeric":
                                    _tmp["Type"] = (
                                        f"{row.Type}({str(row.Prec).strip()},{str(row.Scale).strip()})"
                                    )
                                case _:
                                    raise NotImplementedError(
                                        f"Not implemented type {row.Type}"
                                    )
                            _tmp["Nullable"] = row.Nullable
                            resultset["columns"].append(_tmp)

            work = curr.nextset()
        curr.close()
        return resultset
