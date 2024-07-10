import serial
import time
import math
import csv

arduino = serial.Serial(port='COM6', baudrate=115200, timeout=.1)
id_list = [82, 83]
distance = {82: 0, 83: 0}
coord = [[0, 0], [1, 0]]
active_device = 0
x, y = 0, 0
dist_aa = math.sqrt((coord[0][0] - coord[1][0]) ** 2 + (coord[0][1] - coord[1][1]) ** 2)

def get_coord(dist_a1, dist_a2, dist_aa):
    cos_a = (dist_a1**2 + dist_aa**2 - dist_a2**2)/(2*dist_a1*dist_aa)
    print(cos_a)
    sin_a = math.sqrt(1 - cos_a**2)
    x = dist_a1 * cos_a
    y = dist_a1 * sin_a
    return x, y


# 打开 CSV 文件，准备写入数据
with open('data.csv', 'w', newline='') as csv_file:
    fieldnames = ['Distance_82', 'Distance_83', 'X', 'Y']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

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
                        cos_a = (dist_a1**2 + dist_aa**2 - dist_a2**2)/(2*dist_a1*dist_aa)
                        if cos_a >= -1 and cos_a <= 1:
                            x, y = get_coord(dist_a1, dist_a2, dist_aa)
                        
                    
                    # 获取当前时间戳
                    #timestamp = time.time()

                    # 写入数据到 CSV 文件
                    csv_writer.writerow({
                        'Distance_82': distance[82],
                        'Distance_83': distance[83],
                        'X': x,
                        'Y': y
                    })

                    csv_file.flush()

                    print(distance, ': ', x, y)
