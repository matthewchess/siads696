import re
import pandas as pd
import numpy as np
from geopy.distance import geodesic

ADDRESS_ABBREVIATIONS = {
    # Directions
    'north': 'n',
    'south': 's',
    'east': 'e',
    'west': 'w',
    'northeast': 'ne',
    'northwest': 'nw',
    'southeast': 'se',
    'southwest': 'sw',

    # Street suffixes
    'street': 'st',
    'avenue': 'ave',
    'road': 'rd',
    'drive': 'dr',
    'lane': 'ln',
    'boulevard': 'blvd',
    'circle': 'cir',
    'court': 'ct',
    'place': 'pl',
    'parkway': 'pkwy',
    'highway': 'hwy',
    'trail': 'trl',
    'terrace': 'ter',
    'square': 'sq',
    'crossing': 'xing',
    'center': 'ctr',
    'centre': 'ctr',
    'point': 'pt',
    'ridge': 'rdg',
    'run': 'run',
    'view': 'vw',
    'village': 'vlg',
    'station': 'sta',
    'landing': 'lndg',
    'junction': 'jct',
    'extension': 'ext',
    'expressway': 'expy',
    'freeway': 'fwy',
    'turnpike': 'tpke',
    'causeway': 'cswy',
    'crescent': 'cres',
    'cove': 'cv',
    'fork': 'frk',
    'garden': 'gdn',
    'gardens': 'gdns',
    'grove': 'grv',
    'harbor': 'hbr',
    'harbour': 'hbr',
    'heights': 'hts',
    'hill': 'hl',
    'hills': 'hls',
    'island': 'is',
    'islands': 'iss',
    'knoll': 'knl',
    'knolls': 'knls',
    'lake': 'lk',
    'lakes': 'lks',
    'manor': 'mnr',
    'manors': 'mnrs',
    'meadow': 'mdw',
    'meadows': 'mdws',
    'mount': 'mt',
    'mountain': 'mtn',
    'orchard': 'orch',
    'pine': 'pne',
    'pines': 'pnes',
    'plaza': 'plz',
    'port': 'prt',
    'prairie': 'pr',
    'radial': 'radl',
    'river': 'riv',
    'shore': 'shr',
    'shores': 'shrs',
    'spring': 'spg',
    'springs': 'spgs',
    'summit': 'smt',
    'union': 'un',
    'valley': 'vly',
    'valleys': 'vlys',
    'well': 'wl',
    'wells': 'wls',
    
    # Unit Overrides
    'apartment': 'apt',
    'apt.': 'apt',
    'suite': 'ste',
    'ste.': 'ste',
    'unit': 'unit',
    '#': 'unit',
    'building': 'bldg',
    'floor': 'fl',
    'room': 'rm',
    'department': 'dept'
}


def standardize_address(address):
    """
    Standardizes addresses, replacing common words with 
    abbreviations for comparison accross datasets.
    """
    if pd.isna(address):
        return np.nan
    
    address = address.lower().strip()
    
    # Remove special characters
    address = re.sub(r'[^a-z0-9\s]', '', address)
    address_parts = address.split()
    
    # Update addresses using abbreviations
    cleaned_parts = [
        ADDRESS_ABBREVIATIONS.get(part, part)
        for part in address_parts
    ]
    
    return " ".join(cleaned_parts)


def remove_city_state(address, city, state):
    """
    Removes ZIP code, state, and city information from an address.
    """
    if pd.isna(address):
        return np.nan

    address = str(address)

    # Remove ZIP from address
    address = re.sub(r'\s*,?\s*\d{5}\s*$', '', address)

    # Remove State from address
    if pd.notna(state):
        address = re.sub(
            rf'\s*,?\s*{re.escape(str(state))}\s*$',
            '',
            address,
            flags=re.IGNORECASE
        )

    # Remove City from address
    if pd.notna(city):
        address = re.sub(
            rf'\s*,?\s*{re.escape(str(city))}\s*$',
            '',
            address,
            flags=re.IGNORECASE
        )

    return address.strip(' ,')


def calculate_distance(df1, df2, max_distance=0.5):
    """
    Calculates the distance between coordinates and 
    returns the closest data center index for each row.
    
    Input:
    - df1: a dataframe with lat and long columns
    - df2: a dataframe with lat and long columns
    
    Output:
    - an array of data center indexes
    """
    df1_points = list(zip(df1["lat"], df1["long"]))
    df2_points = list(zip(df2["lat"], df2["long"]))

    distances = []
    for df1_point in df1_points:
        row = []
        for df2_point in df2_points:
            row.append(geodesic(df1_point, df2_point).miles)
        distances.append(row)
        
    distances = np.array(distances)

    nearest_positions = distances.argmin(axis=1).astype(float)
    nearest_distances = distances.min(axis=1)

    # Filter by max distance
    nearest_positions[nearest_distances > max_distance] = np.nan

    return nearest_positions