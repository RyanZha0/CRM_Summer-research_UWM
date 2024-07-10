import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from scipy.stats import sem

file_path = r'D:\summer research\dataexperiment\data3min_daytime1.csv'
data = pd.read_csv(file_path)

data.head()



# 计算平均值和标准误差
mean_distance_82 = data['Distance_82'].mean()
mean_distance_83 = data['Distance_83'].mean()
sem_distance_82 = sem(data['Distance_82'])
sem_distance_83 = sem(data['Distance_83'])

# 绘制带有误差线的图
plt.figure(figsize=(10, 6))
plt.errorbar(['Distance_82', 'Distance_83'], [mean_distance_82, mean_distance_83],
             yerr=[sem_distance_82, sem_distance_83], fmt='o', capsize=5, capthick=2, elinewidth=2)
plt.ylabel('Distance')
plt.title('Average Distance with Error Bars')
plt.grid(True)
plt.show()


# 绘制箱线图
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.boxplot([data['Distance_82'], data['Distance_83']], labels=['Distance_82', 'Distance_83'])
plt.ylabel('Distance')
plt.title('Box Plot of Distance')

# 绘制直方图
plt.subplot(1, 2, 2)
plt.hist(data['Distance_82'], bins=30, alpha=0.5, label='Distance_82')
plt.hist(data['Distance_83'], bins=30, alpha=0.5, label='Distance_83')
plt.xlabel('Distance')
plt.ylabel('Frequency')
plt.title('Histogram of Distance')
plt.legend()

plt.tight_layout()
plt.show()

