import serial
import time
import math
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

arduino = serial.Serial(port='COM6', baudrate=115200, timeout=.1)
id_list = [82, 83]
distance = {82: 0, 83: 0}
coord = [[0, 0], [1, 0]]
active_device = 0
x, y = 0, 0
dist_aa = math.sqrt((coord[0][0] - coord[1][0]) ** 2 + (coord[0][1] - coord[1][1]) ** 2)

#create a list
data_list = []

def get_coord(dist_a1, dist_a2, dist_aa):
    cos_a = (dist_a1**2 + dist_aa**2 - dist_a2**2)/(2*dist_a1*dist_aa)
    sin_a = math.sqrt(1 - cos_a**2)
    x = dist_a1 * cos_a
    y = dist_a1 * sin_a
    return x, y

def read_data():
    global active_device, distance, x, y, data_list

    while True:
        message = arduino.readline()
        message = message.decode('utf-8').rstrip()

        if message != '' and len(message.split(': ')) > 1:
            description, data = message.split(': ')

            if description == 'Device added':
                active_device += 1
            elif description == 'delete inactive device':
                active_device -= 1

            if active_device == 2:
                if description == 'Distance':
                    id, dist = data.split(',')

                    if float(dist) >= 0:
                        distance[int(id)] = float(dist)

                    if distance[id_list[0]] > 0 and distance[id_list[1]] > 0:
                        dist_a1 = distance[id_list[0]]
                        dist_a2 = distance[id_list[1]]
                        cos_a = (dist_a1**2 + dist_aa**2 - dist_a2**2) / (2 * dist_a1 * dist_aa)
                        if cos_a >= -1 and cos_a <= 1:
                            x, y = get_coord(dist_a1, dist_a2, dist_aa)

                    # Get current timestamp
                    timestamp = time.time()

                    # Add data to the list
                    data_list.append({
                        'Timestamp': timestamp,
                        'Device': description,
                        'Distance_82': distance[82],
                        'Distance_83': distance[83],
                        'X': x,
                        'Y': y
                    })

                    print(f'{timestamp}: {distance}, {x}, {y}')

def animate(i):
    timestamps = [entry['Timestamp'] for entry in data_list]
    distances_82 = [entry['Distance_82'] for entry in data_list]
    distances_83 = [entry['Distance_83'] for entry in data_list]

    plt.cla()
    plt.plot(timestamps, distances_82, label='Anchor1')
    plt.plot(timestamps, distances_83, label='Anchor2')

    plt.xlabel('Time')
    plt.ylabel('Distance')
    plt.title('Distance over Time')

    plt.legend(loc='upper left')
    plt.tight_layout()

# Start data reading thread
data_thread = threading.Thread(target=read_data)
data_thread.daemon = True
data_thread.start()

# Set up the plot
plt.style.use('fivethirtyeight')
ani = FuncAnimation(plt.gcf(), animate, interval=1000)
plt.tight_layout()
plt.show()
