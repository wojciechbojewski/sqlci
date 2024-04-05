use master
go

if not exists(select name from sys.databases where name = 'sqlci') 
begin
	create database sqlci
end
go

use sqlci
go

create schema sqlci
go

drop table if exists sqlci.Table_Example
create table sqlci.Table_Example
(
	id int identity(1,1) primary key,
	dt datetime default GETDATE(),
	gd uniqueidentifier default NEWID(),
	nm numeric(10,2) null,
	description nvarchar(100) not null
)
insert into sqlci.Table_Example (description) values ('Example')
go

drop view if exists sqlci.View_Example
go

create view sqlci.View_Example
as
	select id, description from sqlci.Table_Example
go

create or alter procedure sqlci.Procedure_Example
as
	PRINT 'Print example'
	RAISERROR('RAISEERROR example',10,0)
	select * from sqlci.View_Example
go

exec sqlci.Procedure_Example

-- EXEC sp_help 'sqlci.Table_Example'
-- EXEC sp_help 'sqlci.View_Example'
-- EXEC sp_help 'sqlci.Procedure_Example'
