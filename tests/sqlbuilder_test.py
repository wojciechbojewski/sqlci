import unittest
from modules import sqlbuilder


class sqlbuilder_generate_database(unittest.TestCase):
    def test_generate_database(self):
        self.maxDiff = None
        builder = sqlbuilder.sqlbuilder()
        database = builder.generate_database("database")
        self.assertEqual("CREATE DATABASE [database]\nGO", database.build())


class sqlbuilder_generate_schema(unittest.TestCase):
    def test_generate_schema(self):
        self.maxDiff = None
        builder = sqlbuilder.sqlbuilder()
        schema = builder.generate_schema("sqlci")
        self.assertEqual("CREATE SCHEMA [sqlci]\nGO", schema.build())


class sqlbuilder_from_list(unittest.TestCase):
    def test_generate_from_list(self):
        self.maxDiff = None
        builder = sqlbuilder.sqlbuilder()
        text = [
            "line1\n",
            "line2\n",
            "line3\n",
        ]
        self.assertEqual("".join(text), builder.from_list(text))


class sqlbuilder_generate_table(unittest.TestCase):
    def test_generate_table(self):
        self.maxDiff = None
        builder = sqlbuilder.sqlbuilder()
        table = builder.generate_table("[sqlci].[Table_Example]")
        table = table.addColumn({"Column_name": "id", "Type": "int", "Nullable": "no"})
        expected = """CREATE TABLE [sqlci].[Table_Example]
(
    [id] int NOT NULL
)
GO"""
        self.assertEqual(expected, table.build(drop=False))

    def test_generate_table_with_identity(self):
        self.maxDiff = None
        builder = sqlbuilder.sqlbuilder()
        table = builder.generate_table("[sqlci].[Table_Example]")
        table = table.addColumn({"Column_name": "id", "Type": "int", "Nullable": "no"})
        table = table.addIdentity({"Identity": "id", "Seed": 1, "Increment": 1})
        expected = """CREATE TABLE [sqlci].[Table_Example]
(
    [id] int IDENTITY(1,1) NOT NULL
)
GO"""
        self.assertEqual(table.build(drop=False), expected)

    def test_generate_table_defalut_constraint(self):
        self.maxDiff = None
        builder = sqlbuilder.sqlbuilder()
        table = builder.generate_table("[sqlci].[Table_Example]")
        table = table.addColumn({"Column_name": "id", "Type": "int", "Nullable": "no"})
        table = table.addConstraint(
            {
                "constraint_type": "DEFAULT on column datetime",
                "constraint_name": "DF__Table_Exa__datet__123EB7A3",
                "constraint_keys": "(getdate())",
            }
        )
        expected = """CREATE TABLE [sqlci].[Table_Example]
(
    [id] int NOT NULL
)
GO
ALTER TABLE [sqlci].[Table_Example] ADD DEFAULT (getdate()) FOR [datetime]
GO"""
        self.assertEqual(table.build(drop=False), expected)

    def test_generate_table_index_primary_clustered_key(self):
        self.maxDiff = None
        builder = sqlbuilder.sqlbuilder()
        table = builder.generate_table("[sqlci].[Table_Example]")
        table = table.addColumn({"Column_name": "id", "Type": "int", "Nullable": "no"})
        table = table.addColumn(
            {"Column_name": "dt", "Type": "datetime", "Nullable": "no"}
        )
        table = table.addIndex(
            {
                "index_name": "PK__Table_Ex__2ECD2125E0955DAA",
                "index_description": "clustered, unique, primary key located on PRIMARY",
                "index_keys": "id(-), dt",
            }
        )
        expected = """CREATE TABLE [sqlci].[Table_Example]
(
    [id] int NOT NULL,
    [dt] datetime NOT NULL
)
GO
ALTER TABLE [sqlci].[Table_Example] ADD CONSTRAINT PK__Table_Ex__2ECD2125E0955DAA PRIMARY KEY CLUSTERED (id DESC, dt)
GO"""
        self.assertEqual(table.build(drop=False), expected)


# ["index_name","index_description","index_keys"]
# PK__Table_Ex__2ECD2125E0955DAA	clustered, unique, primary key located on PRIMARY	id(-), dt
