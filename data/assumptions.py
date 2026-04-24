"""
BioScope Innovations — Clean Protein Certification™
Master assumptions sourced from Bioscope - TAM SAM SOM Final.xlsx
"""

TAM_TOPDOWN = {
    'global_market_2024_B': 24.2,
    'cagr_2024_2034': 0.084,
    'rapid_testing_share': 0.65,
    'outsourced_share': 0.45,
    'bioscope_niche_share': 0.55,
    'na_share_of_global': 0.38,
    'us_share_of_na': 0.87,
}

SEGMENTS = [
    {
        'key': 'retailers',
        'name': 'Tier 1 Retailers',
        'buyers': 75,
        'samples_per_buyer': 2000,
        'tier1_pct': 0.60, 'tier12_pct': 0.25, 'tier123_pct': 0.15,
        'pen_y1': 0.01, 'pen_y2': 0.03, 'pen_y3': 0.05,
        'source': 'FMI Top 75 US Supermarket List 2024; Supermarket News Top 100',
        'beachhead': False,
    },
    {
        'key': 'processors',
        'name': 'Large Food Processors',
        'buyers': 200,
        'samples_per_buyer': 5000,
        'tier1_pct': 0.70, 'tier12_pct': 0.20, 'tier123_pct': 0.10,
        'pen_y1': 0.005, 'pen_y2': 0.01, 'pen_y3': 0.03,
        'source': 'Fortune 500 filtered food/bev SIC codes; 200 companies with dedicated QA labs',
        'beachhead': False,
    },
    {
        'key': 'brands',
        'name': 'Premium / Natural Brands',
        'buyers': 1500,
        'samples_per_buyer': 500,
        'tier1_pct': 0.50, 'tier12_pct': 0.30, 'tier123_pct': 0.20,
        'pen_y1': 0.005, 'pen_y2': 0.015, 'pen_y3': 0.03,
        'source': 'SPINS Natural Channel Data; Whole Foods supplier base; premium protein segment',
        'beachhead': True,
    },
    {
        'key': 'exporters',
        'name': 'Protein Exporters',
        'buyers': 400,
        'samples_per_buyer': 1000,
        'tier1_pct': 0.90, 'tier12_pct': 0.05, 'tier123_pct': 0.05,
        'pen_y1': 0.005, 'pen_y2': 0.02, 'pen_y3': 0.05,
        'source': 'USDA FSIS Export Establishment List: 400 federally inspected establishments',
        'beachhead': False,
    },
    {
        'key': 'plants',
        'name': 'USDA Meat & Poultry Plants',
        'buyers': 6800,
        'samples_per_buyer': 200,
        'tier1_pct': 0.80, 'tier12_pct': 0.15, 'tier123_pct': 0.05,
        'pen_y1': 0.0, 'pen_y2': 0.002, 'pen_y3': 0.005,
        'source': 'USDA FSIS Plant Directory 2024: 6,800 USDA-inspected plants',
        'beachhead': False,
    },
]

PRICING = {
    'tier1':   {'label': 'Tier 1 — Residue Compliance Panel',  'price': 500,  'cogs': 100, 'gm': 0.80},
    'tier12':  {'label': 'Tier 1+2 — Residue + Welfare',       'price': 700,  'cogs': 130, 'gm': 0.8143},
    'tier123': {'label': 'Tier 1+2+3 — Full Certification',    'price': 1000, 'cogs': 140, 'gm': 0.86},
}

