"""
generate_table_scope.py
Reads iDM_MDM_tables_DDLs.xlsx and the CDM_DB/PIM_DB SQL files,
then writes references/07_mvp-schema-reference.md.
"""

import re
import sys
from collections import OrderedDict
import openpyxl

# ─── paths ────────────────────────────────────────────────────────────────────
EXCEL_PATH  = "resources/iDM_MDM_tables_DDLs.xlsx"
CDM_SQL     = "resources/CDM_DB.sql"
PIM_SQL     = "resources/PIM_DB.sql"
CUSTOM_SQL  = "resources/Core_DB_customized.sql"
OUTPUT_PATH = "references/07_mvp-schema-reference.md"

# ─── helpers ──────────────────────────────────────────────────────────────────

def normalize_name(name: str) -> str:
    """'PRODUCT TO GROUP' → 'PRODUCT_TO_GROUP'"""
    return name.strip().upper().replace(" ", "_")


def extract_col_type(col_name: str, ddl: str) -> str:
    """Return the Teradata data type for col_name from a CREATE TABLE DDL block."""
    if not ddl:
        return ""
    # Match:  [,whitespace] col_name   TYPE[(precision[,scale])]
    pat = (
        r'(?:^|[\n,])\s*'
        + re.escape(col_name)
        + r'\s+((?:NOT\s+)?[A-Z_]+(?:\s*\(\s*[\d,]+\s*\))?(?:\s*\(\s*\d+\s*\))?)'
    )
    m = re.search(pat, ddl, re.IGNORECASE | re.MULTILINE)
    if m:
        raw = m.group(1).strip()
        # strip trailing NULL / NOT NULL that leaked in
        raw = re.sub(r'\s+(NOT\s+)?NULL.*', '', raw, flags=re.IGNORECASE).strip()
        return raw
    return ""


def parse_sql_file(filepath: str):
    """
    Parse a .sql file containing one or more CREATE TABLE statements.
    Returns dict:  table_name (upper, no schema) → {
        'ddl': str,
        'schema': str,
        'columns': [ {'name', 'type', 'pk', 'nullable'} ]
    }
    """
    with open(filepath, encoding="utf-8") as f:
        text = f.read()

    tables = {}
    # Split on CREATE ... TABLE boundaries
    blocks = re.split(r'(?=CREATE\s+(?:MULTISET\s+)?TABLE\s)', text, flags=re.IGNORECASE)
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        m = re.match(
            r'CREATE\s+(?:MULTISET\s+)?TABLE\s+(\w+)\.(\w+)\s*\(', block, re.IGNORECASE
        )
        if not m:
            continue
        schema, tbl = m.group(1).upper(), m.group(2).upper()

        # Extract everything inside the outer parentheses
        paren_start = block.index('(')
        depth = 0
        body = ""
        for i, ch in enumerate(block[paren_start:]):
            if ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
                if depth == 0:
                    body = block[paren_start + 1: paren_start + i]
                    break

        # Find PRIMARY INDEX columns
        pk_cols = set()
        pi = re.search(r'PRIMARY\s+INDEX[^(]*\(([^)]+)\)', block, re.IGNORECASE)
        if pi:
            pk_cols = {c.strip().upper() for c in pi.group(1).split(',')}

        # Parse column lines
        cols = []
        for line in body.split('\n'):
            line = line.strip().lstrip(',').strip()
            if not line or line.upper().startswith('--'):
                continue
            # Grab col_name + type
            cm = re.match(
                r'^(\w[\w$#]*)\s+((?:[A-Z_]+)(?:\s*\(\s*[\d,\s]+\))?)',
                line, re.IGNORECASE
            )
            if not cm:
                continue
            col_name = cm.group(1)
            col_type = cm.group(2).strip()
            # skip keywords
            if col_name.upper() in ('PRIMARY', 'UNIQUE', 'INDEX', 'CONSTRAINT', 'CHECK', 'FOREIGN'):
                continue
            nullable = "NOT NULL" if re.search(r'\bNOT\s+NULL\b', line, re.IGNORECASE) else "NULL"
            pk = "Y" if col_name.upper() in pk_cols else ""
            cols.append({'name': col_name, 'type': col_type, 'pk': pk, 'nullable': nullable})

        tables[tbl] = {'schema': schema, 'ddl': block, 'columns': cols}
    return tables


