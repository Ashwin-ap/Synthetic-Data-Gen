from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

import numpy as np
import pandas as pd

# Project imports work when the module is loaded from the project root.
# Guarded by try/except so standalone `python registry/context.py` still loads
# (the __main__ block adds project root to sys.path before instantiating anything).
try:
    from utils.id_factory import IdFactory
    from registry.profiles import AddressRecord, AgreementProfile, CustomerProfile
except ImportError:
    pass  # types unavailable standalone; __main__ block handles this case


@dataclass
class GenerationContext:
    # Required fields (no defaults) — caller must supply both
    rng: np.random.Generator
    ids: IdFactory  # type: ignore[name-defined]

    # Populated by UniverseBuilder.build() across its _assign_* phases
    customers: List[CustomerProfile] = field(default_factory=list)  # type: ignore[name-defined]
    agreements: List[AgreementProfile] = field(default_factory=list)  # type: ignore[name-defined]
    addresses: List[AddressRecord] = field(default_factory=list)  # type: ignore[name-defined]

    # config is the config.settings module, not a class instance
    config: Any = None

    # Accumulated by tier generators; keys are 'Schema.TABLE' strings
    # e.g. 'Core_DB.AGREEMENT', 'CDM_DB.PARTY_INTERRACTION_EVENT', 'PIM_DB.PRODUCT_GROUP'
    tables: Dict[str, pd.DataFrame] = field(default_factory=dict)


if __name__ == '__main__':
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))

    import numpy as _np
    import pandas as _pd
    from utils.id_factory import IdFactory as _IdFactory
    from config.settings import ID_RANGES

    ctx = GenerationContext(rng=_np.random.default_rng(42), ids=_IdFactory(ID_RANGES))
    assert ctx.tables == {}, 'tables default must be empty dict'
    assert ctx.customers == [] and ctx.agreements == [] and ctx.addresses == []
    assert ctx.config is None

    ctx.tables['Core_DB.AGREEMENT'] = _pd.DataFrame({'Agreement_Id': [100_000]})
    ctx.tables['CDM_DB.PARTY_INTERRACTION_EVENT'] = _pd.DataFrame({'Event_Id': [50_000_000]})
    assert set(ctx.tables.keys()) == {'Core_DB.AGREEMENT', 'CDM_DB.PARTY_INTERRACTION_EVENT'}

    print('registry/context.py OK')
