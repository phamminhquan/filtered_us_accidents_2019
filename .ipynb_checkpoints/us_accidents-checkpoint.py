import csv
import numpy as np
import ipyleaflet as leaflet
import ipywidgets as widgets

state_list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

# Get data from csv file
print('Getting Data')
data =[]
with open('US_Accidents_May19.csv', mode='r') as file:
    csv_reader = csv.reader(file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        data_sample = {}
        if line_count==0:
            keys = row
        else:
            for i in range(len(keys)):
                data_sample[keys[i]] = row[i]
            data.append(data_sample)
        line_count += 1
        
# Filter function
def predicate(sample):
    if sample['State']==state and sample['City']==city and int(sample['Severity'])==severity:
        return True
    else:
        return False

# Filtering
def filter_input(data): return list(filter(predicate, data))

# Create widgets for map
print('Creating Widget')
state_widget = widgets.Dropdown(
    options=state_list,
    value='AL',
    description='State:',
    disabled=False,
)

city_widget = widgets.Text(
    #value='',
    placeholder='e.g. Jacksonville',
    description='City:',
    disabled=False
)

severity_widget = widgets.BoundedIntText(
    value=1,
    min=1,
    max=4,
    step=1,
    description='Severity',
    disabled=False
)

# Create widget control
state_widget_control = leaflet.WidgetControl(widget=state_widget, position='topright')
city_widget_control = leaflet.WidgetControl(widget=city_widget, position='topright')
severity_widget_control = leaflet.WidgetControl(widget=severity_widget, position='topright')

# Input Param
print('Setting Input Parameters')
state = 'FL'
city = 'Jacksonville'
severity = 2
color_by_severity = {1:'green', 2:'blue', 3:'yellow', 4:'red'}
color = color_by_severity[severity]

# Filter data by input param
print('Filtering Input Data')
output = filter_input(data)

# Print-out to check
print(len(output))

# Get coordinates from filter output (lat, long)
coordinates = []
lat_center, lng_center = 0, 0
min_lat, max_lat, min_lng, max_lng = 0, 0, 0, 0
for sample in output:
    coordinates.append((float(sample['Start_Lat']), float(sample['Start_Lng'])))
    lat_center += float(sample['Start_Lat'])
    lng_center += float(sample['Start_Lng'])
lat_center /= len(output)
lng_center /= len(output)

# Get min and max lat for zoom calculation
lat_min_max = min(coordinates)[0], max(coordinates)[0]
lat_range = lat_min_max[1]-lat_min_max[0]
lng_min_max = min(coordinates)[1], max(coordinates)[1]
lng_range = lng_min_max[1]-lng_min_max[0]
if lat_range > lng_range:
    max_range = lat_range
else:
    max_range = lng_range
print(max_range)

# Generate map
print('Rendering Map')
center = (lat_center, lng_center) # geological center of US
zoom = int(np.floor(-3.3333*max_range + 11.6667))
if zoom > 18:
    zoom = 18
elif zoom < 1:
    zoom = 1
m = leaflet.Map(center=center, zoom=zoom)
m.add_control(state_widget_control)
m.add_control(city_widget_control)
m.add_control(severity_widget_control)
for i in range(len(coordinates)):
    circle = leaflet.Circle()
    circle.location = coordinates[i]
    circle.radius = 30
    circle.color = color
    circle.fill_color = color
    m.add_layer(circle)
m

try:
    while True:
        pass
except KeyboardInterrupt:
    print('End')