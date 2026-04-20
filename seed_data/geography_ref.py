from typing import Dict, List

# ── COUNTRIES ──
# Each entry: {name, iso_alpha_2, iso_alpha_3, iso_numeric_3, calendar_type_cd}
# iso_numeric_3: official ISO 3166-1 numeric, zero-padded to 3 chars.
_COUNTRIES: List[Dict] = [
    {'name': 'United States',    'iso_alpha_2': 'US', 'iso_alpha_3': 'USA', 'iso_numeric_3': '840', 'calendar_type_cd': 'GREGORIAN'},
    {'name': 'Canada',           'iso_alpha_2': 'CA', 'iso_alpha_3': 'CAN', 'iso_numeric_3': '124', 'calendar_type_cd': 'GREGORIAN'},
    {'name': 'United Kingdom',   'iso_alpha_2': 'GB', 'iso_alpha_3': 'GBR', 'iso_numeric_3': '826', 'calendar_type_cd': 'GREGORIAN'},
    {'name': 'Germany',          'iso_alpha_2': 'DE', 'iso_alpha_3': 'DEU', 'iso_numeric_3': '276', 'calendar_type_cd': 'GREGORIAN'},
    {'name': 'France',           'iso_alpha_2': 'FR', 'iso_alpha_3': 'FRA', 'iso_numeric_3': '250', 'calendar_type_cd': 'GREGORIAN'},
    {'name': 'Japan',            'iso_alpha_2': 'JP', 'iso_alpha_3': 'JPN', 'iso_numeric_3': '392', 'calendar_type_cd': 'GREGORIAN'},
    {'name': 'Australia',        'iso_alpha_2': 'AU', 'iso_alpha_3': 'AUS', 'iso_numeric_3': '036', 'calendar_type_cd': 'GREGORIAN'},
    {'name': 'Mexico',           'iso_alpha_2': 'MX', 'iso_alpha_3': 'MEX', 'iso_numeric_3': '484', 'calendar_type_cd': 'GREGORIAN'},
    {'name': 'Brazil',           'iso_alpha_2': 'BR', 'iso_alpha_3': 'BRA', 'iso_numeric_3': '076', 'calendar_type_cd': 'GREGORIAN'},
    {'name': 'China',            'iso_alpha_2': 'CN', 'iso_alpha_3': 'CHN', 'iso_numeric_3': '156', 'calendar_type_cd': 'GREGORIAN'},
    {'name': 'India',            'iso_alpha_2': 'IN', 'iso_alpha_3': 'IND', 'iso_numeric_3': '356', 'calendar_type_cd': 'GREGORIAN'},
    {'name': 'Spain',            'iso_alpha_2': 'ES', 'iso_alpha_3': 'ESP', 'iso_numeric_3': '724', 'calendar_type_cd': 'GREGORIAN'},
    {'name': 'Italy',            'iso_alpha_2': 'IT', 'iso_alpha_3': 'ITA', 'iso_numeric_3': '380', 'calendar_type_cd': 'GREGORIAN'},
    {'name': 'Netherlands',      'iso_alpha_2': 'NL', 'iso_alpha_3': 'NLD', 'iso_numeric_3': '528', 'calendar_type_cd': 'GREGORIAN'},
    {'name': 'Switzerland',      'iso_alpha_2': 'CH', 'iso_alpha_3': 'CHE', 'iso_numeric_3': '756', 'calendar_type_cd': 'GREGORIAN'},
    {'name': 'Sweden',           'iso_alpha_2': 'SE', 'iso_alpha_3': 'SWE', 'iso_numeric_3': '752', 'calendar_type_cd': 'GREGORIAN'},
    {'name': 'Ireland',          'iso_alpha_2': 'IE', 'iso_alpha_3': 'IRL', 'iso_numeric_3': '372', 'calendar_type_cd': 'GREGORIAN'},
    {'name': 'Singapore',        'iso_alpha_2': 'SG', 'iso_alpha_3': 'SGP', 'iso_numeric_3': '702', 'calendar_type_cd': 'GREGORIAN'},
    {'name': 'South Africa',     'iso_alpha_2': 'ZA', 'iso_alpha_3': 'ZAF', 'iso_numeric_3': '710', 'calendar_type_cd': 'GREGORIAN'},
    {'name': 'Norway',           'iso_alpha_2': 'NO', 'iso_alpha_3': 'NOR', 'iso_numeric_3': '578', 'calendar_type_cd': 'GREGORIAN'},
]

