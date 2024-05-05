class sqlbuilder:

    def from_list(self, list: list[str]):
        return "".join(list)

    class generate_database:
        def __init__(self, database):
            self._name = database

        def build(self):
            return f"CREATE DATABASE [{self._name}]\nGO"

    class generate_schema:
        def __init__(self, schema):
            self._name = schema

        def build(self):
            return f"CREATE SCHEMA [{self._name}]\nGO"

    class generate_table:
        def __init__(self, name):
            self._name = name
            self._columns = {}
            self._constraint = []
            self._indexies = []

        def addColumn(self, column: dict):
            match column:
                case {"Column_name": name, **kwarg}:
                    self._columns[name] = kwarg
            return self

        def addIdentity(self, identity: dict):
            Column_name = identity["Identity"]
            self._columns[Column_name]["Identity"] = f"IDENTITY({identity["Seed"]},{identity["Increment"]})"
            return self

        def addIndex(self, index: dict):
            match index:
                case {
                    "index_name": name,
                    "index_description": description,
                    "index_keys": keys,
                }:
                    if "clustered, unique, primary key" in description:
                        keys = keys.replace("(-)", " DESC")
                        alter = f"ALTER TABLE {self._name} ADD CONSTRAINT {name} PRIMARY KEY CLUSTERED ({keys})"
                        self._indexies.append(f"{alter}")
                    else:
                        print(f"Ignore index: {index}")
                        #raise NotImplementedError()
            return self

        def addConstraint(self, constraint: dict):
            match constraint:
                case {
                    "constraint_type": type,
                    "constraint_name": name,
                    "constraint_keys": keys,
                }:
                    if "DEFAULT on column" in type:
                        column = type.replace("DEFAULT on column ", "")
                        alter = f"ALTER TABLE {self._name} ADD DEFAULT {keys} FOR [{column}]"
                        self._constraint.append(alter)
                    if "CHECK on column" in type:
                        column = type.replace("CHECK on column ", "")
                        alter = (
                            f"ALTER TABLE {self._name} WITH CHECK ADD CHECK ({keys})"
                        )
                        self._constraint.append(alter)
            return self

        def build(
            self,
            drop=True,
            ignore_default=False,
            ignore_identity=False,
            ignore_check=False,
            ignore_index=False,
        ):
            sql = f"CREATE TABLE {self._name}\n("
            for column in self._columns:
                _type = self._columns[column]["Type"]
                sql = f"{sql}\n    [{column}] {_type}"
                _nullable = self._columns[column]["Nullable"]
                _nullable = "NULL" if _nullable == "yes" else "NOT NULL"
                if not ignore_identity:
                    if "Identity" in self._columns[column]:
                        _increment = self._columns[column]["Identity"]
                        sql = f"{sql} {_increment}"
                sql = f"{sql} {_nullable},"
            sql = sql[:-1]  # remove last comma
            sql = f"{sql}\n)\nGO"

            for constraint in self._constraint:
                if not ignore_check and "CHECK" in constraint:
                    sql = f"{sql}\n{constraint}\nGO"
                if not ignore_default and "DEFAULT" in constraint:
                    sql = f"{sql}\n{constraint}\nGO"

            if not ignore_index:
                for index in self._indexies:
                    sql = f"{sql}\n{index}\nGO"

            if drop:
                sql = f"DROP TABLE IF EXISTS {self._name}\n{sql}"

            return sql