ANALYTES = [
    {
        'key': 'pfas', 'name': 'PFAS panel', 'tier': 1, 'comm_price': 600, 'sam_include': True,
        'usage': {'retailers': 0.50, 'processors': 0.30, 'brands': 0.40, 'exporters': 0.20, 'plants': 0.10},
        'note': 'Retailers: private label compliance. Exporters: less regulated for PFAS currently.',
    },
    {
        'key': 'vet_drugs', 'name': 'Vet drugs multi-residue', 'tier': 1, 'comm_price': 300, 'sam_include': True,
        'usage': {'retailers': 0.80, 'processors': 0.90, 'brands': 0.60, 'exporters': 0.95, 'plants': 0.70},
        'note': 'Near-universal for export compliance (EU/Japan). Retailers demand residue-free.',
    },
    {
        'key': 'pesticides', 'name': 'Pesticides MRA', 'tier': 1, 'comm_price': 515, 'sam_include': True,
        'usage': {'retailers': 0.70, 'processors': 0.60, 'brands': 0.80, 'exporters': 0.70, 'plants': 0.50},
        'note': 'Premium brands: core "clean" claim. Exporters: EU MRL compliance.',
    },
    {
        'key': 'heavy_metals', 'name': 'Heavy metals', 'tier': 1, 'comm_price': 160, 'sam_include': False,
        'usage': {'retailers': 0.60, 'processors': 0.50, 'brands': 0.60, 'exporters': 0.40, 'plants': 0.30},
        'note': 'Standard QA panel included in most Tier 1 suites.',
    },
    {
        'key': 'mycotoxins', 'name': 'Mycotoxins combo', 'tier': 1, 'comm_price': 425, 'sam_include': False,
        'usage': {'retailers': 0.30, 'processors': 0.50, 'brands': 0.30, 'exporters': 0.60, 'plants': 0.40},
        'note': 'Higher for grain/feed processors and exporters with grain inclusion.',
    },
    {
        'key': 'pahs', 'name': 'PAHs', 'tier': 1, 'comm_price': 225, 'sam_include': False,
        'usage': {'retailers': 0.20, 'processors': 0.30, 'brands': 0.20, 'exporters': 0.40, 'plants': 0.20},
        'note': 'Smoked/grilled products; export compliance markets.',
    },
    {
        'key': 'plasticizers', 'name': 'Plasticizers / BPA / Nitrosamines', 'tier': 1, 'comm_price': 275, 'sam_include': False,
        'usage': {'retailers': 0.15, 'processors': 0.25, 'brands': 0.20, 'exporters': 0.10, 'plants': 0.10},
        'note': 'Emerging concern. Growing regulatory pressure.',
    },
    {
        'key': 'stress', 'name': 'Stress biomarkers', 'tier': 2, 'comm_price': 350, 'sam_include': True,
        'usage': {'retailers': 0.25, 'processors': 0.10, 'brands': 0.50, 'exporters': 0.05, 'plants': 0.05},
        'note': 'Retailers + premium brands. Welfare claims are commercial differentiator.',
    },
    {
        'key': 'freshness', 'name': 'Freshness / K-value', 'tier': 2, 'comm_price': 200, 'sam_include': True,
        'usage': {'retailers': 0.20, 'processors': 0.30, 'brands': 0.20, 'exporters': 0.10, 'plants': 0.15},
        'note': 'Large processors: shelf-life optimization. Retailers: private label QC.',
    },
    {
        'key': 'oxidation', 'name': 'Oxidation markers', 'tier': 2, 'comm_price': 375, 'sam_include': True,
        'usage': {'retailers': 0.20, 'processors': 0.35, 'brands': 0.25, 'exporters': 0.05, 'plants': 0.10},
        'note': 'R&D and shelf-life prediction. Processors + premium brands.',
    },
    {
        'key': 'species', 'name': 'Species ID / PCR', 'tier': 3, 'comm_price': 275, 'sam_include': False,
        'usage': {'retailers': 0.15, 'processors': 0.10, 'brands': 0.30, 'exporters': 0.20, 'plants': 0.05},
        'note': 'Premium brands + retailers with fraud exposure.',
    },
    {
        'key': 'fatty_acid', 'name': 'Fatty acid / feeding system', 'tier': 3, 'comm_price': 250, 'sam_include': True,
        'usage': {'retailers': 0.10, 'processors': 0.05, 'brands': 0.40, 'exporters': 0.05, 'plants': 0.02},
        'note': 'Core for grass-fed/pasture-raised claims. Premium brands primary user.',
    },
    {
        'key': 'geo_fp', 'name': 'Geographic fingerprint', 'tier': 3, 'comm_price': 600, 'sam_include': False,
        'usage': {'retailers': 0.05, 'processors': 0.03, 'brands': 0.15, 'exporters': 0.10, 'plants': 0.01},
        'note': 'Niche; origin claims. Few commercial labs offer IRMS.',
    },
    {
        'key': 'vitamins', 'name': 'Fat-soluble vitamins', 'tier': 3, 'comm_price': 1000, 'sam_include': True,
        'usage': {'retailers': 0.05, 'processors': 0.05, 'brands': 0.10, 'exporters': 0.02, 'plants': 0.01},
        'note': 'Nutrient-density claims. Mostly premium/natural brands.',
    },
]

BM2 = {
    'annual_license_fee': 150_000,
    'per_sample_fee': 25,
    'avg_samples_per_lab': 10_000,
    'labs_y1': 0,
    'labs_y2': 2,
    'labs_y3': 7,
    'total_addressable_labs_na': 500,
}

ROB_Y5_ARR = 62_000_000