# ── US STATES + DC ──
# Each entry: {name, usps_2, iso_subdivision_3}
# iso_subdivision_3: USPS 2-letter code right-padded to 3 chars (satisfies CHAR(3) DDL).
_US_STATES: List[Dict] = [
    {'name': 'Alabama',              'usps_2': 'AL', 'iso_subdivision_3': 'AL '},
    {'name': 'Alaska',               'usps_2': 'AK', 'iso_subdivision_3': 'AK '},
    {'name': 'Arizona',              'usps_2': 'AZ', 'iso_subdivision_3': 'AZ '},
    {'name': 'Arkansas',             'usps_2': 'AR', 'iso_subdivision_3': 'AR '},
    {'name': 'California',           'usps_2': 'CA', 'iso_subdivision_3': 'CA '},
    {'name': 'Colorado',             'usps_2': 'CO', 'iso_subdivision_3': 'CO '},
    {'name': 'Connecticut',          'usps_2': 'CT', 'iso_subdivision_3': 'CT '},
    {'name': 'Delaware',             'usps_2': 'DE', 'iso_subdivision_3': 'DE '},
    {'name': 'District of Columbia', 'usps_2': 'DC', 'iso_subdivision_3': 'DC '},
    {'name': 'Florida',              'usps_2': 'FL', 'iso_subdivision_3': 'FL '},
    {'name': 'Georgia',              'usps_2': 'GA', 'iso_subdivision_3': 'GA '},
    {'name': 'Hawaii',               'usps_2': 'HI', 'iso_subdivision_3': 'HI '},
    {'name': 'Idaho',                'usps_2': 'ID', 'iso_subdivision_3': 'ID '},
    {'name': 'Illinois',             'usps_2': 'IL', 'iso_subdivision_3': 'IL '},
    {'name': 'Indiana',              'usps_2': 'IN', 'iso_subdivision_3': 'IN '},
    {'name': 'Iowa',                 'usps_2': 'IA', 'iso_subdivision_3': 'IA '},
    {'name': 'Kansas',               'usps_2': 'KS', 'iso_subdivision_3': 'KS '},
    {'name': 'Kentucky',             'usps_2': 'KY', 'iso_subdivision_3': 'KY '},
    {'name': 'Louisiana',            'usps_2': 'LA', 'iso_subdivision_3': 'LA '},
    {'name': 'Maine',                'usps_2': 'ME', 'iso_subdivision_3': 'ME '},
    {'name': 'Maryland',             'usps_2': 'MD', 'iso_subdivision_3': 'MD '},
    {'name': 'Massachusetts',        'usps_2': 'MA', 'iso_subdivision_3': 'MA '},
    {'name': 'Michigan',             'usps_2': 'MI', 'iso_subdivision_3': 'MI '},
    {'name': 'Minnesota',            'usps_2': 'MN', 'iso_subdivision_3': 'MN '},
    {'name': 'Mississippi',          'usps_2': 'MS', 'iso_subdivision_3': 'MS '},
    {'name': 'Missouri',             'usps_2': 'MO', 'iso_subdivision_3': 'MO '},
    {'name': 'Montana',              'usps_2': 'MT', 'iso_subdivision_3': 'MT '},
    {'name': 'Nebraska',             'usps_2': 'NE', 'iso_subdivision_3': 'NE '},
    {'name': 'Nevada',               'usps_2': 'NV', 'iso_subdivision_3': 'NV '},
    {'name': 'New Hampshire',        'usps_2': 'NH', 'iso_subdivision_3': 'NH '},
    {'name': 'New Jersey',           'usps_2': 'NJ', 'iso_subdivision_3': 'NJ '},
    {'name': 'New Mexico',           'usps_2': 'NM', 'iso_subdivision_3': 'NM '},
    {'name': 'New York',             'usps_2': 'NY', 'iso_subdivision_3': 'NY '},
    {'name': 'North Carolina',       'usps_2': 'NC', 'iso_subdivision_3': 'NC '},
    {'name': 'North Dakota',         'usps_2': 'ND', 'iso_subdivision_3': 'ND '},
    {'name': 'Ohio',                 'usps_2': 'OH', 'iso_subdivision_3': 'OH '},
    {'name': 'Oklahoma',             'usps_2': 'OK', 'iso_subdivision_3': 'OK '},
    {'name': 'Oregon',               'usps_2': 'OR', 'iso_subdivision_3': 'OR '},
    {'name': 'Pennsylvania',         'usps_2': 'PA', 'iso_subdivision_3': 'PA '},
    {'name': 'Rhode Island',         'usps_2': 'RI', 'iso_subdivision_3': 'RI '},
    {'name': 'South Carolina',       'usps_2': 'SC', 'iso_subdivision_3': 'SC '},
    {'name': 'South Dakota',         'usps_2': 'SD', 'iso_subdivision_3': 'SD '},
    {'name': 'Tennessee',            'usps_2': 'TN', 'iso_subdivision_3': 'TN '},
    {'name': 'Texas',                'usps_2': 'TX', 'iso_subdivision_3': 'TX '},
    {'name': 'Utah',                 'usps_2': 'UT', 'iso_subdivision_3': 'UT '},
    {'name': 'Vermont',              'usps_2': 'VT', 'iso_subdivision_3': 'VT '},
    {'name': 'Virginia',             'usps_2': 'VA', 'iso_subdivision_3': 'VA '},
    {'name': 'Washington',           'usps_2': 'WA', 'iso_subdivision_3': 'WA '},
    {'name': 'West Virginia',        'usps_2': 'WV', 'iso_subdivision_3': 'WV '},
    {'name': 'Wisconsin',            'usps_2': 'WI', 'iso_subdivision_3': 'WI '},
    {'name': 'Wyoming',              'usps_2': 'WY', 'iso_subdivision_3': 'WY '},
]