def parse_excel(filepath: str):
    """
    Read the Excel workbook. Returns:
    tables: OrderedDict  key=(excel_type, norm_table_name)  val={
        'excel_type': str,
        'excel_name': str,   # original spaced name
        'norm_name':  str,   # underscored name
        'ddl': str,
        'columns': [ {'name', 'pk', 'nullable'} ]
    }
    """
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active

    tables = OrderedDict()
    last_type = last_norm = last_excel = None
    last_ddl = None

    for row in ws.iter_rows(min_row=2, values_only=True):
        ttype, tname, col_name, pk, nullable, ddl = row

        # forward-fill A and B
        if ttype:
            last_type = ttype.strip()
        if tname:
            last_excel = tname.strip()
            last_norm  = normalize_name(tname)
            last_ddl   = ddl  # DDL only on first row of table
            # Register table even if it has no column rows (e.g. PARTY CONTACT
            # has only the header row with no column data — columns come from SQL file)
            key = (last_type, last_norm)
            if last_type and last_norm and key not in tables:
                tables[key] = {
                    'excel_type': last_type,
                    'excel_name': last_excel,
                    'norm_name':  last_norm,
                    'ddl':        last_ddl or "",
                    'columns':    [],
                }

        if not last_type or not last_norm or not col_name:
            continue

        key = (last_type, last_norm)
        if key not in tables:
            tables[key] = {
                'excel_type': last_type,
                'excel_name': last_excel,
                'norm_name':  last_norm,
                'ddl':        last_ddl or "",
                'columns':    [],
            }

        tables[key]['columns'].append({
            'name':     col_name.strip(),
            'pk':       pk.strip() if pk else "",
            'nullable': nullable.strip() if nullable else "",
        })

    return tables


# ─── main ─────────────────────────────────────────────────────────────────────

