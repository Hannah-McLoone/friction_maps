# ASSUMES ALL VALUES IN KM PER HOUR!

class Values:

    #what weisse uses as his global averages
    country_road_values_glob_avg = {
        "motorway": 105,
        "trunk": 80,
        "railroad": 30,
        "primary": 65,
        "secondary": 60,
        "tertiary": 55,
        "unclassified": 55,
        "road": 30,
        "residential": 40,
        "service": 30,
        "track": 40,
        "pedestrian": 25,
        "unknown": 40
    }

    #what weisse uses as his uk specific values
    uk_country_road_values = {
        "motorway": 112.6538,
        "trunk": 64.3736,
        "primary": 48.2802,
        "secondary": 48.2802,
        "tertiary": 48.2802,
        "motorway_link": 112.6538,
        "primary_link": 48.2802,
        "unclassified": 48.2802,
        "road": 32.1868,
        "residential": 48.2802,
        "service": 32.1868,
        "track": 48.2802,
        "pedestrian": 32.1868,
        "unknown": 48.2802
    }


    speeds_of_features = {
        'paved': 40,           # 30 mph → 48 kph
        'asphalt': 40,         # 50 mph → 80 kph
        'unpaved': 24,         # 25 mph → 40 kph
        'gravel': 24,          # 20 mph → 32 kph
        'dirt': 24,            # 15 mph → 24 kph
        'paving_stones': 32,   # 20 mph → 32 kph
        'metal': 16,            # 10 mph → 16 kph
        'unknown':16
    }


    railspeed = 30
    #waterspeed = 20 #this is for water as a transport



class Land_values:

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
        "wetland": 4           # Slow, difficult to traverse
    }

    land_cover_type_speeds = {

        #land cover subclass - what my code has been using so far
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




ANGLE = 0.008333333333333333333