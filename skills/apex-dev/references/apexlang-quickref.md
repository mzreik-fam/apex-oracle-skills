# APEXlang quick reference (verified on APEX 26.1)

Patterns that validated and imported. Property names and valid values come from the compiler; when unsure, validate and read the error, which lists the valid values.

Layout of a source folder (one `.apx` file per page plus shared components):
```
<app>/application.apx
<app>/pages/p00004-locations.apx
<app>/shared-components/{lists,lovs,static-files,...}.apx
```
`@name` references another component by its id (a region, a column, an LOV). Page item names in conditions are plain text (see gotchas).

## Page, region, item

```
page 4 (
    name: Locations
    alias: LOCATIONS
    title: Locations
    appearance { pageTemplate: @/left-side-column  templateOptions: #DEFAULT# }
    security { pageAccessProtection: unrestricted  formAutoComplete: false }

    pageItem P4_FILTER ( type: hidden  layout { sequence: 5  region: @head  slot: regionBody } )

    region head (
        name: Heading
        type: dynamicContent
        source { language: plsql  plsqlFunctionBody: ```plsql
            return '<h1>Locations</h1>';
        ``` }
        layout { sequence: 10  slot: body }
        appearance { template: @/blank-with-attributes  templateOptions: #DEFAULT# }
    )
)
```
Write nested blocks on separate lines in real files; a `column X ( a b c )` on one line is a syntax error.

A modal dialog page: `appearance { dialogTemplate: @/modal-dialog  pageMode: modalDialog }`, regions use `slot: contentBody`. Open it from SQL or PL/SQL with `apex_page.get_url(p_page => 10, p_items => 'P10_ID', p_values => id)`.

Show a region only in one state:
```
serverSideCondition { type: item=value  item: P7_VIEW  value: REPORT }
```
(`item!=value` for the opposite.) The item name has no `@`.

## Interactive grid (editable)

```
region grid (
    name: Locations
    type: interactiveGrid
    source { location: localDatabase  type: sqlQuery  sqlQuery: ```sql
        select location_id, name_en from locations
    ``` }
    layout { sequence: 20  slot: body }
    appearance { template: @/blank-with-attributes  templateOptions: #DEFAULT# }
    toolbar {
        show: true
        controls: [
            searchCol
            searchField
            actionsMenu
            resetButton
            saveButton
        ]
    }
    edit {
        enabled: true
        allowedOperations: [
            add
            update
            delete
        ]
    }
    column LOCATION_ID (
        type: displayOnly
        heading { heading: ID }
        layout { sequence: 10 }
        source { databaseColumn: LOCATION_ID  dataType: number  primaryKey: true }
    )
    column NAME_EN (
        type: textField
        heading { heading: Name }
        layout { sequence: 20 }
        source { databaseColumn: NAME_EN  dataType: varchar2 }
    )
    savedReport primary (
        name: Primary
        identification { visibility: primary }
        view { default: grid  rowsPerPage: 50 }
        displayColumn ( identification { column: @NAME_EN }  layout { show: true  sequence: 20 } )
    )
)
process save-grid (
    name: Save grid
    type: executeCode
    editableRegion: @grid
    source { language: plsql  plsqlCode: ```plsql
        begin
            case :APEX$ROW_STATUS
                when 'U' then my_pkg.save_row(:LOCATION_ID, :NAME_EN);
                when 'C' then my_pkg.add_row(:NAME_EN);
                when 'D' then my_pkg.remove_row(:LOCATION_ID);
            end case;
        end;
    ``` }
    execution { sequence: 10 }
)
```
- Column `dataType` is lowercase for grids (`number`, `varchar2`, `date`, `timestamp`).
- A grid lists its columns explicitly. A new column in the query is not shown until you add it here and in `displayColumn`.
- `toolbar`, `edit` and `actionsMenu` are groups written directly inside the region. Do not wrap them in an `attributes ( ... )` child (it creates a second grid and the import fails with ORA-00001 on IG_PK).
- The grid needs one `primaryKey: true` column, which can be the row id.

## Interactive report

```
region report (
    name: DLD property report
    type: interactiveReport
    source { location: localDatabase  type: sqlQuery  sqlQuery: select * from v_my_report }
    layout { sequence: 21  slot: body }
    appearance { template: @/blank-with-attributes  templateOptions: #DEFAULT# }
    actionsMenu {
        includeActionsMenu: true
        selectColumns: true  filter: true  rowsPerPage: true  sort: true  controlBreak: true
        highlight: true  compute: true  aggregate: true  chart: true
        groupBy: true  pivot: true  flashback: true  reset: true  download: true  help: true
        saveReport: true  savePublicReport: true
    }
    column NAME_EN (
        identification { type: plainText }
        source { dataType: STRING }
        heading { heading: Name }
        layout { sequence: 20 }
    )
)
```
- Report column `dataType` is uppercase (`STRING`, `NUMBER`, `DATE`, `TIMESTAMP`).
- Group By and Pivot appear in the Actions menu only if `groupBy` and `pivot` are on.
- Every column needs `type: plainText`, `source dataType` and a `heading`.
- Give each column a unique `advanced { endUserAlias: XX }` if the validator reports a duplicate (exports can contain duplicates after a column is added in the browser).
- Pagination: `pagination { type: rowRangesXToYOfZ  displayPosition: topAndBottomLeft }`.

## Column types and options (grid)

`hidden`, `displayOnly`, `textField`, `numberField`, `selectList`, `popupLov`, `link`, `checkbox`, `datePicker`, `textarea`, `htmlExpression`, `switch`, ...

List of values on a column (the LOV is a shared component):
```
lov { type: sharedComponent  lov: @parent-locations }
```
Link column that opens a URL (for example a modal dialog URL built in the SQL):
```
column NAME_EN ( type: link  link { linkText: #NAME_EN#  target: { type: url  url: #UNITS_URL# } } ... )
```
A `link` column cannot have a `readOnly` group.

Read-only by condition on an editable column:
```
readOnly { type: expression  language: plsql  plsqlExpression: nvl(:ORIGIN, 'CUSTOM') <> 'CUSTOM' }
```

## Shared LOV (`shared-components/lovs.apx`)

```
lov parent-locations (
    name: PARENT_LOCATIONS
    source { location: localDatabase  type: sqlQuery  sqlQuery: ```sql
        select full_path as label, location_id from locations order by full_path
    ``` }
    columnMapping { return: LOCATION_ID  display: LABEL }
)
lov yes-no (
    name: YES_NO
    source { location: staticValues }
    entry yes ( sequence: 1  display: Yes  return: Y )
    entry no  ( sequence: 2  display: No   return: N )
)
```
Use `popupLov` (searchable) for lists of more than about 15 values, `selectList` for short ones.

## Page CSS

```
css { inline: ```css
    .a-IRR-container th, .a-IRR-container td { border-right: 1px solid rgba(0,0,0,0.06) !important; }
``` }
```
Regions do not take a `staticId` in this format; style through APEX's own classes such as `.a-IRR-container`.

## Verify what was stored

```sql
select region_name, source_type_code, condition_type, condition_expression1, condition_expression2
  from apex_application_page_regions where application_id = :app and page_id = :page order by display_sequence;
select process_name, process_type_code from apex_application_page_proc where application_id = :app and page_id = :page;
```