# ── FOREIGN TERRITORIES ──
# Each entry: {name, country_iso_alpha_3, territory_type_cd}
# These appear in TERRITORY but NOT in ISO_3166_COUNTRY_SUBDIVISION_STANDARD.
_FOREIGN_TERRITORIES: List[Dict] = [
    {'name': 'Ontario',          'country_iso_alpha_3': 'CAN', 'territory_type_cd': 'PROVINCE'},
    {'name': 'Quebec',           'country_iso_alpha_3': 'CAN', 'territory_type_cd': 'PROVINCE'},
    {'name': 'British Columbia', 'country_iso_alpha_3': 'CAN', 'territory_type_cd': 'PROVINCE'},
    {'name': 'England',          'country_iso_alpha_3': 'GBR', 'territory_type_cd': 'COUNTRY_SUBDIVISION'},
    {'name': 'Scotland',         'country_iso_alpha_3': 'GBR', 'territory_type_cd': 'COUNTRY_SUBDIVISION'},
    {'name': 'Bavaria',          'country_iso_alpha_3': 'DEU', 'territory_type_cd': 'COUNTRY_SUBDIVISION'},
    {'name': 'Berlin',           'country_iso_alpha_3': 'DEU', 'territory_type_cd': 'COUNTRY_SUBDIVISION'},
    {'name': 'Ile-de-France',    'country_iso_alpha_3': 'FRA', 'territory_type_cd': 'COUNTRY_SUBDIVISION'},
    {'name': 'Maharashtra',      'country_iso_alpha_3': 'IND', 'territory_type_cd': 'COUNTRY_SUBDIVISION'},
    {'name': 'New South Wales',  'country_iso_alpha_3': 'AUS', 'territory_type_cd': 'COUNTRY_SUBDIVISION'},
    {'name': 'Tokyo',            'country_iso_alpha_3': 'JPN', 'territory_type_cd': 'COUNTRY_SUBDIVISION'},
]

