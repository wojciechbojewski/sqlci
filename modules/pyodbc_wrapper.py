import pyodbc


class SQLConnectionStringBuilder:
    def __init__(self, config: dict):
        self._config = config

    def build(self):
        connection_string = ""
        if "dsn" in self._config:
            connection_string = f"DSN={self._config['dsn']}"
            return connection_string

        if (
            "driver" in self._config
            and "server" in self._config
            and "database" in self._config
            and "trusted" in self._config
            and "encrypt" in self._config
        ):
            connection_string = (
                f"DRIVER={self._config['driver']};SERVER={self._config['server']}"
            )
            connection_string = (
                f"{connection_string};DATABASE={self._config['database']}"
            )

            connection_string = (
                f"{connection_string};Trusted_Connection={self._config['trusted']}"
            )

            connection_string = f"{connection_string};Encrypt={self._config['encrypt']}"
        else:
            raise AttributeError("Check you connection string")

        return connection_string


class SQLServer:

    def use(self, conn, database: str):
        curr = conn.cursor()
        result = True
        try:
            result = curr.execute(f"use [{database}]")
        except pyodbc.OperationalError as e:
            if e.args[0] == "08004":  # Database doesnt exists
                result = False
        finally:
            curr.close()
        return result

    # def sp_help(self, conn, name: str):
    #     curr = conn.cursor()
    #     curr.execute(f"exec sp_help '{name}'")
    #     output = {}
    #     try:
    #         work = True
    #         while work:
    #             if curr.messages:
    #                 # raise error or print
    #                 pass
    #             if curr.description:
    #                 # data row set
    #                 pass
    #         work = curr.nextset()
    #     finally:
    #         curr.close()
    #     return output

    def _removeSquareBrackets(self, val: str):

        if " " in val and (val[0] != "[" or val[-1] != "]"):
            raise AttributeError()

        output = val
        if output[0] == "[":
            output = output[1:]
        if output[-1] == "]":
            output = output[:-1]
        return output