COMPETITORS = [
    {
        'name': 'Eurofins Scientific', 'type': 'Commercial Lab',
        'revenue': '$8.28B', 'funding': '$806B mkt cap',
        'segments': 'Retailers, Processors, Exporters, USDA Plants',
        'services': 'Standard residue, pathogen, nutrient testing. Per-test pricing. Multi-week turnaround.',
        'differentiation': 'BioScope: one scan, all analytes, minutes. Eurofins: separate test per analyte, 3-week TAT.',
        'speed': 1.5, 'breadth': 7.0, 'revenue_B': 8.28,
    },
    {
        'name': 'SGS SA', 'type': 'Commercial Lab',
        'revenue': '$8.35B', 'funding': '$1.17B',
        'segments': 'Large Processors, Exporters, Retailers',
        'services': 'Inspection, testing, certification across industries. Food is one segment.',
        'differentiation': 'BioScope is a food-only specialist with simultaneous multi-analyte detection. SGS is a generalist.',
        'speed': 1.5, 'breadth': 5.0, 'revenue_B': 8.35,
    },
    {
        'name': 'Neogen Corporation', 'type': 'Rapid Test Kits',
        'revenue': '$880M', 'funding': '$1.1B',
        'segments': 'USDA Plants, Processors, Retailers',
        'services': 'Rapid test kits for pathogens and food safety. One kit = one question.',
        'differentiation': 'One kit answers one question. BioScope answers hundreds simultaneously.',
        'speed': 7.0, 'breadth': 2.5, 'revenue_B': 0.88,
    },
    {
        'name': 'bioMérieux', 'type': 'Microbiology Diagnostics',
        'revenue': '$4.43B', 'funding': '$641M',
        'segments': 'Large Processors, USDA Plants, Retailers',
        'services': 'Pathogen detection (Salmonella, Listeria). Microbiology only.',
        'differentiation': 'Pathogens vs. chemicals are different problems. BioScope solves the chemical + welfare side.',
        'speed': 7.5, 'breadth': 2.0, 'revenue_B': 4.43,
    },
    {
        'name': 'Bio-Rad Laboratories', 'type': 'Life Science / Diagnostics',
        'revenue': '$2.60B', 'funding': '$2.23B',
        'segments': 'Large Processors, USDA Plants',
        'services': 'Allergen and bacteria test kits for standard food safety applications.',
        'differentiation': 'Bacteria/allergens vs. residues/welfare — entirely different problems.',
        'speed': 6.0, 'breadth': 2.5, 'revenue_B': 2.60,
    },
    {
        'name': 'Thermo Fisher Scientific', 'type': 'Analytical Instruments',
        'revenue': '$44.6B', 'funding': 'Public',
        'segments': 'Large Processors, Exporters, USDA Plants',
        'services': 'Lab instruments and MS equipment (not a testing service).',
        'differentiation': 'They sell the oven; BioScope bakes the bread. Complementary, not competing.',
        'speed': 3.0, 'breadth': 7.0, 'revenue_B': 44.6,
    },
    {
        'name': 'Agilent Technologies', 'type': 'Analytical Instruments',
        'revenue': '$7.07B', 'funding': '$4.35B',
        'segments': 'Large Processors, Exporters, USDA Plants',
        'services': 'Analytical instruments needing trained operators and hours of sample prep.',
        'differentiation': 'BioScope: zero prep, minutes. Agilent: hours of prep before you start.',
        'speed': 3.5, 'breadth': 6.0, 'revenue_B': 7.07,
    },
    {
        'name': 'Bruker Corporation', 'type': 'Analytical Instruments / MS',
        'revenue': '$3.44B', 'funding': '$1.82B',
        'segments': 'Large Processors, Exporters, Retailers',
        'services': 'Mass spectrometry instruments for food authenticity and composition.',
        'differentiation': 'Sells machines; BioScope delivers results as a service. Technically closest but different business model.',
        'speed': 4.0, 'breadth': 7.0, 'revenue_B': 3.44,
    },
    {
        'name': 'Bureau Veritas', 'type': 'Certification Body',
        'revenue': '$7.23B', 'funding': '$2.31B',
        'segments': 'Retailers, Processors, Premium Brands, Exporters',
        'services': 'Process audits and certification. Sold food chemistry labs in 2025.',
        'differentiation': 'BV checks process compliance on paper. BioScope checks the actual food leaving the facility.',
        'speed': 1.0, 'breadth': 4.0, 'revenue_B': 7.23,
    },
    {
        'name': 'Clear Labs', 'type': 'NGS / DNA Startup',
        'revenue': 'Private', 'funding': '$173.5M',
        'segments': 'Large Processors, Retailers, Premium Brands',
        'services': 'DNA-based species identification and food fraud detection.',
        'differentiation': "DNA tells you what it is. BioScope tells you if it's safe, fresh, and ethically raised.",
        'speed': 5.0, 'breadth': 3.0, 'revenue_B': 0.10,
    },
    {
        'name': 'Oritain', 'type': 'Origin Verification',
        'revenue': 'Private', 'funding': '$58.8M',
        'segments': 'Exporters, Premium Brands, Large Processors',
        'services': 'Isotope-based geographic origin verification.',
        'differentiation': 'Oritain tells you where food came from. BioScope tells you where, whether safe, and how raised — in one scan.',
        'speed': 3.0, 'breadth': 2.0, 'revenue_B': 0.05,
    },
    {
        'name': 'BioScope (Clean Protein Cert™)', 'type': 'Integrated Certification Platform',
        'revenue': 'Pre-revenue', 'funding': 'Raising',
        'segments': 'All segments',
        'services': 'DESI-MS multi-analyte scan: residues + welfare biomarkers + authenticity + origin. Minutes, not weeks.',
        'differentiation': '— Benchmark —',
        'speed': 9.5, 'breadth': 10.0, 'revenue_B': 0.0,
    },
]
