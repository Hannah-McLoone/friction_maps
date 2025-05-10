ANGLE = 30 / 3600 # 0.008333333...

# ALL VALUES IN KM PER HOUR
class Transport_values:
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

    #value used by wiess
    railspeed = 24.3


#implement values produced from least squares optimistation !!!!
class Land_values:
    land_cover_type_speeds = {
        "barren":3.40213771,
        "crop": 3.56756849,
        "forest": 2.4068217,
        "grass": 4.65970989,
        "mangrove": 1.25192902,
        "moss": 10.67282852,
        "shrub": 4.7761381,
        "snow": 2.34761176,
        "urban": 9.30012946,
        "wetland": 1.23967645 
    }
