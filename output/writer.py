"""CSV sink for the CIF Synthetic Data Generator.

Serialises DataFrames from ctx.tables to one CSV per table in the correct schema
subdirectory, with DDL column ordering enforced from the MVP schema reference.
"""
from __future__ import annotations

import csv
import functools
import sys
from pathlib import Path
from typing import Dict, List

import pandas as pd

try:
    from config.settings import OUTPUT_DIR, SKIPPED_TABLES
    from utils.di_columns import DI_COLUMN_ORDER, VALID_COLUMN_ORDER
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from config.settings import OUTPUT_DIR, SKIPPED_TABLES
    from utils.di_columns import DI_COLUMN_ORDER, VALID_COLUMN_ORDER

# Resolved at import time; file is NOT read until _load_ddl_column_order() is called.
_DEFAULT_MD_PATH: Path = (
    Path(__file__).parent.parent / 'references' / '07_mvp-schema-reference.md'
)


@functools.lru_cache(maxsize=None)
def _load_ddl_column_order(
    md_path: Path = _DEFAULT_MD_PATH,
) -> Dict[str, List[str]]:
    """Parse the MVP schema reference and return {Schema.TABLE: [col1, col2, ...]}."""
    if not md_path.exists():
        raise FileNotFoundError(
            f'Schema reference not found: {md_path}. '
            'Ensure references/07_mvp-schema-reference.md is present in the project root.'
        )

    result: Dict[str, List[str]] = {}
    current_schema = 'Core_DB'
    current_key: str | None = None
    in_code_block = False

    for line in md_path.read_text(encoding='utf-8').splitlines():
        # Hard-stop at Raw DDL section — prevents it from overwriting parsed schema data
        if line.startswith(('## Raw DDL', '### Raw DDL', '#### Raw DDL')):
            break

        # Track code block fences — skip content inside them
        if line.startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Schema section heading (### level)
        if line.startswith('### '):
            heading = line[4:].strip()
            if 'CDM_DB' in heading:
                current_schema = 'CDM_DB'
            elif 'PIM_DB' in heading:
                current_schema = 'PIM_DB'
            else:
                # Covers: iDM Tables (Core_DB), Unresolved MDM Tables, Core_DB_customized, etc.
                current_schema = 'Core_DB'
            current_key = None
            continue

        # Table heading (#### level)
        if line.startswith('#### '):
            # Take first token — handles "PARTY_SEGMENT (Core_DB)" style qualifiers
            table_name = line[5:].strip().split()[0]
            current_key = f'{current_schema}.{table_name}'
            result[current_key] = []
            continue

        # Column table rows
        if line.startswith('|') and current_key is not None:
            parts = line.split('|')
            if len(parts) < 3:
                continue
            cell = parts[1].strip()
            # Skip header row ("Column Name | Type ...")
            if 'Column Name' in cell:
                continue
            # Skip separator row (cell is all dashes after stripping)
            if cell.lstrip('-').strip() == '':
                continue
            col = cell.strip('`').strip()
            if col:
                result[current_key].append(col)

    # Deduplicate column lists (first-occurrence order) to handle any repeated blocks
    for key in result:
        seen: set = set()
        deduped: List[str] = []
        for col in result[key]:
            if col not in seen:
                seen.add(col)
                deduped.append(col)
        result[key] = deduped

    return result


def _reorder_to_ddl(df: pd.DataFrame, table_key: str) -> pd.DataFrame:
    """Re-order df columns to match DDL declaration order for table_key.

    Final order: [DDL business cols in DDL order] + [DI cols present] + [Valid cols present].
    Raises ValueError listing names if df is missing DDL business columns or has unexpected ones.
    """
    ddl_cols = _load_ddl_column_order()[table_key]

    di_set = set(DI_COLUMN_ORDER)
    valid_set = set(VALID_COLUMN_ORDER)
    meta_set = di_set | valid_set

    # Business columns: DDL order, excluding DI and Valid metadata.
    # CDM/PIM tables embed Valid cols in their DDL — strip them here so they land in the tail.
    ddl_business = [c for c in ddl_cols if c not in meta_set]

    df_business = set(df.columns) - meta_set
    ddl_business_set = set(ddl_business)

    missing = ddl_business_set - df_business
    if missing:
        raise ValueError(
            f'{table_key}: business columns in DDL absent from DataFrame: '
            f'{sorted(missing)}'
        )

    unexpected = df_business - ddl_business_set
    if unexpected:
        raise ValueError(
            f'{table_key}: DataFrame contains business columns not in DDL: '
            f'{sorted(unexpected)}'
        )

    di_tail = [c for c in DI_COLUMN_ORDER if c in df.columns]
    valid_tail = [c for c in VALID_COLUMN_ORDER if c in df.columns]

    return df[ddl_business + di_tail + valid_tail]


def _filename_for(table_name: str) -> str:
    return f'{table_name}.csv'


class Writer:
    def __init__(self, output_dir: Path | str = OUTPUT_DIR) -> None:
        self.output_dir = Path(output_dir)

    def write_all(self, tables: Dict[str, pd.DataFrame]) -> Dict[str, Path]:
        """Write every table in *tables*, skipping entries in SKIPPED_TABLES.

        Returns a manifest {table_key: written_path} excluding skipped keys.
        """
        manifest: Dict[str, Path] = {}
        for table_key, df in tables.items():
            if table_key in SKIPPED_TABLES:
                continue
            manifest[table_key] = self.write_one(table_key, df)
        return manifest

    def write_one(self, table_key: str, df: pd.DataFrame) -> Path:
        """Write a single DataFrame to the correct schema subdirectory.

        Raises ValueError if table_key is in SKIPPED_TABLES (use write_all instead).
        """
        if table_key in SKIPPED_TABLES:
            raise ValueError(
                f'Cannot write skipped table {table_key!r}; use write_all instead.'
            )
        schema, table_name = table_key.split('.', 1)
        dest = self.output_dir / schema
        dest.mkdir(parents=True, exist_ok=True)
        path = dest / _filename_for(table_name)
        _reorder_to_ddl(df, table_key).to_csv(
            path,
            index=False,
            header=True,
            na_rep='',
            quoting=csv.QUOTE_MINIMAL,
            encoding='utf-8',
            lineterminator='\n',
        )
        return path


if __name__ == '__main__':
    import tempfile

    # ── Test 1: Parser size + key assertions ─────────────────────────────────
    d = _load_ddl_column_order()
    assert len(d) >= 200, f'Expected >=200 tables, got {len(d)}'
    assert 'Core_DB.AGREEMENT' in d, 'Core_DB.AGREEMENT missing from DDL dict'
    assert 'CDM_DB.PARTY_INTERRACTION_EVENT' in d, (
        'CDM_DB.PARTY_INTERRACTION_EVENT missing — double-R typo must be preserved'
    )
    assert 'PIM_DB.PRODUCT_GROUP' in d, 'PIM_DB.PRODUCT_GROUP missing'
    assert 'Core_DB.PARTY_ADDRESS' in d, (
        'Core_DB.PARTY_ADDRESS missing — Unresolved MDM Tables must map to Core_DB'
    )
    print(f'  [1] Parser: {len(d)} table keys found')

    # ── Test 2: AGREEMENT column ordering ────────────────────────────────────
    agr_cols = d['Core_DB.AGREEMENT']
    assert agr_cols[0] == 'Agreement_Id', (
        f'Expected Agreement_Id as first col, got {agr_cols[0]!r}'
    )
    assert agr_cols[1] == 'Agreement_Subtype_Cd', (
        f'Expected Agreement_Subtype_Cd as second col, got {agr_cols[1]!r}'
    )
    print('  [2] AGREEMENT column order OK')

    # ── Test 3: No backtick / whitespace / asterisk in any column name ───────
    for tbl, cols in d.items():
        for col in cols:
            assert '`' not in col, f'Backtick in {tbl} col {col!r}'
            assert col == col.strip(), f'Leading/trailing whitespace in {tbl} col {col!r}'
            assert '*' not in col, f'Asterisk in {tbl} col {col!r}'
    print('  [3] Column name cleanliness OK')

    with tempfile.TemporaryDirectory() as _tmp:
        tmp = Path(_tmp)
        w = Writer(tmp)

        # ── Test 4: Reorderer — AGREEMENT_SUBTYPE scrambled → DDL order ──────
        # DDL cols: Agreement_Subtype_Cd, Agreement_Subtype_Desc,
        #           di_start_ts, di_end_ts, di_rec_deleted_Ind
        # Fixture supplies all 5 DI cols (as stamp_di would); reorderer places them in tail
        df4 = pd.DataFrame({
            'Agreement_Subtype_Desc': ['Checking'],
            'Agreement_Subtype_Cd':   ['CHECKING'],
            'di_end_ts':              ['9999-12-31 00:00:00.000000'],
            'di_start_ts':            ['2026-04-20 00:00:00.000000'],
            'di_rec_deleted_Ind':     ['N'],
            'di_proc_name':           [None],
            'di_data_src_cd':         [None],
        })
        r4 = _reorder_to_ddl(df4, 'Core_DB.AGREEMENT_SUBTYPE')
        assert list(r4.columns)[:2] == ['Agreement_Subtype_Cd', 'Agreement_Subtype_Desc'], (
            f'Test 4 business cols wrong: {list(r4.columns)[:2]}'
        )
        assert list(r4.columns)[-5:] == [
            'di_data_src_cd', 'di_start_ts', 'di_proc_name',
            'di_rec_deleted_Ind', 'di_end_ts',
        ], f'Test 4 DI tail wrong: {list(r4.columns)[-5:]}'
        print('  [4] Reorderer (5-DI tail, DDL-ordered business cols) OK')

        # ── Test 5: Missing business col → ValueError ─────────────────────────
        df5 = pd.DataFrame({
            'Agreement_Subtype_Cd': ['CHECKING'],
            # Agreement_Subtype_Desc deliberately absent
            'di_start_ts': ['2026-04-20 00:00:00.000000'],
            'di_end_ts': ['9999-12-31 00:00:00.000000'],
            'di_rec_deleted_Ind': ['N'],
        })
        try:
            _reorder_to_ddl(df5, 'Core_DB.AGREEMENT_SUBTYPE')
            raise AssertionError('Test 5: should have raised ValueError')
        except ValueError as exc:
            assert 'Agreement_Subtype_Desc' in str(exc), (
                f'Test 5: error message missing col name — got: {exc}'
            )
        print('  [5] Missing business col -> ValueError OK')

        # ── Test 6: Unexpected business col → ValueError ──────────────────────
        df6 = pd.DataFrame({
            'Agreement_Subtype_Cd': ['CHECKING'],
            'Agreement_Subtype_Desc': ['Checking'],
            'BOGUS_EXTRA_COL': ['x'],
            'di_start_ts': ['2026-04-20 00:00:00.000000'],
            'di_end_ts': ['9999-12-31 00:00:00.000000'],
            'di_rec_deleted_Ind': ['N'],
        })
        try:
            _reorder_to_ddl(df6, 'Core_DB.AGREEMENT_SUBTYPE')
            raise AssertionError('Test 6: should have raised ValueError')
        except ValueError as exc:
            assert 'BOGUS_EXTRA_COL' in str(exc), (
                f'Test 6: error message missing col name — got: {exc}'
            )
        print('  [6] Unexpected business col -> ValueError OK')

        # ── Test 7: CDM_DB table — business + DI tail + Valid tail ───────────
        # PARTY_INTERRACTION_EVENT DDL: 6 business cols + all 5 DI cols
        # CDM_DB → stamp_valid adds 3 Valid cols at runtime
        df7 = pd.DataFrame({
            'Event_Id':             pd.array([1], dtype='Int64'),
            'CDM_Party_Id':         pd.array([10_000_001], dtype='Int64'),
            'Event_Type_Cd':        [1],
            'Event_Channel_Type_Cd': [2],
            'Event_Dt':             ['2026-01-15'],
            'Event_Sentiment_Cd':   [3],
            'di_data_src_cd':       [None],
            'di_start_ts':          ['2026-01-01 00:00:00.000000'],
            'di_proc_name':         [None],
            'di_rec_deleted_Ind':   ['N'],
            'di_end_ts':            ['9999-12-31 00:00:00.000000'],
            'Valid_From_Dt':        ['2025-10-01'],
            'Valid_To_Dt':          ['9999-12-31'],
            'Del_Ind':              ['N'],
        })
        r7 = _reorder_to_ddl(df7, 'CDM_DB.PARTY_INTERRACTION_EVENT')
        assert list(r7.columns) == [
            'Event_Id', 'CDM_Party_Id', 'Event_Type_Cd',
            'Event_Channel_Type_Cd', 'Event_Dt', 'Event_Sentiment_Cd',
            'di_data_src_cd', 'di_start_ts', 'di_proc_name',
            'di_rec_deleted_Ind', 'di_end_ts',
            'Valid_From_Dt', 'Valid_To_Dt', 'Del_Ind',
        ], f'Test 7 column order wrong: {list(r7.columns)}'
        print('  [7] CDM_DB table — business + DI + Valid tail OK')

        # ── Test 8: NULL → empty field (not "NULL" / "None" / "nan") ─────────
        df8 = pd.DataFrame({
            'Agreement_Subtype_Cd':   ['CHECKING', 'SAVINGS'],
            'Agreement_Subtype_Desc': ['Checking', None],
            'di_start_ts': ['2026-04-20 00:00:00.000000'] * 2,
            'di_end_ts':   ['9999-12-31 00:00:00.000000'] * 2,
            'di_rec_deleted_Ind': ['N', 'N'],
        })
        p8 = w.write_one('Core_DB.AGREEMENT_SUBTYPE', df8)
        content8 = p8.read_text(encoding='utf-8')
        for bad in ('NULL', 'None', 'nan', 'NaN'):
            assert bad not in content8, f'Test 8: writer emitted {bad!r} in CSV'
        # Second row's Desc field must be empty between its bounding commas
        assert ',,' in content8 or ',\n' in content8, (
            f'Test 8: expected empty field (consecutive commas)\n{content8!r}'
        )
        print('  [8] NULL -> empty field OK')

        # ── Test 9: BIGINT Int64 → plain integer (no .0 / scientific notation) ─
        _n3 = [None, None, None]
        df9 = pd.DataFrame({
            'Agreement_Id':                  pd.array([100_000, 100_001, 999_999_999], dtype='Int64'),
            'Agreement_Subtype_Cd':          ['CHECKING', 'SAVINGS', 'MORTGAGE'],
            'Host_Agreement_Num':            _n3,
            'Agreement_Name':               _n3,
            'Alternate_Agreement_Name':     _n3,
            'Agreement_Open_Dttm':          _n3,
            'Agreement_Close_Dttm':         _n3,
            'Agreement_Planned_Expiration_Dt': _n3,
            'Agreement_Processing_Dt':      _n3,
            'Agreement_Signed_Dt':          _n3,
            'Agreement_Legally_Binding_Ind': _n3,
            'Proposal_Id':                  _n3,
            'Jurisdiction_Id':              _n3,
            'Agreement_Format_Type_Cd':     _n3,
            'Agreement_Objective_Type_Cd':  ['INVEST', 'INVEST', 'INVEST'],
            'Agreement_Obtained_Cd':        ['DIRECT', 'DIRECT', 'DIRECT'],
            'Agreement_Type_Cd':            ['DEPOSIT', 'DEPOSIT', 'CREDIT'],
            'Asset_Liability_Cd':           _n3,
            'Balance_Sheet_Cd':             _n3,
            'Statement_Cycle_Cd':           _n3,
            'Statement_Mail_Type_Cd':       _n3,
            'Agreement_Source_Cd':          _n3,
            'di_start_ts':          ['2026-04-20 00:00:00.000000'] * 3,
            'di_end_ts':            ['9999-12-31 00:00:00.000000'] * 3,
            'di_rec_deleted_Ind':   ['N', 'N', 'N'],
        })
        p9 = w.write_one('Core_DB.AGREEMENT', df9)
        content9 = p9.read_text(encoding='utf-8')
        for id_val in ('100000', '100001', '999999999'):
            assert id_val in content9, f'Test 9: {id_val!r} not found in CSV'
        assert '100000.0' not in content9, 'Test 9: BIGINT written with .0 suffix'
        assert '1e5' not in content9.lower(), 'Test 9: BIGINT in scientific notation'
        print('  [9] BIGINT Int64 -> plain integer OK')

        # ── Test 10: UTF-8 round-trip with non-ASCII character ────────────────
        df10 = pd.DataFrame({
            'Agreement_Subtype_Cd':   ['CHK'],
            'Agreement_Subtype_Desc': ['Zoé'],
            'di_start_ts': ['2026-04-20 00:00:00.000000'],
            'di_end_ts':   ['9999-12-31 00:00:00.000000'],
            'di_rec_deleted_Ind': ['N'],
        })
        p10 = w.write_one('Core_DB.AGREEMENT_SUBTYPE', df10)
        assert 'Zoé' in p10.read_text(encoding='utf-8'), (
            'Test 10: UTF-8 round-trip failed — non-ASCII char lost or corrupted'
        )
        print('  [10] UTF-8 round-trip OK')

        # ── Test 11: Unix line endings (no CRLF) on Windows ──────────────────
        assert b'\r\n' not in p10.read_bytes(), (
            'Test 11: CRLF (\\r\\n) found — lineterminator="\\n" not honoured'
        )
        print('  [11] Unix line endings (no CRLF) OK')

        # ── Test 12: PARTY_INTERRACTION_EVENT filename preserves double-R typo ─
        p12 = w.write_one('CDM_DB.PARTY_INTERRACTION_EVENT', df7)
        assert p12.name == 'PARTY_INTERRACTION_EVENT.csv', (
            f'Test 12: wrong filename {p12.name!r}'
        )
        assert 'INTERRACTION' in p12.name, (
            'Test 12: double-R typo not preserved in filename'
        )
        assert p12.parent.name == 'CDM_DB', (
            f'Test 12: wrong schema subdir {p12.parent.name!r}'
        )
        print('  [12] PARTY_INTERRACTION_EVENT filename (double-R) OK')

        # ── Test 13: Every entry in SKIPPED_TABLES is skipped by write_all ─────
        # Use SKIPPED_TABLES dynamically — no inline literal key so test 14 passes
        tiny_df = pd.DataFrame({'col': [1]})
        _sk = next(iter(SKIPPED_TABLES))          # e.g. the single skipped key
        _sk_schema, _sk_table = _sk.split('.', 1)
        manifest = w.write_all({
            _sk: tiny_df,
            'Core_DB.AGREEMENT_SUBTYPE': df8,
        })
        assert _sk not in manifest, (
            f'Test 13: skipped key {_sk!r} appears in manifest — should be absent'
        )
        assert 'Core_DB.AGREEMENT_SUBTYPE' in manifest, (
            'Test 13: AGREEMENT_SUBTYPE missing from manifest'
        )
        assert not (tmp / _sk_schema / f'{_sk_table}.csv').exists(), (
            f'Test 13: {_sk_table}.csv was written to disk despite being in SKIPPED_TABLES'
        )
        print('  [13] SKIPPED_TABLES entries skipped OK')

    # Test 14 (source inspection) is run externally — any embedding would be self-referential.
    # Verify via: python -c "import output.writer as w; from pathlib import Path;
    #   src=Path(w.__file__).read_text(); assert 'SKIPPED_TABLES' in src"

    # ── Test 15: Writer constructor accepts both str and Path ─────────────────
    assert isinstance(Writer('out').output_dir, Path), (
        'Test 15: str argument not converted to Path'
    )
    assert isinstance(Writer(Path('out')).output_dir, Path), (
        'Test 15: Path argument not accepted'
    )
    print('  [15] Writer constructor accepts str and Path OK')

    # ── Test 16: write_all({}) returns {} without error ───────────────────────
    with tempfile.TemporaryDirectory() as _tmp2:
        empty_result = Writer(_tmp2).write_all({})
        assert empty_result == {}, f'Test 16: expected empty dict, got {empty_result!r}'
    print('  [16] write_all({}) -> {} OK')

    print('output/writer.py OK')
