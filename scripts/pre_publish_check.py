#!/usr/bin/env python3
"""Static publishing checks only; does not execute model-training notebooks."""
from pathlib import Path
import json,re,sys,ast
ROOT=Path(__file__).resolve().parents[1]
EXPECTED = ['notebooks/geo_stratigraphic_fusion/07G_FORCE_legacy_geo_stratigraphic_fusion_SINGLE_NOTEBOOK_GATE_FIXED.ipynb', 'notebooks/geo_stratigraphic_fusion/07G_FORCE_legacy_geo_stratigraphic_fusion_EVIDENCE_BASELINE_RAW_SELECTION_FIXED.ipynb', 'notebooks/ablation_studies/08_FORCE_Legacy_TCN_Geo_Stacking_WITH_REUSED_FINAL_TEST.ipynb', 'notebooks/ablation_studies/08B_FORCE_Legacy_TCN_CONSTRAINED_GATE_WITH_REUSED_TEST.ipynb', 'notebooks/temporal_fusion/08C_FORCE_Legacy_TCN_NESTED_CONVEX_BLEND_WITH_REUSED_TEST_FIXED.ipynb', 'notebooks/temporal_fusion/08C_FORCE_Legacy_TCN_NESTED_CONVEX_BLEND_FULLCV_BUDGET_REPAIR.ipynb', 'notebooks/supplementary/08C_FORCE_Legacy_TCN_FINAL_TEST_LITE.ipynb']
FAILS=[]
for rel in EXPECTED:
    p=ROOT/rel
    if not p.is_file():
        FAILS.append(f"Missing notebook: {rel}")
        continue
    try:
        nb=json.loads(p.read_text(encoding='utf8'))
        assert nb['nbformat']==4
        for i,cell in enumerate(nb['cells']):
            st=''.join(cell.get('source',[]))
            if cell['cell_type']=='markdown' and re.search(r'[\u0600-\u06FF]',st):
                FAILS.append(f"Persian markdown in {rel}, cell {i}")
            if cell['cell_type']=='code':
                compile(st, f"{rel} cell {i}", 'exec')
                if 'Path.home()' in st and 'Desktop' in st:
                    FAILS.append(f"Nonportable path in {rel}, cell {i}")
        print(f"OK: {rel} | {len(nb['cells'])} cells | {sum(bool(c.get('outputs')) for c in nb['cells'])} stored-output cells")
    except Exception as e:
        FAILS.append(f"Parse/code issue in {rel}: {e}")
print('\n'+'PASS (static only)' if not FAILS else '\nFAIL\n'+'\n'.join(FAILS))
sys.exit(bool(FAILS))
