

DROP TABLE IF EXISTS [sqlci].[Table_Example]
CREATE TABLE [sqlci].[Table_Example]
(
    [id] int IDENTITY(1,1) NOT NULL,
    [dt] datetime NOT NULL,
    [gd] uniqueidentifier NULL,
    [nm] numeric(10,2) NULL,
    [description] nvarchar(800) NOT NULL
)
GO
ALTER TABLE [sqlci].[Table_Example] ADD CONSTRAINT PK__Table_Ex__2ECD212538CF6BDE PRIMARY KEY CLUSTERED (id DESC, dt)
GO

DROP TABLE IF EXISTS [sqlci].[Table_Example2]
CREATE TABLE [sqlci].[Table_Example2]
(
    [id] int IDENTITY(1,1) NOT NULL,
    [dt] datetime NOT NULL,
    [gd] uniqueidentifier NULL,
    [nm] numeric(10,2) NULL,
    [description] nvarchar(800) NOT NULL
)
GO
ALTER TABLE [sqlci].[Table_Example2] ADD CONSTRAINT PK__Table_Ex__2ECD212549300FCD PRIMARY KEY CLUSTERED (id DESC, dt)
GO