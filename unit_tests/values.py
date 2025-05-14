#some very simplified parameter values for testing

ANGLE = 1

class Land_values:
    land_cover_type_speeds = {
        "grass": 12,
        "forest": 5,
        "wetland":4
    }

class Transport_values:
    #what weisse uses as his global averages
    country_road_values_glob_avg = {
        "motorway": 100,
        "primary": 50
    }

    #value used by wiess
    railspeed = 20
