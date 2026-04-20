import sys

import numpy as np

from config import settings
from config.settings import SEED, OUTPUT_DIR

from registry.universe import UniverseBuilder
from output.validator import Validator
from output.writer import Writer

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


def main() -> None:
    print("CIF Synthetic Data Generator")
    print(f"  Seed={SEED}  Customers={settings.TARGET_CUSTOMERS}  Agreements={settings.TARGET_AGREEMENTS}")

    # Phase 1 — Universe Build
    rng = np.random.default_rng(SEED)
    ctx = UniverseBuilder().build(settings, rng)

    # Phase 2 — Tiered Writing (order must match output/validator.py build_full_ctx_seed_42)
    tiers = [
        Tier0Lookups(), Tier1Geography(), Tier2Core(),
        Tier3PartySubtypes(), Tier4aIndividual(), Tier4bOrganization(), Tier4cShared(),
        Tier5Location(), Tier6Links(),
        Tier7aAgreementCrosscut(), Tier7bSubtypes(),
        Tier8ProductHierarchy(), Tier9PartyAgreement(), Tier10Events(),
        Tier11CRM(), Tier13Tasks(), Tier14CDM(), Tier15PIM(),
    ]
    for tier in tiers:
        new_tables = tier.generate(ctx)
        ctx.tables.update(new_tables)
        total_rows = sum(len(df) for df in new_tables.values())
        print(f"  {tier.__class__.__name__}: {total_rows:,} rows across {len(new_tables)} tables")

    # Phase 3 — Validation (hard gate per mvp-tool-design.md §14 Decision 6)
    errors = Validator().check_all(ctx)
    if errors:
        for e in errors:
            print(f"VALIDATION ERROR: {e}")
        sys.exit(1)

    # Phase 4 — CSV Write
    Writer(OUTPUT_DIR).write_all(ctx.tables)
    print(f"Done. Output in {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
