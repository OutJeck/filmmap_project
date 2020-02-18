from reading_data import *
import folium


def creating_map(data, lat, lng):
    """
    lst, float, float -> str
    Returns the created map,
    which displays the analyzed information.
    """
    m = folium.Map(location=[lat, lng], zoom_start=12)
    tooltip = '<b>More info<b>'
    fg = folium.FeatureGroup(name="markers")
    fp = folium.FeatureGroup(name="Ukraine")
    folium.GeoJson(data=open('ukraine.geojson',
                             'r', encoding='utf-8-sig').read()).add_to(fp)
    folium.Marker(location=[lat, lng],
                  popup='<b>My coordinates<b>',
                  tooltip=tooltip,
                  icon=folium.Icon(color='red',
                  icon='info-sign')).add_to(fg)
    for i in data:
        folium.Marker(
            location=[i[1][-2], i[1][-1]],
            popup=str(i[1][0] + ' ' + i[1][1]),
            tooltip=tooltip,
            icon=folium.Icon(color='blue',
                             icon='info-sign')).add_to(fg)
        folium.PolyLine(
            locations=[[lat, lng], [i[1][-2], i[1][-1]]],
            tooltip=str(str(round(i[0], 2)) + ' km'),
            color='blue').add_to(fg)
    fg.add_to(m)
    fp.add_to(m)
    folium.LayerControl().add_to(m)
    m.save('{0}_movies_map.html'.format(data[0][1][1]))
    return 'Finished. Please have look at the map: \
    {0}_movies_map.html'.format(data[0][1][1])


if __name__ == '__main__':
    year = input('Enter the year for analysis: ')
    latitude = float(input('Enter the latitude: '))
    longitude = float(input('Enter the longitude: '))
    print('Map is generating...\nPlease wait...')
    coo = find_my_coo(latitude, longitude)
    data_ = reading_file('locations.list', coo, year)
    data_coo = coordinates(data_)
    nearest = find_nearest(data_coo, coo)
    c = creating_map(nearest, latitude, longitude)
    print(c)
