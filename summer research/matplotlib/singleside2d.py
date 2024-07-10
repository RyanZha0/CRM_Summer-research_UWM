import serial
import time
import math
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

arduino = serial.Serial(port='COM6', baudrate=115200, timeout=.1)
id_list = [82, 83]
distance = {82: 0, 83: 0}
coord = [[0, 0], [1, 0]]  # Coordinates of the anchors
active_device = 0
x, y = 0, 0
dist_aa = math.sqrt((coord[0][0] - coord[1][0]) ** 2 + (coord[0][1] - coord[1][1]) ** 2)

# Create a list
data_list = []

def get_coord(dist_a1, dist_a2, dist_aa):
    cos_a = (dist_a1**2 + dist_aa**2 - dist_a2**2) / (2 * dist_a1 * dist_aa)
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

                    timestamp = time.time()

                    data_list.append({
                        'Timestamp': timestamp,
                        'Device': description,
                        'Distance_82': distance[82],
                        'Distance_83': distance[83],
                        'X': x,
                        'Y': y
                    })

                    # Keep only the latest entry in data_list to reduce memory usage
                    if len(data_list) > 1:
                        data_list = data_list[-1:]

                    print(f'{timestamp}: {distance}, {x}, {y}')

def animate(i):
    if data_list:
        x_coords = [coord[0][0], coord[1][0], data_list[-1]['X']]
        y_coords = [coord[0][1], coord[1][1], data_list[-1]['Y']]
        dist_82 = data_list[-1]['Distance_82']
        dist_83 = data_list[-1]['Distance_83']

        plt.cla()
        plt.scatter(x_coords[:2], y_coords[:2], label='Anchors', color='blue', s=100) 
        plt.scatter(x_coords[2], y_coords[2], label='Tag', color='red', s=100) 

        offset = 0.02
        
        plt.text(x_coords[0], y_coords[0] + offset, 'Anchor 1', fontsize=12, ha='center', va='bottom', color='blue')
        plt.text(x_coords[1], y_coords[1] + offset, 'Anchor 2', fontsize=12, ha='center', va='bottom', color='blue')
        plt.text(x_coords[2], y_coords[2] + offset, f'Tag\nDist to A1: {dist_82:.2f}\nDist to A2: {dist_83:.2f}', fontsize=12, ha='center', va='bottom', color='red')

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Real-time 2D Positioning')

        plt.legend(loc='upper left')
        plt.axis('equal')  
        plt.xlim(-0.5, 1.5) 
        plt.ylim(-0.5, 1.5)  
        plt.tight_layout()

data_thread = threading.Thread(target=read_data)
data_thread.daemon = True
data_thread.start()

plt.style.use('fivethirtyeight')
ani = FuncAnimation(plt.gcf(), animate, interval=1000)
plt.tight_layout()
plt.show()
