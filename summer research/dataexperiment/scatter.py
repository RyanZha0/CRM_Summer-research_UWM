import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = r'D:\summer research\dataexperiment\data3min_daytime1.csv'
data = pd.read_csv(file_path)

anchor1 = (0, 0)
d = 1
anchor2 = (d, 0)

def calculate_tag_position(distance1, distance2, d):
    x = (distance1**2 - distance2**2 + d**2) / (2 * d)
    y = np.sqrt(distance1**2 - x**2)
    return (x, y)

tags = []

for index, row in data.iterrows():
    tag_position = calculate_tag_position(row['Distance_82'], row['Distance_83'], d)
    tags.append(tag_position)

tags = np.array(tags)

plt.figure(figsize=(10, 6))
plt.scatter(tags[:, 0], tags[:, 1], c='blue', label='Tags')
plt.scatter(anchor1[0], anchor1[1], c='red', label='Anchor 1')
plt.scatter(anchor2[0], anchor2[1], c='red', label='Anchor 2')

offset = 0.02
plt.text(anchor1[0], anchor1[1] + offset, 'Anchor 1', fontsize=10, ha='center', va='bottom', color='black')
plt.text(anchor2[0], anchor2[1] + offset, 'Anchor 2', fontsize=10, ha='center', va='bottom', color='black')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Tag positions based on distances from anchors')
plt.legend()
plt.grid(True)
plt.show()
