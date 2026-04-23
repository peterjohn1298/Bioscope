"""
BioScope market sizing calculation engine.
All functions accept optional override dicts so pages can inject scenario parameters.
"""

import copy
from data.assumptions import TAM_TOPDOWN, SEGMENTS, PRICING, ANALYTES, BM2

TIER_PRICE_KEY = {1: 'tier1', 2: 'tier12', 3: 'tier123'}


def calc_topdown(params=None):
    p = {**TAM_TOPDOWN, **(params or {})}
    g = p['global_market_2024_B']
    rapid = g * p['rapid_testing_share']
    outsourced = rapid * p['outsourced_share']
    niche = outsourced * p['bioscope_niche_share']
    na = niche * p['na_share_of_global']
    us = na * p['us_share_of_na']
    return {
        'global_market': g,
        'after_rapid': rapid,
        'after_outsourced': outsourced,
        'global_tam': niche,
        'na_tam': na,
        'us_tam': us,
        'waterfall': [
            {'label': 'Global Food Safety Testing (2024)', 'value': g},
            {'label': '× Rapid testing share (65%)',        'value': rapid},
            {'label': '× Outsourced / contract labs (45%)', 'value': outsourced},
            {'label': '× BioScope niche — residue + auth + welfare (55%)', 'value': niche},
            {'label': 'North America TAM (38% of global)',  'value': na},
            {'label': 'US TAM ★ (87% of N.Am)',            'value': us},
        ],
        'params': p,
    }


def calc_bottomup(segments=None, pricing=None, analytes=None):
    segs = segments or SEGMENTS
    prc = pricing or PRICING
    anals = analytes or ANALYTES

    t_price = {t: prc[TIER_PRICE_KEY[t]]['price'] for t in (1, 2, 3)}
    t_comm_price = {a['key']: a['comm_price'] for a in anals}

    rows = []
    for seg in segs:
        seg_key = seg['key']
        for analyte in anals:
            usage = analyte['usage'].get(seg_key, 0)
            tests = seg['buyers'] * seg['samples_per_buyer'] * usage
            comm_rev = tests * analyte['comm_price']
            bio_price = t_price[analyte['tier']]
            bio_rev = tests * bio_price

            rows.append({
                'segment_key': seg_key,
                'segment': seg['name'],
                'analyte': analyte['name'],
                'tier': analyte['tier'],
                'tests': tests,
                'comm_price': analyte['comm_price'],
                'comm_rev': comm_rev,
                'bio_price': bio_price,
                'bio_rev_100pct': bio_rev,
                'som_y1': bio_rev * seg['pen_y1'],
                'som_y2': bio_rev * seg['pen_y2'],
                'som_y3': bio_rev * seg['pen_y3'],
            })
    return rows


def segment_totals(bu_rows):
    totals = {}
    for r in bu_rows:
        k = r['segment_key']
        if k not in totals:
            totals[k] = {
                'segment': r['segment'],
                'comm_rev': 0, 'bio_rev_100pct': 0,
                'som_y1': 0, 'som_y2': 0, 'som_y3': 0,
            }
        totals[k]['comm_rev'] += r['comm_rev']
        totals[k]['bio_rev_100pct'] += r['bio_rev_100pct']
        totals[k]['som_y1'] += r['som_y1']
        totals[k]['som_y2'] += r['som_y2']
        totals[k]['som_y3'] += r['som_y3']
    return totals


def calc_som(segments=None, pricing=None, analytes=None, bm2_params=None):
    segs = segments or SEGMENTS
    prc = pricing or PRICING
    anals = analytes or ANALYTES
    bm2 = bm2_params or BM2

    bu_rows = calc_bottomup(segs, prc, anals)
    seg_tots = segment_totals(bu_rows)

    result_segs = []
    for seg in segs:
        k = seg['key']
        tot = seg_tots.get(k, {'comm_rev': 0, 'bio_rev_100pct': 0, 'som_y1': 0, 'som_y2': 0, 'som_y3': 0})

        buyers = seg['buyers']
        y1c = max(0, round(buyers * seg['pen_y1']))
        y2c = max(0, round(buyers * seg['pen_y2']))
        y3c = max(0, round(buyers * seg['pen_y3']))
        avg_rev = tot['bio_rev_100pct'] / buyers if buyers > 0 else 0

        result_segs.append({
            'key': k,
            'name': seg['name'],
            'beachhead': seg.get('beachhead', False),
            'buyers': buyers,
            'y1_customers': y1c,
            'y2_customers': y2c,
            'y3_customers': y3c,
            'avg_rev_per_customer': avg_rev,
            'som_y1': tot['som_y1'],
            'som_y2': tot['som_y2'],
            'som_y3': tot['som_y3'],
        })

    bm2_rev_per_lab = bm2['annual_license_fee'] + bm2['per_sample_fee'] * bm2['avg_samples_per_lab']
    bm2_y1 = bm2['labs_y1'] * bm2_rev_per_lab
    bm2_y2 = bm2['labs_y2'] * bm2_rev_per_lab
    bm2_y3 = bm2['labs_y3'] * bm2_rev_per_lab

    bm1_y1 = sum(s['som_y1'] for s in result_segs)
    bm1_y2 = sum(s['som_y2'] for s in result_segs)
    bm1_y3 = sum(s['som_y3'] for s in result_segs)

    return {
        'segments': result_segs,
        'bm2': {'y1': bm2_y1, 'y2': bm2_y2, 'y3': bm2_y3, 'labs_y3': bm2['labs_y3']},
        'bm1': {'y1': bm1_y1, 'y2': bm1_y2, 'y3': bm1_y3},
        'total': {
            'y1': bm1_y1 + bm2_y1,
            'y2': bm1_y2 + bm2_y2,
            'y3': bm1_y3 + bm2_y3,
        },
    }


