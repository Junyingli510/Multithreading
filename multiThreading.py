##############################   Features   ##############################
#
# 1. Reading ISS position will be in one thread
# 2. Writing to csv will be in another thread
# 3. Make a real-time plot visualizing the ISS position (x = longitude, y = latitutude). Plotting will be also in different thread
# 4. Read, write and visualize with different frequencies (eg. read every second, write every 5 seconds, visualize every 3 seconds)

import matplotlib.pyplot as plt
import numpy
import requests
from time import sleep
import threading
from matplotlib.animation import FuncAnimation
import csv

hl, = plt.plot([], []) #empty plot
plt.ylim(-360, 360)       # set axis limits
plt.xlim(-360, 360)
new_data= [0,0]

location = {}
    
def get_location():
    #A JSON request to retrieve the current longitude and latitude of the IIS space station (real time)  
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    result = response.json()
    
    global location
    #Let's extract the required information
    location = result["iss_position"]
    lat = location["latitude"]
    lon = location["longitude"]
        
    #Output informationon screen
    print("_ ISS location: ", lat, lon)

    threading.Timer( 1, get_location).start()

def write_location():
    lat = str(location["latitude"])
    lon = str(location['longitude'])
    print("_____ Write_location : ", lat, lon)
    with open('location.csv', 'a', newline="", encoding="utf8") as file:
        reader = csv.writer(file)
        reader.writerows([[lat + ' ' + lon]])
        
    threading.Timer( 5, write_location).start()

def update_line(hl, new_data):
    # set x, y value for draw graph
    hl.set_xdata(numpy.append(hl.get_xdata(), new_data[0]))
    hl.set_ydata(numpy.append(hl.get_ydata(), new_data[1]))
    plt.draw()        # draw new data
    plt.pause(3)    # update graph every 0.5 second

def draw_location():
    for _ in range(0, 50000):
        global location
        new_data[0] = float(location['latitude'])     # x data
        new_data[1] = float(location['longitude'])  # y data
            # new_data[0] = _      # x data
            # new_data[1] = _ + 1  # y data
        print("___ draw location", new_data[0],  new_data[1])
        update_line(hl, new_data)

if __name__ == '__main__':
    get_location()
    write_location()
    draw_location()