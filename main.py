import sys
from config.settings import SEED, TARGET_CUSTOMERS, TARGET_AGREEMENTS, OUTPUT_DIR


def main() -> None:
    print("CIF Synthetic Data Generator")
    print(f"  Seed={SEED}  Customers={TARGET_CUSTOMERS}  Agreements={TARGET_AGREEMENTS}")

    # TODO Step 4: Phase 1 — Universe Build
    # rng = np.random.default_rng(SEED)
    # universe = UniverseBuilder().build(config, rng)
    # ctx = universe.to_context(config, rng)

    # TODO Steps 6–23: Phase 2 — Tiered Writing
    # tiers = [
    #     Tier0Lookups(), Tier1Geography(), Tier2Core(),
    #     Tier3PartySubtypes(), Tier4PartyAttributes(), Tier5Location(),
    #     Tier6Links(), Tier7AgreementDetails(), Tier8ProductHierarchy(),
    #     Tier9PartyAgreement(), Tier10Events(), Tier11CRM(),
    #     Tier13Tasks(), Tier14CDM(), Tier15PIM(),
    # ]
    # for tier in tiers:
    #     new_tables = tier.generate(ctx)
    #     ctx.tables.update(new_tables)
    #     print(f"  {tier.__class__.__name__}: "
    #           f"{sum(len(df) for df in new_tables.values()):,} rows "
    #           f"across {len(new_tables)} tables")

    # TODO Step 24: Phase 3 — Validation
    # errors = Validator().check_all(ctx)
    # if errors:
    #     for e in errors:
    #         print(f"VALIDATION ERROR: {e}")
    #     sys.exit(1)

    # TODO Step 25: Phase 4 — CSV Write
    # Writer(OUTPUT_DIR).write_all(ctx.tables)
    # print(f"Done. Output in {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
