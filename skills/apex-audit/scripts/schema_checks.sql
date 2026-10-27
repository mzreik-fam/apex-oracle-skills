-- Schema checks for the current user. Run in SQLcl: @schema_checks.sql
set pagesize 200 linesize 200 feedback on
prompt === Tables without a primary key
select table_name from user_tables t
 where not exists (select 1 from user_constraints c where c.table_name = t.table_name and c.constraint_type = 'P') order by 1;

prompt === Editable-looking tables without audit columns (created_by / created_at)
select table_name from user_tables t
 where table_name not like 'SYS%' and table_name not like 'DR$%'
   and (select count(*) from user_tab_columns c where c.table_name = t.table_name and c.column_name in ('CREATED_BY','CREATED_AT')) < 2 order by 1;

prompt === Columns that look like UUIDs (RAW(16) or sys_guid defaults)
select table_name, column_name, data_type, data_length from user_tab_cols
 where (data_type = 'RAW' and data_length = 16) or upper(data_default_vc) like '%SYS_GUID%' order by 1, 2;

prompt === Foreign key columns without an index
select c.table_name, cc.column_name, c.constraint_name
  from user_constraints c join user_cons_columns cc on cc.constraint_name = c.constraint_name and cc.position = 1
 where c.constraint_type = 'R'
   and not exists (select 1 from user_ind_columns i where i.table_name = c.table_name and i.column_name = cc.column_name and i.column_position = 1) order by 1, 2;

prompt === Unnamed constraints (system names like SYS_C...)
select table_name, constraint_name, constraint_type from user_constraints
 where constraint_name like 'SYS\_C%' escape '\' and constraint_type in ('U','R','C') and generated = 'GENERATED NAME'
   and search_condition_vc not like '%IS NOT NULL' order by 1;

prompt === PL/SQL that swallows errors (when others then null)
select name, type, line, text from user_source
 where regexp_like(text, 'when\s+others\s+then\s+null', 'i') order by 1, 3;

prompt === PL/SQL with COMMIT inside routines that may be reused (review each)
select name, type, line from user_source where regexp_like(text, '^\s*commit\s*;', 'i') order by 1, 3;

prompt === PL/SQL with dbms_output left in
select name, type, line from user_source where regexp_like(text, 'dbms_output', 'i') and type in ('PACKAGE BODY','PROCEDURE','FUNCTION','TRIGGER') order by 1, 3;

prompt === Invalid objects
select object_name, object_type, status from user_objects where status <> 'VALID' order by 1;

prompt === Views that may have a frozen column list (created from select alias.*)
select view_name from user_views where regexp_like(text_vc, 'select\s+\w+\.\*', 'i') order by 1;
