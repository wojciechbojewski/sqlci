import unittest
import pyodbc
from modules.sqlserver import sqlserver


class sqlserver_sp_help(unittest.TestCase):
    def test_sp_help_empty_arguments_throw_exception(self):
        sql = sqlserver()
        self.assertRaises(NotImplementedError, sql.sp_help, (None,))

    def test_sp_help_non_table_argument_throw_exception(self):
        conn = pyodbc.connect("DSN=PROD")
        sql = sqlserver()
        with self.assertRaises(NotImplementedError) as context:
            sql.sp_help(conn, "[sqlci].[Procedure_Example]")

    def test_sp_help_table_return_data(self):
        conn = pyodbc.connect("DSN=PROD")
        conn.execute(
            """DROP TABLE IF EXISTS [sqlci].[Table_Example]
CREATE TABLE [sqlci].[Table_Example] (
	[id] [int] NULL,
	[datetime] [datetime] NULL,
	[guid] [uniqueidentifier] NULL,
	[number] [numeric](10, 2) NULL,
	[description] [nvarchar](100) NOT NULL,
)"""
        )
        sql = sqlserver()
        result = sql.sp_help(conn, "[sqlci].[Table_Example]")
        expected = {
            "columns": [
                {"Column_name": "id", "Type": "int", "Nullable": "yes"},
                {"Column_name": "datetime", "Type": "datetime", "Nullable": "yes"},
                {"Column_name": "guid", "Type": "uniqueidentifier", "Nullable": "yes"},
                {"Column_name": "number", "Type": "numeric(10,2)", "Nullable": "yes"},
                {
                    "Column_name": "description",
                    "Type": "nvarchar(200)",
                    "Nullable": "no",
                },
            ]
        }
        self.assertDictEqual(result, expected)

    def test_sp_help_table_return_data_with_identity(self):
        self.maxDiff = None
        conn = pyodbc.connect("DSN=PROD")
        conn.execute(
            """DROP TABLE IF EXISTS [sqlci].[Table_Example]
CREATE TABLE [sqlci].[Table_Example] (
	[id] [int] IDENTITY(1,1) NOT NULL
)"""
        )
        sql = sqlserver()
        result = sql.sp_help(conn, "[sqlci].[Table_Example]")
        expected = {
            "columns": [
                {
                    "Column_name": "id",
                    "Type": "int",
                    "Nullable": "no",
                }
            ],
            "identity": {"Identity": "id", "Seed": 1, "Increment": 1},
        }
        self.assertDictEqual(result, expected, result)
