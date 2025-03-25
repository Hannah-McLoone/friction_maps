
# these are temporary paceholder values. there are more roads to be put in
# ASSUMES ALL VALUES IN KM PER HOUR!

class Values:

    country_road_values = {
        'motorway': 113,  # 70 mph → 113 kph
        'primary': 97,    # 60 mph → 97 kph
        'unclassified': None,  
        'secondary': 80,  # 50 mph → 80 kph
        'tertiary': 64,   # 40 mph → 64 kph
        'service': 32     # 20 mph → 32 kph
    }# need to add track, unknown


    speeds_of_features = {
        'paved': 48,           # 30 mph → 48 kph
        'asphalt': 50,         # 50 mph → 80 kph
        'unpaved': 24,         # 25 mph → 40 kph
        'gravel': 24,          # 20 mph → 32 kph
        'dirt': 24,            # 15 mph → 24 kph
        'paving_stones': 32,   # 20 mph → 32 kph
        'metal': 16,            # 10 mph → 16 kph
        'unknown':16
    }


    railspeed = 60
    waterspeed = 20 #this is for water as a transport



class Land_values:

    land_class_speeds = {
        "archipelago": 15,      # Moderate speed through islands
        "bare_rock": 5,         # Slow due to uneven surfaces
        "beach": 10,            # Moderate speed, soft sand can slow down
        "cave_entrance": 3,     # Slow, limited visibility and accessibility
        "cliff": 2,             # Very slow, steep and dangerous terrain
        "desert": 10,           # Moderate speed, but can vary with sand conditions
        "dune": 6,              # Slow due to soft sand
        "fell": 8,              # Moderate speed on uneven ground
        "forest": 5,            # Slow due to obstacles and dense vegetation
        "glacier": 4,           # Very slow, icy and hazardous
        "grass": 12,            # Moderate speed, generally easy to traverse
        "grassland": 15,        # Fast speed on open land
        "heath": 10,            # Moderate speed, some obstacles
        "hill": 8,              # Moderate speed, can vary with steepness
        "island": 12,           # Similar to grassland
        "islet": 12,            # Similar to grassland
        "land": 15,             # General flat land speed
        "meadow": 14,           # Fast speed, open and easy to navigate
        "mountain_range": 3,    # Very slow, rugged terrain
        "peak": 2,              # Extremely slow, steep and challenging
        "peninsula": 15,        # Similar to grassland, depends on terrain
        "reef": 8,              # Moderate speed, can be tricky
        "ridge": 5,             # Slow, uneven surfaces
        "rock": 3,              # Very slow, difficult to navigate
        "saddle": 6,            # Moderate speed, can be easier
        "sand": 5,              # Slow, loose terrain
        "scree": 4,             # Slow, loose rock can be tricky
        "scrub": 10,            # Moderate speed, some obstacles
        "shingle": 7,           # Moderate speed, pebbly terrain
        "shrub": 10,            # Moderate speed, can have some obstacles
        "shrubbery": 8,         # Moderate speed, denser than scrub
        "stone": 3,             # Very slow, difficult surfaces
        "tree": 5,              # Slow due to obstacles
        "tree_row": 6,          # Moderate speed, some spacing
        "tundra": 10,           # Moderate speed, but can vary with conditions
        "valley": 12,           # Fast speed, generally easy to navigate
        "volcano": 5,           # Slow, steep and rocky
        "wetland": 4,           # Slow, difficult to traverse
        "wood": 5                # Slow, similar to forest
    }

    land_type_speeds = {
        "desert": 10,           # Moderate speed, varies with sand conditions
        "forest": 5,            # Slow due to dense vegetation and obstacles
        "glacier": 4,           # Very slow, icy and hazardous terrain
        "grass": 12,            # Moderate speed, generally easy to traverse
        "land": 15,             # General flat land speed
        "physical": 10,         # Moderate speed, general terrain
        "reef": 8,              # Moderate speed, tricky navigation
        "rock": 3,              # Very slow, difficult surfaces
        "sand": 5,              # Slow due to loose terrain
        "shrub": 10,            # Moderate speed, some obstacles
        "tree": 5,              # Slow, due to obstacles
        "wetland": 4,           # Slow, difficult to traverse

        "barren": 12,           # Fast speed, generally open terrain
        "crop": 14,             # Fast speed, open agricultural fields
        "forest": 5,            # Slow due to dense vegetation
        "grass": 12,            # Moderate speed, easy to navigate
        "mangrove": 4,          # Slow, due to water and root systems
        "moss": 8,              # Moderate speed, can be uneven
        "shrub": 10,            # Moderate speed, some obstacles
        "snow": 3,              # Very slow, difficult to navigate
        "urban": 15,            # Moderate speed, depends on infrastructure
        "wetland": 4             # Slow, difficult to traverse
    }





class water_values:

    water = {
        'canal':1,
        'human_made':1,
        'lake':1,
        'ocean':1,
        'physical':1,
        'pond':1,
        'reservoir':1,
        'river':1,
        'water':1
    }

    raw_water_speed = 19

ANGLE = 1#0.008333333333333333333