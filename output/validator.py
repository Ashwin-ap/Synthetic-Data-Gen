"""Post-generation Layer 2 constraint validator for the CIF Synthetic Data Generator.

Validator.check_all(ctx) -> List[str]
  Returns a list of violation strings. Empty list = all 22 constraints pass + FK integrity clean.
  Never raises; always returns. No mutations on ctx.tables.
"""
from __future__ import annotations

import dataclasses
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import pandas as pd

# ---------------------------------------------------------------------------
# Imports — support running as `python output/validator.py` from project root
# ---------------------------------------------------------------------------
try:
    from config.settings import (
        HIGH_DATE,
        SIM_DATE,
        SKIPPED_TABLES,
        PARTY_INTERRACTION_EVENT_TABLE_NAME,
        BANK_PARTY_ID,
    )
    from config.code_values import (
        AGREEMENT_STATUS_SCHEMES,
        FROZEN_STATUS_ROW,
        LANGUAGE_USAGE_TYPES,
        PROFITABILITY_MODEL_TYPE_CD,
        CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD,
        RATE_FEATURE_SUBTYPE_CD,
        TERRITORY_ISO_STANDARD_CD,
    )
    from registry.context import GenerationContext
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from config.settings import (
        HIGH_DATE,
        SIM_DATE,
        SKIPPED_TABLES,
        PARTY_INTERRACTION_EVENT_TABLE_NAME,
        BANK_PARTY_ID,
    )
    from config.code_values import (
        AGREEMENT_STATUS_SCHEMES,
        FROZEN_STATUS_ROW,
        LANGUAGE_USAGE_TYPES,
        PROFITABILITY_MODEL_TYPE_CD,
        CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD,
        RATE_FEATURE_SUBTYPE_CD,
        TERRITORY_ISO_STANDARD_CD,
    )
    from registry.context import GenerationContext

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

_MAX_VIOLATIONS_PER_CHECK: int = 5

# Layer 2 literal-match strings (PRD §7.11) — never hardcode inline
_CUSTOMER_ROLE_CD:          str = 'customer'
_BORROWER_ROLE_CD:          str = 'borrower'
_CUSTOMER_OF_ENTERPRISE_CD: str = 'customer of enterprise'
_PRIMARY_ROLE_CD:           str = 'primary'
_PREFERRED_CURRENCY_USE_CD: str = 'preferred'
_PRIMARY_IND_YES:           str = 'Yes'
_REQUIRED_ID_TYPES: frozenset = frozenset({'SSN', "Driver's License", 'Passport'})

# PIM hierarchy integer codes (verified: tier15_pim.py stores Int64 1/2)
_PIM_ROOT_TYPE_CD:      int = 1
_PIM_CLV_CHILD_TYPE_CD: int = 2
_PIM_CLV_CHILD_COUNT:   int = 8

# ---------------------------------------------------------------------------
# FK manifest: (child_table, child_col, parent_table, parent_col)
# Parent for all Party_Id FKs is CDM_DB.PARTY.CDM_Party_Id — shared ID space
# per PRD §7.2 / Decision 4.
# ---------------------------------------------------------------------------
_FK_MANIFEST: List[Tuple[str, str, str, str]] = [
    ('Core_DB.PARTY_AGREEMENT',     'Agreement_Id',        'Core_DB.AGREEMENT',   'Agreement_Id'),
    ('Core_DB.PARTY_AGREEMENT',     'Party_Id',            'CDM_DB.PARTY',        'CDM_Party_Id'),
    ('Core_DB.AGREEMENT_STATUS',    'Agreement_Id',        'Core_DB.AGREEMENT',   'Agreement_Id'),
    ('Core_DB.AGREEMENT_CURRENCY',  'Agreement_Id',        'Core_DB.AGREEMENT',   'Agreement_Id'),
    ('Core_DB.AGREEMENT_SCORE',     'Agreement_Id',        'Core_DB.AGREEMENT',   'Agreement_Id'),
    ('Core_DB.AGREEMENT_FEATURE',   'Agreement_Id',        'Core_DB.AGREEMENT',   'Agreement_Id'),
    ('Core_DB.AGREEMENT_PRODUCT',   'Agreement_Id',        'Core_DB.AGREEMENT',   'Agreement_Id'),
    ('Core_DB.AGREEMENT_PRODUCT',   'Product_Id',          'Core_DB.PRODUCT',     'Product_Id'),
    ('Core_DB.PARTY_RELATED',       'Party_Id',            'CDM_DB.PARTY',        'CDM_Party_Id'),
    ('Core_DB.PARTY_LOCATOR',       'Party_Id',            'CDM_DB.PARTY',        'CDM_Party_Id'),
    ('Core_DB.PARTY_LOCATOR',       'Locator_Id',          'Core_DB.ADDRESS',     'Address_Id'),
    ('Core_DB.EVENT_PARTY',         'Event_Id',            'Core_DB.EVENT',       'Event_Id'),
    ('Core_DB.CAMPAIGN_STATUS',     'Campaign_Id',         'Core_DB.CAMPAIGN',    'Campaign_Id'),
    ('Core_DB.PROMOTION_OFFER',     'Promotion_Id',        'Core_DB.PROMOTION',   'Promotion_Id'),
    ('Core_DB.PARTY_IDENTIFICATION','Party_Id',            'Core_DB.INDIVIDUAL',  'Individual_Party_Id'),
    ('Core_DB.INDIVIDUAL_NAME',     'Individual_Party_Id', 'Core_DB.INDIVIDUAL',  'Individual_Party_Id'),
    ('Core_DB.PARTY_SCORE',         'Party_Id',            'CDM_DB.PARTY',        'CDM_Party_Id'),
    ('Core_DB.PARTY_STATUS',        'Party_Id',            'CDM_DB.PARTY',        'CDM_Party_Id'),
    ('PIM_DB.PRODUCT',              'Product_Id',          'Core_DB.PRODUCT',     'Product_Id'),
    ('Core_DB.PARTY_LANGUAGE_USAGE','Party_Id',            'CDM_DB.PARTY',        'CDM_Party_Id'),
]


# ---------------------------------------------------------------------------
# Validator class
# ---------------------------------------------------------------------------