# ── CITIES ──
# Each entry: {name, state_usps_2, country_iso_alpha_3, city_type_cd,
#              postal_codes, time_zone_cd, territory_name}
# For US cities: state_usps_2 is set, territory_name is None.
# For international cities: state_usps_2 is None, territory_name matches a name
#   in _FOREIGN_TERRITORIES.
_CITIES: List[Dict] = [
    # ── California ──
    {'name': 'Los Angeles',      'state_usps_2': 'CA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['90001', '90012', '90028'], 'time_zone_cd': 'PT',  'territory_name': None},
    {'name': 'San Francisco',    'state_usps_2': 'CA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['94102', '94107', '94115'], 'time_zone_cd': 'PT',  'territory_name': None},
    {'name': 'San Diego',        'state_usps_2': 'CA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['92101', '92103'],          'time_zone_cd': 'PT',  'territory_name': None},
    {'name': 'San Jose',         'state_usps_2': 'CA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['95101', '95112'],          'time_zone_cd': 'PT',  'territory_name': None},
    {'name': 'Sacramento',       'state_usps_2': 'CA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['95814', '95821'],          'time_zone_cd': 'PT',  'territory_name': None},
    # ── New York ──
    {'name': 'New York City',    'state_usps_2': 'NY', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['10001', '10016', '10025'], 'time_zone_cd': 'ET',  'territory_name': None},
    {'name': 'Buffalo',          'state_usps_2': 'NY', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['14201', '14202'],          'time_zone_cd': 'ET',  'territory_name': None},
    {'name': 'Albany',           'state_usps_2': 'NY', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['12201', '12206'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── Texas ──
    {'name': 'Houston',          'state_usps_2': 'TX', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['77001', '77002', '77019'], 'time_zone_cd': 'CT',  'territory_name': None},
    {'name': 'Dallas',           'state_usps_2': 'TX', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['75201', '75202', '75204'], 'time_zone_cd': 'CT',  'territory_name': None},
    {'name': 'Austin',           'state_usps_2': 'TX', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['78701', '78702'],          'time_zone_cd': 'CT',  'territory_name': None},
    {'name': 'San Antonio',      'state_usps_2': 'TX', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['78201', '78202'],          'time_zone_cd': 'CT',  'territory_name': None},
    # ── Florida ──
    {'name': 'Miami',            'state_usps_2': 'FL', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['33101', '33125', '33130'], 'time_zone_cd': 'ET',  'territory_name': None},
    {'name': 'Orlando',          'state_usps_2': 'FL', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['32801', '32803'],          'time_zone_cd': 'ET',  'territory_name': None},
    {'name': 'Tampa',            'state_usps_2': 'FL', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['33601', '33602'],          'time_zone_cd': 'ET',  'territory_name': None},
    {'name': 'Jacksonville',     'state_usps_2': 'FL', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['32099', '32202'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── Illinois ──
    {'name': 'Chicago',          'state_usps_2': 'IL', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['60601', '60607', '60614'], 'time_zone_cd': 'CT',  'territory_name': None},
    {'name': 'Springfield',      'state_usps_2': 'IL', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['62701', '62702'],          'time_zone_cd': 'CT',  'territory_name': None},
    # ── Pennsylvania ──
    {'name': 'Philadelphia',     'state_usps_2': 'PA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['19101', '19103', '19107'], 'time_zone_cd': 'ET',  'territory_name': None},
    {'name': 'Pittsburgh',       'state_usps_2': 'PA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['15201', '15203'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── Ohio ──
    {'name': 'Columbus',         'state_usps_2': 'OH', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['43201', '43202'],          'time_zone_cd': 'ET',  'territory_name': None},
    {'name': 'Cleveland',        'state_usps_2': 'OH', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['44101', '44102'],          'time_zone_cd': 'ET',  'territory_name': None},
    {'name': 'Cincinnati',       'state_usps_2': 'OH', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['45201', '45202'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── Georgia ──
    {'name': 'Atlanta',          'state_usps_2': 'GA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['30301', '30303', '30308'], 'time_zone_cd': 'ET',  'territory_name': None},
    # ── North Carolina ──
    {'name': 'Charlotte',        'state_usps_2': 'NC', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['28201', '28202'],          'time_zone_cd': 'ET',  'territory_name': None},
    {'name': 'Raleigh',          'state_usps_2': 'NC', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['27601', '27602'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── Michigan ──
    {'name': 'Detroit',          'state_usps_2': 'MI', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['48201', '48202'],          'time_zone_cd': 'ET',  'territory_name': None},
    {'name': 'Grand Rapids',     'state_usps_2': 'MI', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['49501', '49503'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── Arizona ──
    {'name': 'Phoenix',          'state_usps_2': 'AZ', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['85001', '85004', '85012'], 'time_zone_cd': 'MT',  'territory_name': None},
    {'name': 'Tucson',           'state_usps_2': 'AZ', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['85701', '85702'],          'time_zone_cd': 'MT',  'territory_name': None},
    # ── Colorado ──
    {'name': 'Denver',           'state_usps_2': 'CO', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['80201', '80202', '80203'], 'time_zone_cd': 'MT',  'territory_name': None},
    {'name': 'Colorado Springs', 'state_usps_2': 'CO', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['80901', '80903'],          'time_zone_cd': 'MT',  'territory_name': None},
    # ── Washington ──
    {'name': 'Seattle',          'state_usps_2': 'WA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['98101', '98102', '98104'], 'time_zone_cd': 'PT',  'territory_name': None},
    {'name': 'Spokane',          'state_usps_2': 'WA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['99201', '99202'],          'time_zone_cd': 'PT',  'territory_name': None},
    # ── Oregon ──
    {'name': 'Portland',         'state_usps_2': 'OR', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['97201', '97202', '97209'], 'time_zone_cd': 'PT',  'territory_name': None},
    # ── Massachusetts ──
    {'name': 'Boston',           'state_usps_2': 'MA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['02101', '02108', '02115'], 'time_zone_cd': 'ET',  'territory_name': None},
    {'name': 'Worcester',        'state_usps_2': 'MA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['01601', '01602'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── Virginia ──
    {'name': 'Virginia Beach',   'state_usps_2': 'VA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['23450', '23451'],          'time_zone_cd': 'ET',  'territory_name': None},
    {'name': 'Richmond',         'state_usps_2': 'VA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['23218', '23219'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── Minnesota ──
    {'name': 'Minneapolis',      'state_usps_2': 'MN', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['55401', '55402', '55403'], 'time_zone_cd': 'CT',  'territory_name': None},
    # ── Missouri ──
    {'name': 'Kansas City',      'state_usps_2': 'MO', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['64101', '64105'],          'time_zone_cd': 'CT',  'territory_name': None},
    {'name': 'St. Louis',        'state_usps_2': 'MO', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['63101', '63103'],          'time_zone_cd': 'CT',  'territory_name': None},
    # ── Indiana ──
    {'name': 'Indianapolis',     'state_usps_2': 'IN', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['46201', '46202'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── Tennessee ──
    {'name': 'Nashville',        'state_usps_2': 'TN', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['37201', '37203'],          'time_zone_cd': 'CT',  'territory_name': None},
    {'name': 'Memphis',          'state_usps_2': 'TN', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['38101', '38103'],          'time_zone_cd': 'CT',  'territory_name': None},
    # ── Nevada ──
    {'name': 'Las Vegas',        'state_usps_2': 'NV', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['89101', '89102', '89109'], 'time_zone_cd': 'PT',  'territory_name': None},
    {'name': 'Reno',             'state_usps_2': 'NV', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['89501', '89502'],          'time_zone_cd': 'PT',  'territory_name': None},
    # ── Wisconsin ──
    {'name': 'Milwaukee',        'state_usps_2': 'WI', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['53201', '53202'],          'time_zone_cd': 'CT',  'territory_name': None},
    # ── Maryland ──
    {'name': 'Baltimore',        'state_usps_2': 'MD', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['21201', '21202'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── Connecticut ──
    {'name': 'Hartford',         'state_usps_2': 'CT', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['06101', '06103'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── Louisiana ──
    {'name': 'New Orleans',      'state_usps_2': 'LA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['70112', '70113'],          'time_zone_cd': 'CT',  'territory_name': None},
    # ── Kentucky ──
    {'name': 'Louisville',       'state_usps_2': 'KY', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['40201', '40202'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── Oklahoma ──
    {'name': 'Oklahoma City',    'state_usps_2': 'OK', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['73101', '73102'],          'time_zone_cd': 'CT',  'territory_name': None},
    # ── New Jersey ──
    {'name': 'Newark',           'state_usps_2': 'NJ', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['07101', '07102'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── Nebraska ──
    {'name': 'Omaha',            'state_usps_2': 'NE', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['68101', '68102'],          'time_zone_cd': 'CT',  'territory_name': None},
    # ── New Mexico ──
    {'name': 'Albuquerque',      'state_usps_2': 'NM', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['87101', '87102'],          'time_zone_cd': 'MT',  'territory_name': None},
    # ── Utah ──
    {'name': 'Salt Lake City',   'state_usps_2': 'UT', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['84101', '84102'],          'time_zone_cd': 'MT',  'territory_name': None},
    # ── Hawaii ──
    {'name': 'Honolulu',         'state_usps_2': 'HI', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['96801', '96813'],          'time_zone_cd': None,  'territory_name': None},
    # ── Alaska ──
    {'name': 'Anchorage',        'state_usps_2': 'AK', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['99501', '99502'],          'time_zone_cd': None,  'territory_name': None},
    # ── Idaho ──
    {'name': 'Boise',            'state_usps_2': 'ID', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['83701', '83702'],          'time_zone_cd': 'MT',  'territory_name': None},
    # ── Iowa ──
    {'name': 'Des Moines',       'state_usps_2': 'IA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['50301', '50309'],          'time_zone_cd': 'CT',  'territory_name': None},
    # ── Kansas ──
    {'name': 'Wichita',          'state_usps_2': 'KS', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['67201', '67202'],          'time_zone_cd': 'CT',  'territory_name': None},
    # ── Arkansas ──
    {'name': 'Little Rock',      'state_usps_2': 'AR', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['72201', '72202'],          'time_zone_cd': 'CT',  'territory_name': None},
    # ── South Carolina ──
    {'name': 'Columbia',         'state_usps_2': 'SC', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['29201', '29202'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── Mississippi ──
    {'name': 'Jackson',          'state_usps_2': 'MS', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['39201', '39202'],          'time_zone_cd': 'CT',  'territory_name': None},
    # ── Alabama ──
    {'name': 'Birmingham',       'state_usps_2': 'AL', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['35203', '35205'],          'time_zone_cd': 'CT',  'territory_name': None},
    {'name': 'Montgomery',       'state_usps_2': 'AL', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['36101', '36104'],          'time_zone_cd': 'CT',  'territory_name': None},
    # ── Delaware ──
    {'name': 'Wilmington',       'state_usps_2': 'DE', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['19801', '19802'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── Maine ──
    {'name': 'Portland',         'state_usps_2': 'ME', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['04101', '04102'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── Montana ──
    {'name': 'Billings',         'state_usps_2': 'MT', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['59101', '59102'],          'time_zone_cd': 'MT',  'territory_name': None},
    # ── New Hampshire ──
    {'name': 'Manchester',       'state_usps_2': 'NH', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['03101', '03102'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── North Dakota ──
    {'name': 'Fargo',            'state_usps_2': 'ND', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['58102', '58103'],          'time_zone_cd': 'CT',  'territory_name': None},
    # ── Rhode Island ──
    {'name': 'Providence',       'state_usps_2': 'RI', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['02901', '02903'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── South Dakota ──
    {'name': 'Sioux Falls',      'state_usps_2': 'SD', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['57101', '57103'],          'time_zone_cd': 'CT',  'territory_name': None},
    # ── Vermont ──
    {'name': 'Burlington',       'state_usps_2': 'VT', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['05401', '05402'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── West Virginia ──
    {'name': 'Charleston',       'state_usps_2': 'WV', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['25301', '25302'],          'time_zone_cd': 'ET',  'territory_name': None},
    # ── Wyoming ──
    {'name': 'Cheyenne',         'state_usps_2': 'WY', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['82001', '82009'],          'time_zone_cd': 'MT',  'territory_name': None},
    # ── Additional cities for coverage ──
    {'name': 'Fresno',           'state_usps_2': 'CA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['93701', '93702'],          'time_zone_cd': 'PT',  'territory_name': None},
    {'name': 'Oakland',          'state_usps_2': 'CA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['94601', '94607'],          'time_zone_cd': 'PT',  'territory_name': None},
    {'name': 'Fort Worth',       'state_usps_2': 'TX', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['76101', '76102'],          'time_zone_cd': 'CT',  'territory_name': None},
    {'name': 'El Paso',          'state_usps_2': 'TX', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['79901', '79902'],          'time_zone_cd': 'MT',  'territory_name': None},
    {'name': 'Fort Lauderdale',  'state_usps_2': 'FL', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['33301', '33304'],          'time_zone_cd': 'ET',  'territory_name': None},
    {'name': 'Aurora',           'state_usps_2': 'CO', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['80010', '80012'],          'time_zone_cd': 'MT',  'territory_name': None},
    {'name': 'Tacoma',           'state_usps_2': 'WA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['98401', '98402'],          'time_zone_cd': 'PT',  'territory_name': None},
    {'name': 'St. Paul',         'state_usps_2': 'MN', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['55101', '55102'],          'time_zone_cd': 'CT',  'territory_name': None},
    {'name': 'Lexington',        'state_usps_2': 'KY', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['40501', '40502'],          'time_zone_cd': 'ET',  'territory_name': None},
    {'name': 'Tulsa',            'state_usps_2': 'OK', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['74101', '74103'],          'time_zone_cd': 'CT',  'territory_name': None},
    {'name': 'Baton Rouge',      'state_usps_2': 'LA', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['70801', '70802'],          'time_zone_cd': 'CT',  'territory_name': None},
    {'name': 'Knoxville',        'state_usps_2': 'TN', 'country_iso_alpha_3': 'USA', 'city_type_cd': 'CITY',         'postal_codes': ['37901', '37902'],          'time_zone_cd': 'ET',  'territory_name': None},
    # International cities
    {'name': 'Toronto',          'state_usps_2': None, 'country_iso_alpha_3': 'CAN', 'city_type_cd': 'CITY',         'postal_codes': ['M5H 2N2', 'M5V 3A8'],      'time_zone_cd': None,  'territory_name': 'Ontario'},
    {'name': 'Montreal',         'state_usps_2': None, 'country_iso_alpha_3': 'CAN', 'city_type_cd': 'CITY',         'postal_codes': ['H2Y 1C6', 'H3B 4G7'],      'time_zone_cd': None,  'territory_name': 'Quebec'},
    {'name': 'Vancouver',        'state_usps_2': None, 'country_iso_alpha_3': 'CAN', 'city_type_cd': 'CITY',         'postal_codes': ['V6B 1A1', 'V6C 2B5'],      'time_zone_cd': None,  'territory_name': 'British Columbia'},
    {'name': 'London',           'state_usps_2': None, 'country_iso_alpha_3': 'GBR', 'city_type_cd': 'CITY',         'postal_codes': ['SW1A 1AA', 'EC1A 1BB'],    'time_zone_cd': None,  'territory_name': 'England'},
    {'name': 'Edinburgh',        'state_usps_2': None, 'country_iso_alpha_3': 'GBR', 'city_type_cd': 'CITY',         'postal_codes': ['EH1 1YZ', 'EH2 2AD'],      'time_zone_cd': None,  'territory_name': 'Scotland'},
    {'name': 'Munich',           'state_usps_2': None, 'country_iso_alpha_3': 'DEU', 'city_type_cd': 'CITY',         'postal_codes': ['80331', '80335'],          'time_zone_cd': None,  'territory_name': 'Bavaria'},
    {'name': 'Berlin',           'state_usps_2': None, 'country_iso_alpha_3': 'DEU', 'city_type_cd': 'CITY',         'postal_codes': ['10115', '10117'],          'time_zone_cd': None,  'territory_name': 'Berlin'},
    {'name': 'Paris',            'state_usps_2': None, 'country_iso_alpha_3': 'FRA', 'city_type_cd': 'CITY',         'postal_codes': ['75001', '75008'],          'time_zone_cd': None,  'territory_name': 'Ile-de-France'},
    {'name': 'Mumbai',           'state_usps_2': None, 'country_iso_alpha_3': 'IND', 'city_type_cd': 'MUNICIPALITY', 'postal_codes': ['400001', '400051'],        'time_zone_cd': None,  'territory_name': 'Maharashtra'},
    {'name': 'Sydney',           'state_usps_2': None, 'country_iso_alpha_3': 'AUS', 'city_type_cd': 'CITY',         'postal_codes': ['2000', '2010'],            'time_zone_cd': None,  'territory_name': 'New South Wales'},
    {'name': 'Tokyo',            'state_usps_2': None, 'country_iso_alpha_3': 'JPN', 'city_type_cd': 'MUNICIPALITY', 'postal_codes': ['100-0001', '100-0005'],    'time_zone_cd': None,  'territory_name': 'Tokyo'},
    {'name': 'Singapore City',   'state_usps_2': None, 'country_iso_alpha_3': 'SGP', 'city_type_cd': 'CITY',         'postal_codes': ['018956', '049909'],        'time_zone_cd': None,  'territory_name': None},
]

# ── COUNTIES ──
# Each entry: {name, state_usps_2}
_COUNTIES: List[Dict] = [
    {'name': 'Los Angeles County',  'state_usps_2': 'CA'},
    {'name': 'San Diego County',    'state_usps_2': 'CA'},
    {'name': 'Santa Clara County',  'state_usps_2': 'CA'},
    {'name': 'Cook County',         'state_usps_2': 'IL'},
    {'name': 'Harris County',       'state_usps_2': 'TX'},
    {'name': 'Dallas County',       'state_usps_2': 'TX'},
    {'name': 'Travis County',       'state_usps_2': 'TX'},
    {'name': 'Maricopa County',     'state_usps_2': 'AZ'},
    {'name': 'Miami-Dade County',   'state_usps_2': 'FL'},
    {'name': 'Broward County',      'state_usps_2': 'FL'},
    {'name': 'King County',         'state_usps_2': 'WA'},
    {'name': 'New York County',     'state_usps_2': 'NY'},
    {'name': 'Kings County',        'state_usps_2': 'NY'},
    {'name': 'Fulton County',       'state_usps_2': 'GA'},
    {'name': 'Cuyahoga County',     'state_usps_2': 'OH'},
    {'name': 'Franklin County',     'state_usps_2': 'OH'},
    {'name': 'Wayne County',        'state_usps_2': 'MI'},
    {'name': 'Philadelphia County', 'state_usps_2': 'PA'},
    {'name': 'Allegheny County',    'state_usps_2': 'PA'},
    {'name': 'Denver County',       'state_usps_2': 'CO'},
    {'name': 'Clark County',        'state_usps_2': 'NV'},
    {'name': 'Multnomah County',    'state_usps_2': 'OR'},
]

# ── GEOGRAPHICAL AREAS ──
# Each entry: {name, subtype_cd, short_name, desc, currency_cd, start_dt}
_GEOGRAPHICAL_AREAS: List[Dict] = [
    {
        'name': 'North America',
        'subtype_cd': 'CONTINENT',
        'short_name': 'N. America',
        'desc': 'North American continent including USA, Canada, Mexico',
        'currency_cd': 'USD',
        'start_dt': '2000-01-01',
    },
    {
        'name': 'Europe',
        'subtype_cd': 'CONTINENT',
        'short_name': 'Europe',
        'desc': 'European continent',
        'currency_cd': 'EUR',
        'start_dt': '2000-01-01',
    },
    {
        'name': 'Eurozone',
        'subtype_cd': 'ECONOMIC_ZONE',
        'short_name': 'Eurozone',
        'desc': 'European Union member states using the Euro',
        'currency_cd': 'EUR',
        'start_dt': '2000-01-01',
    },
    {
        'name': 'United Kingdom Region',
        'subtype_cd': 'TRADE_BLOC',
        'short_name': 'UK Region',
        'desc': 'United Kingdom geographic and currency region',
        'currency_cd': 'GBP',
        'start_dt': '2000-01-01',
    },
    {
        'name': 'Asia Pacific',
        'subtype_cd': 'CONTINENT',
        'short_name': 'APAC',
        'desc': 'Asia Pacific region',
        'currency_cd': 'USD',
        'start_dt': '2000-01-01',
    },
    {
        'name': 'Latin America',
        'subtype_cd': 'CONTINENT',
        'short_name': 'LATAM',
        'desc': 'Latin American region including Central and South America',
        'currency_cd': 'USD',
        'start_dt': '2000-01-01',
    },
]


def get_geography_seed_data() -> Dict[str, List[Dict]]:
    """Return static geography reference data as plain lists of dicts.

    No surrogate IDs are included — IDs are minted by Tier1Geography.generate()
    via ctx.ids. Lists are hand-authored and deterministic (no randomness).
    """
    return {
        'countries':           _COUNTRIES,
        'us_states':           _US_STATES,
        'foreign_territories': _FOREIGN_TERRITORIES,
        'cities':              _CITIES,
        'counties':            _COUNTIES,
        'geographical_areas':  _GEOGRAPHICAL_AREAS,
    }
