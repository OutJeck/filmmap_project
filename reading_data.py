import haversine
from opencage.geocoder import OpenCageGeocode
key = 'eb6b80413896491c882adeb4203d4aa8'
# key = 'd8cb447f8f7a4eccbdef25d14c3c69e2'
geocoder = OpenCageGeocode(key)


def find_my_coo(lat, lng):
    """
    int -> dict
    Returns the information about the place
    by using coordinates.
    """
    results = geocoder.reverse_geocode(lat, lng)
    return results


def reading_file(name_f, country, year):
    """
    file, dict, str -> lst
    Returns the information about films
    and filters its by a few parameters.
    """
    lst = []
    country = country[0]['components']['country']
    if country == 'United States of America':
        country = 'USA'
    elif country == 'United Kingdom':
        country = 'UK'

    with open(name_f, 'r') as file:
        n = 0
        for line in file:
            var_l = []
            if n >= 14:
                if line.find('{') != -1:
                    line1 = line[:line.find('{')]
                    line2 = line[line.find('}')+1:]
                    line = line1+line2
                line = line.strip().split('\t')

                if line[-1].find(country) == -1:
                    continue

                line_var = line[0].split(' (')
                if line_var[1].find(year) == -1:
                    continue
                var_l.append(line_var[0])
                var_l.append(line_var[1].replace(')', ''))
                var_l.append(''.join(line[1:]))
                lst.append(var_l)
                if len(lst) == 400:
                    break
            n += 1
    return lst


def coordinates(data):
    """
    lst -> lst
    Returns the old info of the data
    and coordinates of the specified locations.
    """
    lst = []
    for line in data:
        query = str(line[-1])
        results = geocoder.geocode(query)
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        lst.append((line[0], line[1], query,  lat, lng))
    return lst


def find_nearest(data, my_coo):
    """
    lst, dict -> lst
    Returns the distance between two locations.
    """
    lat = my_coo[0]['geometry']['lat']
    lng = my_coo[0]['geometry']['lng']
    d = dict()
    lst = []
    for i in data:
        a = (i[-2], i[-1])
        b = (lat, lng)
        distance = haversine.haversine(a, b)
        d[distance] = i

    list_keys = list(d.keys())
    list_keys.sort()
    n = 0
    for i in list_keys:
        if n == 10:
            break
        lst.append([i, d[i]])
        n += 1
    return lst
