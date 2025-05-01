import math

def calculate_dew_point(temperature, humidity):
    tn = 243.12
    m = 17.62
    if temperature <= 0:
        tn = 272.62
        m = 22.46

    log_humidity = math.log(humidity / 100.0)
    ew = (m * temperature) / (tn + temperature)
    dew_point = tn * ((log_humidity + ew) / (m - log_humidity - ew))

    return dew_point


print(calculate_dew_point(-10, 30))