class Validator:
    """Runs all 22 Layer 2 transformation-readiness checks plus FK integrity.

    Usage::

        errors = Validator().check_all(ctx)
        if errors:
            for e in errors:
                print(f'VALIDATION ERROR: {e}')
            sys.exit(1)
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def check_all(self, ctx: GenerationContext) -> List[str]:
        """Run all 22 constraint checks + FK integrity in one pass.

        Returns a list of violation strings. Empty list = all constraints pass.
        Never raises — every check returns List[str].
        """
        violations: List[str] = []
        for method in [
            self._check_01_agreement_status_6_schemes,
            self._check_02_lookup_desc_populated,
            self._check_03_individual_name_sim_date_window,
            self._check_04_party_language_usage_two_rows,
            self._check_05_party_status_at_least_one,
            self._check_06_agreement_feature_rate_for_loans,
            self._check_07_agreement_product_primary_role,
            self._check_08_agreement_currency_preferred,
            self._check_09_party_agreement_customer_role,
            self._check_10_party_related_customer_of_enterprise,
            self._check_11_party_agreement_borrower_for_loans,
            self._check_12_party_agreement_customer_for_retail,
            self._check_13_frozen_status_code_FROZEN,
            self._check_14_organization_primary_naics_sic_gics,
            self._check_15_campaign_status_at_least_one,
            self._check_16_promotion_offer_at_most_five,
            self._check_17_agreement_score_profitability,
            self._check_18_party_score_customer_profitability,
            self._check_19_iso_3166_country_subdivision_populated,
            self._check_20_pim_product_group_clv_hierarchy,
            self._check_21_frozen_status_desc_exact_match,
            self._check_22_party_identification_ssn_passport_dl,
            self._check_fk_integrity,
        ]:
            violations.extend(method(ctx))
        return violations

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_table(
        self, ctx: GenerationContext, key: str
    ) -> Tuple[Optional[pd.DataFrame], List[str]]:
        """Return (df, []) if key is present and not skipped; (None, [error]) otherwise."""
        if key in SKIPPED_TABLES:
            return None, []
        if key not in ctx.tables:
            return None, [f'required table {key} missing from ctx.tables']
        return ctx.tables[key], []

    def _cap(self, violations: List[str], tag: str) -> List[str]:
        """Cap to _MAX_VIOLATIONS_PER_CHECK, appending a summary line if truncated."""
        if len(violations) <= _MAX_VIOLATIONS_PER_CHECK:
            return violations
        extra = len(violations) - _MAX_VIOLATIONS_PER_CHECK
        return violations[:_MAX_VIOLATIONS_PER_CHECK] + [
            f'{tag} ... and {extra} more violations'
        ]

    # ------------------------------------------------------------------
    # Constraint checks #1–#22
    # ------------------------------------------------------------------

    def _check_01_agreement_status_6_schemes(self, ctx: GenerationContext) -> List[str]:
        """#1 — AGREEMENT_STATUS has all 6 scheme types per agreement (current rows only).
        §12 row 1; 02-map-ref Step 3 item #1."""
        tag = '[#1 AGREEMENT_STATUS 6 schemes]'
        df, errs = self._get_table(ctx, 'Core_DB.AGREEMENT_STATUS')
        if df is None:
            return errs

        required = set(AGREEMENT_STATUS_SCHEMES)
        # Current rows: Agreement_Status_End_Dttm is None/NaT (historical rows have a real dttm)
        current = df[df['Agreement_Status_End_Dttm'].isna()]

        violations: List[str] = []
        grouped = current.groupby('Agreement_Id')['Agreement_Status_Scheme_Cd'].apply(set)
        for agr_id in sorted(grouped.index):
            actual = grouped[agr_id]
            missing = required - actual
            if missing:
                violations.append(
                    f"{tag} Core_DB.AGREEMENT_STATUS: "
                    f"Agreement_Id={agr_id} missing schemes {sorted(missing)}"
                )
        return self._cap(violations, tag)

    def _check_02_lookup_desc_populated(self, ctx: GenerationContext) -> List[str]:
        """#2 — Every *_TYPE/*_SUBTYPE/*_CLASSIFICATION lookup table has *_Desc columns non-null.
        §12 row 2; 02-map-ref Step 3 item #2."""
        tag = '[#2 lookup_desc]'
        violations: List[str] = []

        for key, df in ctx.tables.items():
            if key in SKIPPED_TABLES:
                continue
            table_name = key.split('.', 1)[1]
            is_lookup = ('_TYPE' in table_name or '_SUBTYPE' in table_name
                         or '_CLASSIFICATION' in table_name)
            if not is_lookup:
                continue
            desc_cols = [c for c in df.columns if c.endswith('_Desc')]
            for col in desc_cols:
                null_count = int(df[col].isna().sum())
                if null_count > 0:
                    violations.append(
                        f"{tag} {key}: {col} has {null_count} NULL row(s)"
                    )
        return violations  # not capped — each entry is a distinct table+column pair

    def _check_03_individual_name_sim_date_window(self, ctx: GenerationContext) -> List[str]:
        """#3 — INDIVIDUAL_NAME: SIM_DATE in [Individual_Name_Start_Dt, Individual_Name_End_Dt].
        §12 row 3; 02-map-ref Step 3 item #3."""
        tag = '[#3 INDIVIDUAL_NAME window]'
        df, errs = self._get_table(ctx, 'Core_DB.INDIVIDUAL_NAME')
        if df is None:
            return errs

        sim = pd.Timestamp(SIM_DATE)
        start = pd.to_datetime(df['Individual_Name_Start_Dt'], errors='coerce')
        end   = pd.to_datetime(df['Individual_Name_End_Dt'],   errors='coerce')
        # NaT end_dt means open-ended → satisfies upper bound; keep as-is (NaT < sim → False)
        bad_mask = (start > sim) | (end.notna() & (end < sim))
        bad = df[bad_mask]

        violations: List[str] = []
        for _, row in bad.iterrows():
            violations.append(
                f"{tag} Core_DB.INDIVIDUAL_NAME: "
                f"Individual_Party_Id={row['Individual_Party_Id']}: "
                f"Start_Dt={row['Individual_Name_Start_Dt']}, "
                f"End_Dt={row['Individual_Name_End_Dt']} "
                f"(SIM_DATE={SIM_DATE})"
            )
        return self._cap(violations, tag)

    def _check_04_party_language_usage_two_rows(self, ctx: GenerationContext) -> List[str]:
        """#4 — PARTY_LANGUAGE_USAGE: each party has 'primary spoken language' +
        'primary written language' in Language_Usage_Type_Cd.
        §12 row 4; 02-map-ref Step 3 item #4."""
        tag = '[#4 PARTY_LANGUAGE_USAGE two rows]'
        df, errs = self._get_table(ctx, 'Core_DB.PARTY_LANGUAGE_USAGE')
        if df is None:
            return errs

        required = set(LANGUAGE_USAGE_TYPES)
        violations: List[str] = []

        # Build type-set per party that has at least one row
        grouped = df.groupby('Party_Id')['Language_Usage_Type_Cd'].apply(set)
        for party_id in sorted(grouped.index):
            missing = required - grouped[party_id]
            if missing:
                violations.append(
                    f"{tag} Core_DB.PARTY_LANGUAGE_USAGE: "
                    f"Party_Id={party_id} missing type(s) {sorted(missing)}"
                )

        # Also catch parties that have zero rows (absent entirely)
        cdm_df, _ = self._get_table(ctx, 'CDM_DB.PARTY')
        if cdm_df is not None:
            all_ids    = set(cdm_df['CDM_Party_Id'].dropna()) - {BANK_PARTY_ID}
            present    = set(grouped.index)
            absent_ids = all_ids - present
            for party_id in sorted(absent_ids):
                violations.append(
                    f"{tag} Core_DB.PARTY_LANGUAGE_USAGE: "
                    f"Party_Id={party_id} has no language usage rows"
                )

        return self._cap(violations, tag)

    def _check_05_party_status_at_least_one(self, ctx: GenerationContext) -> List[str]:
        """#5 — PARTY_STATUS: every CDM_DB.PARTY party has ≥1 status row.
        §12 row 5; 02-map-ref Step 3 item #5."""
        tag = '[#5 PARTY_STATUS at-least-one]'
        cdm_df, errs1 = self._get_table(ctx, 'CDM_DB.PARTY')
        status_df, errs2 = self._get_table(ctx, 'Core_DB.PARTY_STATUS')
        if cdm_df is None or status_df is None:
            return errs1 + errs2

        # Exclude reserved bank/placeholder party (not a real customer)
        all_ids    = set(cdm_df['CDM_Party_Id'].dropna()) - {BANK_PARTY_ID}
        status_ids = set(status_df['Party_Id'].dropna())
        missing    = all_ids - status_ids

        violations = [
            f"{tag} Core_DB.PARTY_STATUS: Party_Id={pid} has no PARTY_STATUS row"
            for pid in sorted(missing)
        ]
        return self._cap(violations, tag)

    def _check_06_agreement_feature_rate_for_loans(self, ctx: GenerationContext) -> List[str]:
        """#6 — AGREEMENT_FEATURE: loan agreements (LOAN_TERM, MORTGAGE, CREDIT_CARD) have a
        Rate Feature row. §12 row 6; 02-map-ref Step 3 item #6."""
        tag = '[#6 AGREEMENT_FEATURE rate feature]'
        feat_df, errs1 = self._get_table(ctx, 'Core_DB.FEATURE')
        af_df,   errs2 = self._get_table(ctx, 'Core_DB.AGREEMENT_FEATURE')
        if feat_df is None or af_df is None:
            return errs1 + errs2

        rate_feat_ids = set(
            feat_df[feat_df['Feature_Subtype_Cd'] == RATE_FEATURE_SUBTYPE_CD]['Feature_Id'].dropna()
        )
        if not rate_feat_ids:
            return [f"{tag} Core_DB.FEATURE: no row with Feature_Subtype_Cd='{RATE_FEATURE_SUBTYPE_CD}'"]

        # Collect loan agreement IDs from the three sub-type tables
        empty = pd.DataFrame(columns=['Agreement_Id'])
        loan_ids: Set = set()
        for sub_key in (
            'Core_DB.LOAN_TERM_AGREEMENT',
            'Core_DB.MORTGAGE_AGREEMENT',
            'Core_DB.CREDIT_CARD_AGREEMENT',
        ):
            sub_df = ctx.tables.get(sub_key, empty)
            loan_ids |= set(sub_df['Agreement_Id'].dropna())

        if not loan_ids:
            return []  # no loan agreements generated — nothing to check

        agrs_with_rate = set(
            af_df[af_df['Feature_Id'].isin(rate_feat_ids)]['Agreement_Id'].dropna()
        )
        missing = loan_ids - agrs_with_rate

        violations = [
            f"{tag} Core_DB.AGREEMENT_FEATURE: "
            f"Agreement_Id={aid} (loan type) has no Rate Feature row"
            for aid in sorted(missing)
        ]
        return self._cap(violations, tag)

    def _check_07_agreement_product_primary_role(self, ctx: GenerationContext) -> List[str]:
        """#7 — AGREEMENT_PRODUCT: every agreement has ≥1 row with Agreement_Product_Role_Cd='primary'.
        §12 row 7; 02-map-ref Step 3 item #7."""
        tag = '[#7 AGREEMENT_PRODUCT primary role]'
        agr_df, errs1 = self._get_table(ctx, 'Core_DB.AGREEMENT')
        ap_df,  errs2 = self._get_table(ctx, 'Core_DB.AGREEMENT_PRODUCT')
        if agr_df is None or ap_df is None:
            return errs1 + errs2

        all_ids     = set(agr_df['Agreement_Id'].dropna())
        primary_ids = set(
            ap_df[ap_df['Agreement_Product_Role_Cd'] == _PRIMARY_ROLE_CD]['Agreement_Id'].dropna()
        )
        missing = all_ids - primary_ids

        violations = [
            f"{tag} Core_DB.AGREEMENT_PRODUCT: "
            f"Agreement_Id={aid} has no row with Agreement_Product_Role_Cd='primary'"
            for aid in sorted(missing)
        ]
        return self._cap(violations, tag)

    def _check_08_agreement_currency_preferred(self, ctx: GenerationContext) -> List[str]:
        """#8 — AGREEMENT_CURRENCY: every agreement has ≥1 row with Currency_Use_Cd='preferred'.
        §12 row 8; 02-map-ref Step 3 item #8."""
        tag = '[#8 AGREEMENT_CURRENCY preferred]'
        agr_df, errs1 = self._get_table(ctx, 'Core_DB.AGREEMENT')
        ac_df,  errs2 = self._get_table(ctx, 'Core_DB.AGREEMENT_CURRENCY')
        if agr_df is None or ac_df is None:
            return errs1 + errs2

        all_ids      = set(agr_df['Agreement_Id'].dropna())
        preferred_ids = set(
            ac_df[ac_df['Currency_Use_Cd'] == _PREFERRED_CURRENCY_USE_CD]['Agreement_Id'].dropna()
        )
        missing = all_ids - preferred_ids

        violations = [
            f"{tag} Core_DB.AGREEMENT_CURRENCY: "
            f"Agreement_Id={aid} has 0 rows with Currency_Use_Cd='preferred' (expected ≥1)"
            for aid in sorted(missing)
        ]
        return self._cap(violations, tag)

    def _check_09_party_agreement_customer_role(self, ctx: GenerationContext) -> List[str]:
        """#9 — PARTY_AGREEMENT: every agreement has ≥1 row with Party_Agreement_Role_Cd='customer'.
        §12 row 9; 02-map-ref Step 3 item #9."""
        tag = '[#9 PARTY_AGREEMENT customer role]'
        agr_df, errs1 = self._get_table(ctx, 'Core_DB.AGREEMENT')
        pa_df,  errs2 = self._get_table(ctx, 'Core_DB.PARTY_AGREEMENT')
        if agr_df is None or pa_df is None:
            return errs1 + errs2

        all_ids      = set(agr_df['Agreement_Id'].dropna())
        customer_ids = set(
            pa_df[pa_df['Party_Agreement_Role_Cd'] == _CUSTOMER_ROLE_CD]['Agreement_Id'].dropna()
        )
        missing = all_ids - customer_ids

        violations = [
            f"{tag} Core_DB.PARTY_AGREEMENT: "
            f"Agreement_Id={aid} has no row with Party_Agreement_Role_Cd='customer'"
            for aid in sorted(missing)
        ]
        return self._cap(violations, tag)

    def _check_10_party_related_customer_of_enterprise(self, ctx: GenerationContext) -> List[str]:
        """#10 — PARTY_RELATED: every individual party has ≥1 row with
        Party_Related_Role_Cd='customer of enterprise'.
        §12 row 10; 02-map-ref Step 3 item #10."""
        tag = '[#10 PARTY_RELATED customer-of-enterprise]'
        ind_df, errs1 = self._get_table(ctx, 'Core_DB.INDIVIDUAL')
        pr_df,  errs2 = self._get_table(ctx, 'Core_DB.PARTY_RELATED')
        if ind_df is None or pr_df is None:
            return errs1 + errs2

        individual_ids  = set(ind_df['Individual_Party_Id'].dropna())
        enterprise_ids  = set(
            pr_df[pr_df['Party_Related_Role_Cd'] == _CUSTOMER_OF_ENTERPRISE_CD]['Party_Id'].dropna()
        )
        missing = individual_ids - enterprise_ids

        violations = [
            f"{tag} Core_DB.PARTY_RELATED: "
            f"Party_Id={pid} (individual) has no 'customer of enterprise' row"
            for pid in sorted(missing)
        ]
        return self._cap(violations, tag)

    def _check_11_party_agreement_borrower_for_loans(self, ctx: GenerationContext) -> List[str]:
        """#11 — PARTY_AGREEMENT: every credit agreement has ≥1 row with role='borrower'.
        Borrower row is generated when ag.is_credit=True (verified: tier9_party_agreement.py:106).
        §12 row 11; 02-map-ref Step 3 item #11."""
        tag = '[#11 PARTY_AGREEMENT borrower for loans]'
        pa_df, errs = self._get_table(ctx, 'Core_DB.PARTY_AGREEMENT')
        if pa_df is None:
            return errs

        if not ctx.agreements:
            return [f"{tag} ctx.agreements is empty — cannot verify borrower constraint"]

        credit_ids = {ag.agreement_id for ag in ctx.agreements if ag.is_credit}
        if not credit_ids:
            return []  # no credit agreements — nothing to check

        borrower_ids = set(
            pa_df[pa_df['Party_Agreement_Role_Cd'] == _BORROWER_ROLE_CD]['Agreement_Id'].dropna()
        )
        missing = credit_ids - borrower_ids

        violations = [
            f"{tag} Core_DB.PARTY_AGREEMENT: "
            f"Agreement_Id={aid} (is_credit=True) has no 'borrower' row"
            for aid in sorted(missing)
        ]
        return self._cap(violations, tag)

    def _check_12_party_agreement_customer_for_retail(self, ctx: GenerationContext) -> List[str]:
        """#12 — PARTY_AGREEMENT: retail (individually-owned) agreements have a 'customer' role row.
        §12 row 12; 02-map-ref Step 3 item #12."""
        tag = '[#12 PARTY_AGREEMENT customer for retail]'
        pa_df, errs = self._get_table(ctx, 'Core_DB.PARTY_AGREEMENT')
        if pa_df is None:
            return errs

        if not ctx.customers or not ctx.agreements:
            return [f"{tag} ctx.customers or ctx.agreements is empty — cannot verify"]

        individual_ids = {cp.party_id for cp in ctx.customers if cp.party_type == 'INDIVIDUAL'}
        retail_agr_ids = {
            ag.agreement_id for ag in ctx.agreements
            if ag.owner_party_id in individual_ids
        }
        if not retail_agr_ids:
            return []

        customer_ids = set(
            pa_df[pa_df['Party_Agreement_Role_Cd'] == _CUSTOMER_ROLE_CD]['Agreement_Id'].dropna()
        )
        missing = retail_agr_ids - customer_ids

        violations = [
            f"{tag} Core_DB.PARTY_AGREEMENT: "
            f"Agreement_Id={aid} (retail/individual-owned) has no 'customer' role row"
            for aid in sorted(missing)
        ]
        return self._cap(violations, tag)

    def _check_13_frozen_status_code_FROZEN(self, ctx: GenerationContext) -> List[str]:
        """#13 — AGREEMENT_STATUS_TYPE: row with Scheme='Frozen Status', Code='FROZEN' exists.
        §12 row 13; 02-map-ref Step 3 item #13."""
        tag = '[#13 FROZEN status code]'
        df, errs = self._get_table(ctx, 'Core_DB.AGREEMENT_STATUS_TYPE')
        if df is None:
            return errs

        mask = (
            (df['Agreement_Status_Scheme_Cd'] == FROZEN_STATUS_ROW['Agreement_Status_Scheme_Cd'])
            & (df['Agreement_Status_Cd'] == FROZEN_STATUS_ROW['Agreement_Status_Cd'])
        )
        if not mask.any():
            return [
                f"{tag} Core_DB.AGREEMENT_STATUS_TYPE: "
                f"missing row with Scheme='Frozen Status', Code='FROZEN'"
            ]
        return []

    def _check_14_organization_primary_naics_sic_gics(self, ctx: GenerationContext) -> List[str]:
        """#14 — ORGANIZATION NAICS/SIC/GICS: no org has >1 Primary_*_Ind='Yes' per standard
        (zero is acceptable; violation is two or more).
        §12 row 14; 02-map-ref Step 3 item #14."""
        tag = '[#14 ORGANIZATION primary indicator]'
        checks = [
            ('Core_DB.ORGANIZATION_NAICS', 'Organization_Party_Id', 'Primary_NAICS_Ind'),
            ('Core_DB.ORGANIZATION_SIC',   'Organization_Party_Id', 'Primary_SIC_Ind'),
            ('Core_DB.ORGANIZATION_GICS',  'Organization_Party_Id', 'Primary_GICS_Ind'),
        ]
        violations: List[str] = []
        for table_key, id_col, ind_col in checks:
            df, errs = self._get_table(ctx, table_key)
            if df is None:
                violations.extend(errs)
                continue
            yes_rows = df[df[ind_col] == _PRIMARY_IND_YES]
            counts   = yes_rows.groupby(id_col).size()
            bad      = counts[counts > 1]
            for org_id, cnt in sorted(bad.items()):
                violations.append(
                    f"{tag} {table_key}: "
                    f"Organization_Party_Id={org_id} has {cnt} rows with "
                    f"{ind_col}='Yes' (expected 0 or 1)"
                )
        return self._cap(violations, tag)

    def _check_15_campaign_status_at_least_one(self, ctx: GenerationContext) -> List[str]:
        """#15 — CAMPAIGN_STATUS: every campaign has ≥1 status row.
        §12 row 15; 02-map-ref Step 3 item #15."""
        tag = '[#15 CAMPAIGN_STATUS at-least-one]'
        cam_df, errs1 = self._get_table(ctx, 'Core_DB.CAMPAIGN')
        cs_df,  errs2 = self._get_table(ctx, 'Core_DB.CAMPAIGN_STATUS')
        if cam_df is None or cs_df is None:
            return errs1 + errs2

        all_ids      = set(cam_df['Campaign_Id'].dropna())
        status_ids   = set(cs_df['Campaign_Id'].dropna())
        missing      = all_ids - status_ids

        violations = [
            f"{tag} Core_DB.CAMPAIGN_STATUS: Campaign_Id={cid} has no CAMPAIGN_STATUS row"
            for cid in sorted(missing)
        ]
        return self._cap(violations, tag)

    def _check_16_promotion_offer_at_most_five(self, ctx: GenerationContext) -> List[str]:
        """#16 — PROMOTION_OFFER: ≤5 offers per promotion (fewer is acceptable; >5 is a violation).
        §12 row 16; 02-map-ref Step 3 item #16."""
        tag = '[#16 PROMOTION_OFFER at-most-5]'
        po_df, errs = self._get_table(ctx, 'Core_DB.PROMOTION_OFFER')
        if po_df is None:
            return errs

        counts    = po_df.groupby('Promotion_Id').size()
        violators = counts[counts > 5]

        violations = [
            f"{tag} Core_DB.PROMOTION_OFFER: Promotion_Id={pid} has {cnt} offers (max 5)"
            for pid, cnt in sorted(violators.items())
        ]
        return self._cap(violations, tag)

    def _check_17_agreement_score_profitability(self, ctx: GenerationContext) -> List[str]:
        """#17 — AGREEMENT_SCORE: every agreement has a row linked to a 'profitability' model
        (ANALYTICAL_MODEL.Model_Type_Cd='profitability').
        §12 row 17; 02-map-ref Step 3 item #17."""
        tag = '[#17 AGREEMENT_SCORE profitability]'
        agr_df, errs1 = self._get_table(ctx, 'Core_DB.AGREEMENT')
        as_df,  errs2 = self._get_table(ctx, 'Core_DB.AGREEMENT_SCORE')
        am_df,  errs3 = self._get_table(ctx, 'Core_DB.ANALYTICAL_MODEL')
        if agr_df is None or as_df is None or am_df is None:
            return errs1 + errs2 + errs3

        profit_ids = set(
            am_df[am_df['Model_Type_Cd'] == PROFITABILITY_MODEL_TYPE_CD]['Model_Id'].dropna()
        )
        if not profit_ids:
            return [
                f"{tag} Core_DB.ANALYTICAL_MODEL: "
                f"no row with Model_Type_Cd='{PROFITABILITY_MODEL_TYPE_CD}'"
            ]

        scored_agrs = set(
            as_df[as_df['Model_Id'].isin(profit_ids)]['Agreement_Id'].dropna()
        )
        all_ids = set(agr_df['Agreement_Id'].dropna())
        missing = all_ids - scored_agrs

        violations = [
            f"{tag} Core_DB.AGREEMENT_SCORE: "
            f"Agreement_Id={aid} has no profitability model score row"
            for aid in sorted(missing)
        ]
        return self._cap(violations, tag)

    def _check_18_party_score_customer_profitability(self, ctx: GenerationContext) -> List[str]:
        """#18 — PARTY_SCORE: every party has a row linked to a 'customer profitability' model
        (ANALYTICAL_MODEL.Model_Purpose_Cd='customer profitability').
        §12 row 18; 02-map-ref Step 3 item #18."""
        tag = '[#18 PARTY_SCORE customer profitability]'
        cdm_df, errs1 = self._get_table(ctx, 'CDM_DB.PARTY')
        ps_df,  errs2 = self._get_table(ctx, 'Core_DB.PARTY_SCORE')
        am_df,  errs3 = self._get_table(ctx, 'Core_DB.ANALYTICAL_MODEL')
        if cdm_df is None or ps_df is None or am_df is None:
            return errs1 + errs2 + errs3

        cp_ids = set(
            am_df[am_df['Model_Purpose_Cd'] == CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD]['Model_Id'].dropna()
        )
        if not cp_ids:
            return [
                f"{tag} Core_DB.ANALYTICAL_MODEL: "
                f"no row with Model_Purpose_Cd='{CUSTOMER_PROFITABILITY_MODEL_PURPOSE_CD}'"
            ]

        scored_parties = set(
            ps_df[ps_df['Model_Id'].isin(cp_ids)]['Party_Id'].dropna()
        )
        # Exclude reserved bank/placeholder party (not a real customer)
        all_ids = set(cdm_df['CDM_Party_Id'].dropna()) - {BANK_PARTY_ID}
        missing = all_ids - scored_parties

        violations = [
            f"{tag} Core_DB.PARTY_SCORE: "
            f"Party_Id={pid} has no customer profitability model score row"
            for pid in sorted(missing)
        ]
        return self._cap(violations, tag)

    def _check_19_iso_3166_country_subdivision_populated(
        self, ctx: GenerationContext
    ) -> List[str]:
        """#19 — ISO_3166_COUNTRY_SUBDIVISION_STANDARD: non-empty; Territory_Standard_Type_Cd
        non-null; at least one row with the ISO 3166-2 standard code.
        §12 row 19; 02-map-ref Step 3 item #19."""
        tag = '[#19 ISO_3166_COUNTRY_SUBDIVISION populated]'
        df, errs = self._get_table(ctx, 'Core_DB.ISO_3166_COUNTRY_SUBDIVISION_STANDARD')
        if df is None:
            return errs

        violations: List[str] = []
        if len(df) == 0:
            return [f"{tag} Core_DB.ISO_3166_COUNTRY_SUBDIVISION_STANDARD: table is empty"]

        null_count = int(df['Territory_Standard_Type_Cd'].isna().sum())
        if null_count > 0:
            violations.append(
                f"{tag} Core_DB.ISO_3166_COUNTRY_SUBDIVISION_STANDARD: "
                f"Territory_Standard_Type_Cd has {null_count} NULL row(s)"
            )

        has_std = (df['Territory_Standard_Type_Cd'] == TERRITORY_ISO_STANDARD_CD).any()
        if not has_std:
            violations.append(
                f"{tag} Core_DB.ISO_3166_COUNTRY_SUBDIVISION_STANDARD: "
                f"no row with Territory_Standard_Type_Cd='{TERRITORY_ISO_STANDARD_CD}'"
            )
        return violations

    def _check_20_pim_product_group_clv_hierarchy(self, ctx: GenerationContext) -> List[str]:
        """#20 — PIM_DB.PRODUCT_GROUP: exactly 1 root (type_cd=1, self-ref Parent_Group_Id)
        + exactly 8 CLV children (type_cd=2) whose Parent_Group_Id == root.
        §12 row 20; 02-map-ref Step 3 item #20."""
        tag = '[#20 PIM PRODUCT_GROUP CLV hierarchy]'
        df, errs = self._get_table(ctx, 'PIM_DB.PRODUCT_GROUP')
        if df is None:
            return errs

        # Product_Group_Type_Cd stored as Int64 in tier15_pim.py
        type_col = df['Product_Group_Type_Cd'].astype('Int64')
        id_col   = df['Product_Group_Id'].astype('Int64')
        par_col  = df['Parent_Group_Id'].astype('Int64')

        root_mask = (type_col == _PIM_ROOT_TYPE_CD) & (id_col == par_col)
        root_rows = df[root_mask]

        if len(root_rows) != 1:
            return [
                f"{tag} PIM_DB.PRODUCT_GROUP: expected 1 root row (type_cd=1, self-ref), "
                f"found {len(root_rows)}"
            ]

        root_id   = int(id_col[root_mask].iloc[0])
        child_mask = (type_col == _PIM_CLV_CHILD_TYPE_CD) & (par_col == root_id)
        child_rows = df[child_mask]

        if len(child_rows) != _PIM_CLV_CHILD_COUNT:
            return [
                f"{tag} PIM_DB.PRODUCT_GROUP: expected {_PIM_CLV_CHILD_COUNT} CLV child rows "
                f"(type_cd=2, Parent_Group_Id={root_id}), found {len(child_rows)}"
            ]
        return []

    def _check_21_frozen_status_desc_exact_match(self, ctx: GenerationContext) -> List[str]:
        """#21 — AGREEMENT_STATUS_TYPE FROZEN row's Agreement_Status_Desc = 'Frozen' exactly
        (case-sensitive). Layer 2 ACCOUNT_STATUS_DIMENSION matches on this literal.
        §12 row 21; 02-map-ref Step 3 item #21."""
        tag = '[#21 FROZEN status desc]'
        df, errs = self._get_table(ctx, 'Core_DB.AGREEMENT_STATUS_TYPE')
        if df is None:
            return errs

        mask = (
            (df['Agreement_Status_Scheme_Cd'] == FROZEN_STATUS_ROW['Agreement_Status_Scheme_Cd'])
            & (df['Agreement_Status_Cd'] == FROZEN_STATUS_ROW['Agreement_Status_Cd'])
        )
        if not mask.any():
            return [
                f"{tag} Core_DB.AGREEMENT_STATUS_TYPE: "
                f"FROZEN row not found — cannot verify desc (also fails #13)"
            ]

        expected = FROZEN_STATUS_ROW['Agreement_Status_Desc']
        actual   = str(df[mask].iloc[0]['Agreement_Status_Desc'])
        if actual != expected:
            return [
                f"{tag} Core_DB.AGREEMENT_STATUS_TYPE: "
                f"Agreement_Status_Desc='{actual}' (expected='{expected}', case-sensitive)"
            ]
        return []

    def _check_22_party_identification_ssn_passport_dl(
        self, ctx: GenerationContext
    ) -> List[str]:
        """#22 — PARTY_IDENTIFICATION: each individual has all 3 types (SSN, Driver's License,
        Passport); organizations must NOT appear in this table.
        §12 row 22; 02-map-ref Step 3 item #22."""
        tag = '[#22 PARTY_IDENTIFICATION SSN/Passport/DL]'
        pi_df,  errs1 = self._get_table(ctx, 'Core_DB.PARTY_IDENTIFICATION')
        ind_df, errs2 = self._get_table(ctx, 'Core_DB.INDIVIDUAL')
        org_df, errs3 = self._get_table(ctx, 'Core_DB.ORGANIZATION')
        if pi_df is None or ind_df is None or org_df is None:
            return errs1 + errs2 + errs3

        violations: List[str] = []

        # Check orgs do not appear
        org_ids    = set(org_df['Organization_Party_Id'].dropna())
        pi_ids     = set(pi_df['Party_Id'].dropna())
        orgs_in_pi = sorted(org_ids & pi_ids)
        for oid in orgs_in_pi[:_MAX_VIOLATIONS_PER_CHECK]:
            violations.append(
                f"{tag} Core_DB.PARTY_IDENTIFICATION: "
                f"Organization_Party_Id={oid} appears in PARTY_IDENTIFICATION (must not)"
            )
        if len(orgs_in_pi) > _MAX_VIOLATIONS_PER_CHECK:
            violations.append(
                f"{tag} ... and {len(orgs_in_pi) - _MAX_VIOLATIONS_PER_CHECK} more org violations"
            )

        # Check each individual has all 3 required types
        ind_ids      = set(ind_df['Individual_Party_Id'].dropna())
        ind_pi       = pi_df[pi_df['Party_Id'].isin(ind_ids)]
        type_by_party = ind_pi.groupby('Party_Id')['Party_Identification_Type_Cd'].apply(set)

        # Individuals with no rows at all
        ind_with_rows = set(type_by_party.index)
        no_rows = sorted(ind_ids - ind_with_rows)
        for pid in no_rows[:_MAX_VIOLATIONS_PER_CHECK]:
            violations.append(
                f"{tag} Core_DB.PARTY_IDENTIFICATION: "
                f"Party_Id={pid} (individual) has no identification rows"
            )
        if len(no_rows) > _MAX_VIOLATIONS_PER_CHECK:
            violations.append(
                f"{tag} ... and {len(no_rows) - _MAX_VIOLATIONS_PER_CHECK} more with no rows"
            )

        # Individuals missing specific types
        ind_violations: List[str] = []
        for pid in sorted(type_by_party.index):
            missing = _REQUIRED_ID_TYPES - type_by_party[pid]
            if missing:
                ind_violations.append(
                    f"{tag} Core_DB.PARTY_IDENTIFICATION: "
                    f"Party_Id={pid} (individual) missing type(s) {sorted(missing)}"
                )
        violations.extend(self._cap(ind_violations, tag))

        return violations

    # ------------------------------------------------------------------
    # FK integrity scan
    # ------------------------------------------------------------------

    def _check_fk_integrity(self, ctx: GenerationContext) -> List[str]:
        """FK integrity: for each entry in _FK_MANIFEST, child column values minus NULL must be
        a subset of parent column values.
        §12 FK; 02-map-ref Step 3 FK."""
        violations: List[str] = []
        for child_key, child_col, parent_key, parent_col in _FK_MANIFEST:
            child_df, c_errs = self._get_table(ctx, child_key)
            if child_df is None:
                violations.extend(c_errs)
                continue
            parent_df, p_errs = self._get_table(ctx, parent_key)
            if parent_df is None:
                violations.extend(p_errs)
                continue

            if child_col not in child_df.columns:
                violations.append(
                    f"[FK] {child_key}.{child_col}: column not found in DataFrame"
                )
                continue
            if parent_col not in parent_df.columns:
                violations.append(
                    f"[FK] {parent_key}.{parent_col}: column not found in DataFrame"
                )
                continue

            child_vals  = set(child_df[child_col].dropna())
            parent_vals = set(parent_df[parent_col].dropna())
            orphans     = child_vals - parent_vals

            if orphans:
                sample = sorted(str(v) for v in orphans)[:5]
                extra  = len(orphans) - 5 if len(orphans) > 5 else 0
                msg = (
                    f"[FK] {child_key}.{child_col} → {parent_key}.{parent_col}: "
                    f"{len(orphans)} orphan value(s), e.g. {sample}"
                    + (f" ... and {extra} more" if extra else "")
                )
                violations.append(msg)
        return violations