def calc_sam(segments=None):
    """
    SAM = existing commercial lab market spend for addressable segments, scaled to N.Am.
    Uses commercial pricing (not BioScope pricing) — consistent with Excel SAM sheet col E.
    """
    segs = segments or SEGMENTS
    p = TAM_TOPDOWN

    sam_segments = []
    for seg in segs:
        us_market = 0
        for analyte in ANALYTES:
            usage = analyte['usage'].get(seg['key'], 0)
            tests = seg['buyers'] * seg['samples_per_buyer'] * usage
            us_market += tests * analyte['comm_price']  # commercial price, not BioScope price

        na_sam = us_market / p['us_share_of_na']
        sam_segments.append({
            'name': seg['name'],
            'us_market': us_market,
            'na_sam': na_sam,
        })

    total_na_sam = sum(s['na_sam'] for s in sam_segments)
    bm2_sam = BM2['total_addressable_labs_na'] * BM2['annual_license_fee']

    return {
        'segments': sam_segments,
        'total_na_sam': total_na_sam,
        'bm2_sam': bm2_sam,
        'combined_sam': total_na_sam + bm2_sam,
    }


def sensitivity_tornado(base_som_y3, n=10):
    """
    Vary each key assumption ±20% and return sorted impact on Y3 SOM.
    Returns list of dicts sorted by absolute impact descending.
    """
    results = []

    def run(seg_overrides=None, price_overrides=None, bm2_overrides=None):
        segs = copy.deepcopy(SEGMENTS)
        prc = copy.deepcopy(PRICING)
        bm2 = copy.deepcopy(BM2)

        if seg_overrides:
            for s in segs:
                if s['key'] in seg_overrides:
                    s.update(seg_overrides[s['key']])
        if price_overrides:
            for k, v in price_overrides.items():
                if k in prc:
                    prc[k]['price'] = v
        if bm2_overrides:
            bm2.update(bm2_overrides)

        return calc_som(segs, prc, None, bm2)['total']['y3']

    delta = 0.20

    # Penetration rates by segment
    for seg in SEGMENTS:
        k = seg['key']
        base_pen = seg['pen_y3']
        hi = run(seg_overrides={k: {'pen_y3': base_pen * (1 + delta)}})
        lo = run(seg_overrides={k: {'pen_y3': base_pen * (1 - delta)}})
        results.append({
            'label': f"{seg['name']} — Penetration Y3",
            'upside': hi - base_som_y3,
            'downside': lo - base_som_y3,
            'category': 'Penetration',
        })

    # Pricing
    for tier_key, tier_data in PRICING.items():
        base_price = tier_data['price']
        hi = run(price_overrides={tier_key: base_price * (1 + delta)})
        lo = run(price_overrides={tier_key: base_price * (1 - delta)})
        results.append({
            'label': f"Price — {tier_data['label']}",
            'upside': hi - base_som_y3,
            'downside': lo - base_som_y3,
            'category': 'Pricing',
        })

    # BM2 licensing ramp
    base_labs = BM2['labs_y3']
    hi = run(bm2_overrides={'labs_y3': int(base_labs * (1 + delta * 2))})
    lo = run(bm2_overrides={'labs_y3': max(0, int(base_labs * (1 - delta)))})
    results.append({
        'label': 'BM2 Licensed Labs (Y3)',
        'upside': hi - base_som_y3,
        'downside': lo - base_som_y3,
        'category': 'BM2 Licensing',
    })

    # Sort by total swing (upside - downside)
    results.sort(key=lambda x: abs(x['upside'] - x['downside']), reverse=True)
    return results[:n]


SCENARIOS = {
    'bear': {
        'label': 'Bear (Conservative)',
        'color': '#E74C3C',
        'description': 'Slower enterprise adoption, 50% of base penetration, no pricing uplift.',
        'pen_multiplier': 0.50,
        'price_multiplier': 1.00,
        'bm2_labs': {'y1': 0, 'y2': 1, 'y3': 3},
    },
    'base': {
        'label': 'Base Case',
        'color': '#3498DB',
        'description': 'Excel model assumptions — independently derived by Purdue team.',
        'pen_multiplier': 1.00,
        'price_multiplier': 1.00,
        'bm2_labs': {'y1': 0, 'y2': 2, 'y3': 7},
    },
    'bull': {
        'label': 'Bull (Optimistic)',
        'color': '#2ECC71',
        'description': 'Faster beachhead traction, 1.75× base penetration, +10% pricing.',
        'pen_multiplier': 1.75,
        'price_multiplier': 1.10,
        'bm2_labs': {'y1': 0, 'y2': 4, 'y3': 15},
    },
}


def calc_scenario(scenario_key):
    sc = SCENARIOS[scenario_key]
    segs = copy.deepcopy(SEGMENTS)
    prc = copy.deepcopy(PRICING)
    bm2 = copy.deepcopy(BM2)

    pm = sc['pen_multiplier']
    for s in segs:
        s['pen_y1'] = min(1.0, s['pen_y1'] * pm)
        s['pen_y2'] = min(1.0, s['pen_y2'] * pm)
        s['pen_y3'] = min(1.0, s['pen_y3'] * pm)

    xm = sc['price_multiplier']
    for tier in prc:
        prc[tier]['price'] = round(prc[tier]['price'] * xm)

    bm2['labs_y1'] = sc['bm2_labs']['y1']
    bm2['labs_y2'] = sc['bm2_labs']['y2']
    bm2['labs_y3'] = sc['bm2_labs']['y3']

    return calc_som(segs, prc, None, bm2)