def main():
    print("Reading SQL files …")
    cdm_tables  = parse_sql_file(CDM_SQL)
    pim_tables  = parse_sql_file(PIM_SQL)
    cust_tables = parse_sql_file(CUSTOM_SQL)

    # All authoritative SQL-defined tables (for type lookup)
    sql_master = {}
    sql_master.update(cdm_tables)
    sql_master.update(pim_tables)
    sql_master.update(cust_tables)

    print("Reading Excel …")
    excel_tables = parse_excel(EXCEL_PATH)

    # ── detect Excel table-name typos: DDL says TABLE X but Excel spells it Y ─
    excel_typos = {}   # misspelled_norm → correct_norm
    for (etype, nname), info in excel_tables.items():
        if not info['ddl']:
            continue
        m = re.search(r'CREATE\s+(?:MULTISET\s+)?TABLE\s+\w+\.(\w+)', info['ddl'], re.IGNORECASE)
        if m:
            ddl_name = m.group(1).upper()
            if ddl_name != nname and ddl_name in {n for (_, n) in excel_tables}:
                excel_typos[nname] = ddl_name

    # Remove typo duplicates — keep the correctly-spelled entry
    for typo_key in list(excel_tables.keys()):
        etype, nname = typo_key
        if nname in excel_typos:
            del excel_tables[typo_key]

    # Drop header-only rows that have no columns AND no CREATE TABLE DDL
    # (e.g. SERVICES_BB, INDIVIDUAL_BB are Layer 2 placeholders, not Layer 1 tables)
    ALL_SQL_NAMES = (
        set(cdm_tables.keys()) | set(pim_tables.keys()) | set(cust_tables.keys())
    )
    KNOWN_ALIASES = {'PARTY_CONTACT', 'PARTY_ADDRESS'}  # keep even if no cols
    for key in list(excel_tables.keys()):
        etype, nname = key
        info = excel_tables[key]
        has_cols = bool(info['columns'])
        has_ddl  = bool(re.search(r'CREATE\s+(?:MULTISET\s+)?TABLE', info['ddl'], re.IGNORECASE))
        in_sql   = nname in ALL_SQL_NAMES or nname in KNOWN_ALIASES
        if not has_cols and not has_ddl and not in_sql:
            del excel_tables[key]

    # Build schema assignment: MDM → CDM or PIM
    CDM_NAMES = set(cdm_tables.keys())
    PIM_NAMES = set(pim_tables.keys())

    # Also handle "PARTY CONTACT" → CONTACT mapping
    ALIASES = {
        'PARTY_CONTACT': 'CONTACT',
        'PARTY_ADDRESS': None,   # no SQL match → anomaly
    }

    # ── classify each Excel table ──────────────────────────────────────────────
    # schema_map: (etype, nname) → schema string  (keyed by full tuple to avoid
    # collision when the same table name appears in both iDM and MDM sections)
    schema_map = {}
    for (etype, nname), info in excel_tables.items():
        effective = ALIASES.get(nname, nname)
        if etype == 'iDM':
            schema_map[(etype, nname)] = 'Core_DB'
        elif effective in CDM_NAMES:
            schema_map[(etype, nname)] = 'CDM_DB'
        elif effective in PIM_NAMES:
            schema_map[(etype, nname)] = 'PIM_DB'
        else:
            schema_map[(etype, nname)] = 'UNKNOWN'

    # ── gather column type info ────────────────────────────────────────────────
    # For iDM tables: parse type from the Excel DDL (column F)
    # For CDM/PIM: use the SQL-file column list (authoritative)

    def get_columns_with_types(nname, info, schema):
        """Return list of dicts: name, type, pk, nullable."""
        effective = ALIASES.get(nname, nname)
        if schema in ('CDM_DB', 'PIM_DB') and effective and effective in sql_master:
            # Use SQL-file authoritative columns
            return sql_master[effective]['columns']
        # iDM or unknown: use Excel columns + type from Excel DDL
        ddl = info['ddl']
        cols = []
        for c in info['columns']:
            typ = extract_col_type(c['name'], ddl)
            cols.append({'name': c['name'], 'type': typ, 'pk': c['pk'], 'nullable': c['nullable']})
        return cols

    # ── build final table registry grouped by output schema ───────────────────
    # Groups: Core_DB (iDM), CDM_DB, PIM_DB, UNKNOWN
    groups = OrderedDict([
        ('Core_DB', []),
        ('CDM_DB',  []),
        ('PIM_DB',  []),
        ('UNKNOWN', []),
    ])

    for (etype, nname), info in excel_tables.items():
        schema = schema_map[(etype, nname)]
        effective = ALIASES.get(nname, nname)
        cols = get_columns_with_types(nname, info, schema)

        # raw DDL: prefer SQL-file DDL for CDM/PIM; fall back to Excel DDL
        if schema == 'CDM_DB' and effective in cdm_tables:
            raw_ddl = cdm_tables[effective]['ddl']
        elif schema == 'PIM_DB' and effective in pim_tables:
            raw_ddl = pim_tables[effective]['ddl']
        else:
            raw_ddl = info['ddl']

        entry = {
            'norm_name':   nname,
            'excel_name':  info['excel_name'],
            'excel_type':  etype,
            'schema':      schema,
            'effective':   effective,
            'columns':     cols,
            'raw_ddl':     raw_ddl,
        }
        groups[schema].append(entry)

    # ── anomaly detection ──────────────────────────────────────────────────────
    anomalies = []

    # 0. Excel table-name typos detected above
    for typo, correct in excel_typos.items():
        anomalies.append(
            f"**Excel table-name typo** — Excel row labelled `{typo}` is a duplicate of `{correct}` "
            f"(same DDL, different spelling in column B). The typo entry has been removed; "
            f"only `{correct}` is included in this document."
        )

    # Collect all table PKs for FK reference checking
    pk_map = {}   # norm_name → set of PK col names
    for schema_tables in groups.values():
        for t in schema_tables:
            pks = {c['name'].upper() for c in t['columns'] if c.get('pk') == 'Y'}
            pk_map[t['norm_name']] = pks

    # Collect all column names with their types across all tables
    all_col_info = []  # (table_name, col_name, col_type, pk, nullable)
    for schema_tables in groups.values():
        for t in schema_tables:
            for c in t['columns']:
                all_col_info.append((t['norm_name'], c['name'], c.get('type', ''), c.get('pk', ''), c.get('nullable', '')))

    # 1. ST_Geometry columns
    for tbl, col, typ, pk, null in all_col_info:
        if 'ST_GEOMETRY' in typ.upper() or 'GEOSPTL' in col.upper():
            anomalies.append(
                f"**ST_Geometry / spatial column** — `{tbl}.{col}` type `{typ}` cannot be represented in CSV."
            )

    # 2. Tables with no PK defined
    for schema_tables in groups.values():
        for t in schema_tables:
            pks = [c for c in t['columns'] if c.get('pk') == 'Y']
            if not pks:
                anomalies.append(
                    f"**No PK defined** — `{t['norm_name']}` has no column marked PK in Excel source."
                )

    # 3. INTEGER columns that are FKs (end in _Id, NOT NULL, not PK)
    for tbl, col, typ, pk, null in all_col_info:
        if (col.upper().endswith('_ID')
                and pk != 'Y'
                and null == 'NOT NULL'
                and 'INT' in typ.upper()
                and typ.upper() not in ('BIGINT',)):
            anomalies.append(
                f"**INTEGER FK candidate** — `{tbl}.{col}` is `{typ}` NOT NULL (non-PK `_Id` column); "
                f"may need BIGINT for CDM_DB cross-schema joins."
            )

    # 4. *_Id columns NOT NULL but not PK (implicit FK)
    for tbl, col, typ, pk, null in all_col_info:
        if (col.upper().endswith('_ID')
                and pk != 'Y'
                and null == 'NOT NULL'):
            # only flag if not already flagged as INTEGER FK
            if not ('INT' in typ.upper() and typ.upper() not in ('BIGINT',)):
                anomalies.append(
                    f"**Implicit FK** — `{tbl}.{col}` (`{typ}`) is NOT NULL but not marked PK — "
                    f"likely references a parent table."
                )

    # 5. MDM tables not resolved to CDM/PIM
    for (etype, nname), schema in schema_map.items():
        if schema == 'UNKNOWN':
            anomalies.append(
                f"**Schema unknown** — Excel MDM table `{nname}` has no matching table in "
                f"CDM_DB.sql or PIM_DB.sql. DDL uses CORE_DB placeholder."
            )

    # 6. MDM tables whose Excel DDL says CORE_DB (schema mismatch note)
    anomalies.append(
        "**Schema prefix mismatch** — All MDM table DDLs in Excel column F use `CORE_DB.` prefix. "
        "Authoritative DDLs from `CDM_DB.sql` / `PIM_DB.sql` are used for column schemas above. "
        "The CORE_DB-prefixed DDL is preserved verbatim in the raw DDL section (Excel source)."
    )

    # 7. PARTY CONTACT → CONTACT alias
    anomalies.append(
        "**Name alias** — Excel MDM table `PARTY_CONTACT` (no DDL in column F) maps to "
        "`CDM_DB.CONTACT` in `CDM_DB.sql`. The CDM_DB.sql DDL is used."
    )

    # 8. CDM_DB.ADDRESS missing CDM_Address_Id
    for tbl, col, typ, pk, null in all_col_info:
        if tbl == 'ADDRESS' and 'CDM_ADDRESS_ID' not in {c['name'].upper() for c in sql_master.get('ADDRESS', {}).get('columns', [])}:
            anomalies.append(
                "**Missing surrogate PK** — `CDM_DB.ADDRESS` DDL does not define `CDM_Address_Id`. "
                "Per `05_architect-qa.md` Q6, a BIGINT surrogate key must be added to the generated CSV."
            )
            break

    # de-dup anomalies
    seen = set()
    deduped = []
    for a in anomalies:
        key = a[:60]
        if key not in seen:
            seen.add(key)
            deduped.append(a)
    anomalies = deduped

    # ── console summary ────────────────────────────────────────────────────────
    total = sum(len(v) for v in groups.values())
    print(f"\n{'='*60}")
    print(f"Total tables: {total}")
    for schema, tbls in groups.items():
        print(f"  {schema:12s}: {len(tbls):3d} tables")
    print(f"\nAnomalies detected: {len(anomalies)}")
    for a in anomalies:
        print(f"  • {a[:100]}")
    print(f"{'='*60}\n")

    # ── markdown generation ────────────────────────────────────────────────────
    lines = []
    A = lines.append  # shorthand

    A("# CIF Layer 1 Schema Reference")
    A(f"_Generated from `{EXCEL_PATH}` + SQL DDL files. Total tables: {total}_")
    A("")

    # ── Summary Table ──────────────────────────────────────────────────────────
    A("## Summary Table")
    A("")
    A("| Schema | Table Name | Column Count | PK Columns |")
    A("|--------|------------|-------------|------------|")
    for schema, tbls in groups.items():
        for t in tbls:
            pk_cols = [c['name'] for c in t['columns'] if c.get('pk') == 'Y']
            pk_str = ", ".join(pk_cols) if pk_cols else "_(none)_"
            A(f"| {schema} | `{t['norm_name']}` | {len(t['columns'])} | {pk_str} |")
    A("")

    # ── Schemas by Table Type ──────────────────────────────────────────────────
    A("---")
    A("")
    A("## Schemas by Table Type")
    A("")

    section_titles = {
        'Core_DB': '### iDM Tables (Core_DB)',
        'CDM_DB':  '### CDM Tables (CDM_DB)',
        'PIM_DB':  '### PIM Tables (PIM_DB)',
        'UNKNOWN': '### Unresolved MDM Tables',
    }

    for schema, tbls in groups.items():
        if not tbls:
            continue
        A(section_titles[schema])
        A("")
        for t in tbls:
            A(f"#### {t['norm_name']}")
            if t['excel_name'].replace(' ', '_').upper() != t['norm_name']:
                A(f"_Excel name: \"{t['excel_name']}\"_  ")
            if schema in ('CDM_DB', 'PIM_DB') and t['effective'] and t['effective'] != t['norm_name']:
                A(f"_SQL file table: `{schema}.{t['effective']}`_  ")
            A("")
            A("| Column Name | Type (from DDL) | PK | Nullable |")
            A("|-------------|-----------------|----| ---------|")
            for c in t['columns']:
                pk_flag  = c.get('pk', '')
                nullable = c.get('nullable', '')
                typ      = c.get('type', '')
                A(f"| `{c['name']}` | `{typ}` | {pk_flag} | {nullable} |")
            A("")

    # ── Anomalies ──────────────────────────────────────────────────────────────
    A("---")
    A("")
    A("## DDL Anomalies & Notes")
    A("")
    for i, note in enumerate(anomalies, 1):
        A(f"{i}. {note}")
    A("")

    # ── Raw DDL ────────────────────────────────────────────────────────────────
    A("---")
    A("")
    A("## Raw DDL")
    A("")
    A("> For **CDM_DB** and **PIM_DB** tables the DDL shown is from the authoritative "
      "`CDM_DB.sql` / `PIM_DB.sql` files (correct schema prefix). "
      "For **Core_DB (iDM)** tables the DDL is from Excel column F.")
    A("")

    for schema, tbls in groups.items():
        if not tbls:
            continue
        A(f"### {schema}")
        A("")
        for t in tbls:
            A(f"#### {t['norm_name']}")
            A("")
            ddl = t['raw_ddl'].strip() if t['raw_ddl'] else "-- DDL not available"
            A("```sql")
            A(ddl)
            A("```")
            A("")

    # ── write file ─────────────────────────────────────────────────────────────
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"Written -> {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