# ---------------------------------------------------------------------------
# deepcopy_ctx helper (used in __main__ sad-path tests)
# ---------------------------------------------------------------------------

def deepcopy_ctx(ctx: GenerationContext) -> GenerationContext:
    """Shallow-copy ctx + copy each DataFrame in tables. Fast and sufficient for tests
    that only mutate ctx.tables (not ctx.customers/agreements/addresses)."""
    shallow = dataclasses.replace(ctx)
    shallow.tables = {k: df.copy() for k, df in ctx.tables.items()}
    return shallow


# ---------------------------------------------------------------------------
# __main__ smoke test
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    import numpy as np

    sys.path.insert(0, str(Path(__file__).parent.parent))

    from config import settings
    from registry.universe import UniverseBuilder
    from generators.tier0_lookups import Tier0Lookups
    from generators.tier1_geography import Tier1Geography
    from generators.tier2_core import Tier2Core
    from generators.tier3_party_subtypes import Tier3PartySubtypes
    from generators.tier4a_individual import Tier4aIndividual
    from generators.tier4b_organization import Tier4bOrganization
    from generators.tier4c_shared import Tier4cShared
    from generators.tier5_location import Tier5Location
    from generators.tier6_links import Tier6Links
    from generators.tier7a_agreement_crosscut import Tier7aAgreementCrosscut
    from generators.tier7b_subtypes import Tier7bSubtypes
    from generators.tier8_product_hierarchy import Tier8ProductHierarchy
    from generators.tier9_party_agreement import Tier9PartyAgreement
    from generators.tier10_events import Tier10Events
    from generators.tier11_crm import Tier11CRM
    from generators.tier13_tasks import Tier13Tasks
    from generators.tier14_cdm import Tier14CDM
    from generators.tier15_pim import Tier15PIM

    def build_full_ctx_seed_42():
        rng = np.random.default_rng(settings.SEED)
        ctx = UniverseBuilder().build(settings, rng)
        for tier in [
            Tier0Lookups(), Tier1Geography(), Tier2Core(),
            Tier3PartySubtypes(), Tier4aIndividual(), Tier4bOrganization(), Tier4cShared(),
            Tier5Location(), Tier6Links(),
            Tier7aAgreementCrosscut(), Tier7bSubtypes(),
            Tier8ProductHierarchy(), Tier9PartyAgreement(), Tier10Events(),
            Tier11CRM(), Tier13Tasks(), Tier14CDM(), Tier15PIM(),
        ]:
            ctx.tables.update(tier.generate(ctx))
        return ctx

    # ── Build full context once ──────────────────────────────────────────────
    print('  Building full context (seed=42)...')
    ctx = build_full_ctx_seed_42()
    print(f'  Context built: {len(ctx.tables)} tables, '
          f'{len(ctx.customers)} customers, {len(ctx.agreements)} agreements')

    # ── [1] Happy path ───────────────────────────────────────────────────────
    errors = Validator().check_all(ctx)
    assert errors == [], (
        f'Expected no errors on clean ctx; got {len(errors)}:\n'
        + '\n'.join(errors[:10])
    )
    print('  [1] Happy-path: check_all(ctx) == [] OK')

    # ── [2] Reproducibility ──────────────────────────────────────────────────
    a = Validator().check_all(ctx)
    b = Validator().check_all(ctx)
    assert a == b, f'check_all not reproducible: {set(a) ^ set(b)}'
    print('  [2] Reproducibility: two calls return identical lists OK')

    # ── [3] Sad-path — remove all 'preferred' AGREEMENT_CURRENCY rows ────────
    ctx2 = deepcopy_ctx(ctx)
    df2 = ctx2.tables['Core_DB.AGREEMENT_CURRENCY']
    ctx2.tables['Core_DB.AGREEMENT_CURRENCY'] = df2[df2['Currency_Use_Cd'] != 'preferred']
    errors2 = Validator().check_all(ctx2)
    assert any('#8' in e and 'AGREEMENT_CURRENCY' in e for e in errors2), (
        f'Expected #8 + AGREEMENT_CURRENCY in errors; got: {errors2[:5]}'
    )
    print('  [3] Sad-path #8: removing preferred currency rows fires correct violation OK')

    # ── [4] Sad-path — delete FROZEN row ────────────────────────────────────
    ctx3 = deepcopy_ctx(ctx)
    df3 = ctx3.tables['Core_DB.AGREEMENT_STATUS_TYPE']
    ctx3.tables['Core_DB.AGREEMENT_STATUS_TYPE'] = df3[df3['Agreement_Status_Cd'] != 'FROZEN']
    errors3 = Validator().check_all(ctx3)
    assert any('#13' in e for e in errors3), f'#13 not fired: {errors3[:5]}'
    assert any('#21' in e for e in errors3), f'#21 not fired: {errors3[:5]}'
    print('  [4] Sad-path #13+#21: deleting FROZEN row fires both in same pass OK')

    # ── [5] Sad-path — drop one party's language usage rows ─────────────────
    ctx4 = deepcopy_ctx(ctx)
    df4 = ctx4.tables['Core_DB.PARTY_LANGUAGE_USAGE']
    victim = int(df4['Party_Id'].iloc[0])
    ctx4.tables['Core_DB.PARTY_LANGUAGE_USAGE'] = df4[df4['Party_Id'] != victim]
    errors4 = Validator().check_all(ctx4)
    assert any('#4' in e and str(victim) in e for e in errors4), (
        f'Expected #4 + Party_Id={victim} in errors; got: {errors4[:5]}'
    )
    print(f'  [5] Sad-path #4: dropping Party_Id={victim} language rows fires violation OK')

    # ── [6] Sad-path — remove all Passport rows ─────────────────────────────
    ctx4b = deepcopy_ctx(ctx)
    df4b = ctx4b.tables['Core_DB.PARTY_IDENTIFICATION']
    ctx4b.tables['Core_DB.PARTY_IDENTIFICATION'] = df4b[
        df4b['Party_Identification_Type_Cd'] != 'Passport'
    ]
    errors4b = Validator().check_all(ctx4b)
    assert any('#22' in e and 'Passport' in e for e in errors4b), (
        f'Expected #22 + Passport in errors; got: {errors4b[:5]}'
    )
    print('  [6] Sad-path #22: removing Passport rows fires violation naming Passport OK')

    # ── [7] Sad-path — orphan Agreement_Id in PARTY_AGREEMENT ───────────────
    ctx6 = deepcopy_ctx(ctx)
    df6 = ctx6.tables['Core_DB.PARTY_AGREEMENT'].copy()
    df6.loc[len(df6)] = df6.iloc[0].copy()
    df6.loc[len(df6) - 1, 'Agreement_Id'] = 999_999_999_999
    ctx6.tables['Core_DB.PARTY_AGREEMENT'] = df6
    errors6 = Validator().check_all(ctx6)
    assert any('PARTY_AGREEMENT' in e and 'Agreement_Id' in e for e in errors6), (
        f'Expected PARTY_AGREEMENT + Agreement_Id in errors; got: {errors6[:5]}'
    )
    print('  [7] Sad-path FK: orphan Agreement_Id in PARTY_AGREEMENT detected OK')

    # ── [8] Missing table → "missing" violation, no KeyError ─────────────────
    ctx7 = deepcopy_ctx(ctx)
    del ctx7.tables['Core_DB.AGREEMENT_CURRENCY']
    errors7 = Validator().check_all(ctx7)
    assert any('AGREEMENT_CURRENCY' in e and 'missing' in e.lower() for e in errors7), (
        f'Expected missing-table error for AGREEMENT_CURRENCY; got: {errors7[:5]}'
    )
    print('  [8] Missing table produces "missing" violation, no KeyError OK')

    # ── [9] SKIPPED_TABLES not in ctx.tables; happy path still passes ────────
    from config.settings import SKIPPED_TABLES as _ST
    for k in _ST:
        assert k not in ctx.tables, f'Skipped table {k} should not be in ctx.tables'
    assert Validator().check_all(ctx) == [], 'SKIPPED_TABLES check broke happy path'
    print('  [9] SKIPPED_TABLES absent from ctx.tables; happy path unaffected OK')

    # ── [10] Violation string quality + per-check cap ────────────────────────
    ctx5 = deepcopy_ctx(ctx)
    ctx5.tables['Core_DB.AGREEMENT_CURRENCY'] = (
        ctx5.tables['Core_DB.AGREEMENT_CURRENCY'].iloc[0:0]
    )
    errors5 = Validator().check_all(ctx5)
    check8 = [e for e in errors5 if '#8' in e]
    assert len(check8) <= 10, f'#8 emitted {len(check8)} strings (cap is 10)'
    for e in errors5:
        assert any(tok in e for tok in ('#', 'Id=', 'DB.')), f'unhelpful error string: {e!r}'
    print(f'  [10] Violation string quality OK; #8 cap honoured ({len(check8)} strings <=10)')

    print('output/validator.py OK')
