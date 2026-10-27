#!/bin/sh
# Safe APEXlang deploy: export the live app, validate your source, import.
# Settings (environment variables):
#   SQLCL_CONN   saved SQLcl connection name           (required)
#   APEX_WS      APEX workspace name                    (required)
#   APEX_APP_ID  application id                         (required)
#   APEX_APP_NAME  application NAME for the import      (required; NOT the connection name)
#   APEX_SRC     folder with the APEXlang source        (default: ./apex-src)
#   SQLCL        path to the sql binary                 (default: sql)
set -e
: "${SQLCL_CONN:?set SQLCL_CONN}" "${APEX_WS:?set APEX_WS}" "${APEX_APP_ID:?set APEX_APP_ID}" "${APEX_APP_NAME:?set APEX_APP_NAME}"
SRC="${APEX_SRC:-./apex-src}"; SQL="${SQLCL:-sql}"
BACKUP="backups/live-$(date +%Y%m%d-%H%M%S)"
echo "1/3 exporting the live app to $BACKUP"
printf "apex export -applicationid %s -exptype APEXLANG -dir %s\nexit\n" "$APEX_APP_ID" "$BACKUP" | "$SQL" -S -name "$SQLCL_CONN" | grep -E "created|rror" | tail -2
echo "    Compare $BACKUP with $SRC now. Anything that differs may be somebody's browser edit: merge it before importing."
printf "Continue with validate and import? [y/N] "; read -r ans; [ "$ans" = "y" ] || { echo "stopped"; exit 1; }
echo "2/3 validating"
printf "set autocommit off\napex validate -input %s -workspace %s\nexit\n" "$SRC" "$APEX_WS" | "$SQL" -S -name "$SQLCL_CONN" | grep -v -E "JLine|^\s*$" | tail -15
echo "3/3 importing as application name: $APEX_APP_NAME"
printf "set autocommit off\napex import -input %s -workspace %s -name %s\nexit\n" "$SRC" "$APEX_WS" "$APEX_APP_NAME" | "$SQL" -S -name "$SQLCL_CONN" | grep -v -E "JLine|^\s*$" | tail -6
echo "Done. Verify against apex_application_page_regions, and tell users their private saved reports were reset."
