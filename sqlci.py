import pyodbc
from modules.sqlserver import sqlserver
from modules.sqlbuilder import sqlbuilder
import os

if __name__ == "__main__":
    os.system("cls")
    with open("output.sql", "w") as file:
        conn = pyodbc.connect(f"DSN=PROD")
        sqlserver = sqlserver()
        builder = sqlbuilder()
        for item in ["[sqlci].[Table_Example]", "[sqlci].[Table_Example2]"]:
            result = sqlserver.sp_help(conn, item)
            table = builder.generate_table(item)
            for column in result["columns"]:
                table.addColumn(column)
            if "identity" in result:
                table.addIdentity(result["identity"])
            if "constraints" in result:
                for constraint in result["constraints"]:
                    table.addConstraint(constraint)
            if "indexies" in result:
                for index in result["indexies"]:
                    table.addIndex(index)
            file.write("\n\n" + table.build())
        conn.close()
