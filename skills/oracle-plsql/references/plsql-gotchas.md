# PL/SQL and SQL gotchas

| Error or symptom | Cause | Fix |
|---|---|---|
| PLS-00231 function may not be used in SQL | The function is private to the package body | Declare it in the package specification |
| PLS-00204 EXISTS/DECODE only in SQL | Used inside a PL/SQL expression | `select count(*) into ...` or `case` |
| ORA-54017 update of virtual column | Tried to set a computed column | Update the source columns |
| ORA-40556 chained JSON_TABLE | A second JSON_TABLE reads the first one's output | Stage the JSON in a work table |
| ORA-06502 on a long string | Concatenation passed the VARCHAR2 limit | Build in a CLOB with `dbms_lob.writeappend` |
| ORA-22998 LENGTHB on CLOB | LENGTHB does not take a CLOB | `dbms_lob.getlength` or pass VARCHAR2 |
| ORA-00001 inside a MERGE | The same new key appears twice in the source | De-duplicate the source before the merge |
| ORA-12899 value too large | Column too small for real data | Widen the column (a bigger `varchar2` or a CLOB), not the data |
| ORA-24247 network access denied | Missing ACL for UTL_HTTP | Grant the host ACE to the schema |
| A view still lacks a new column | The view was created with `select t.*` | Recreate the view |
| SQLcl runs part of a script | A blank line ends the statement; `&` starts substitution | Remove blank lines inside statements; `set define off` |
| Reserved word as a column | `number`, `date`, `level`, ... | Rename the column |
| Test data stays after rollback | A routine inside commits | Clean up explicitly |
| Oracle Cloud cannot reach a government API | The API only allows listed IP addresses | Fetch from an allowed machine and load the files |
