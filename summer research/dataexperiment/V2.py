import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取数据
file_path = r'D:\summer research\dataexperiment\data3min_daytime1.csv'
data = pd.read_csv(file_path)

# 排除非数值列（如时间戳）
numeric_data = data.select_dtypes(include=[np.number])

# 计算统计量
statistics = numeric_data.describe().transpose()

# 计算标准误差
statistics['std_err'] = numeric_data.std() / np.sqrt(len(numeric_data))

print(statistics)

# 绘制带有误差线的图
mean_distance_82 = numeric_data['Distance_82'].mean()
mean_distance_83 = numeric_data['Distance_83'].mean()
sem_distance_82 = numeric_data['Distance_82'].std() / (len(numeric_data['Distance_82']) ** 0.5)
sem_distance_83 = numeric_data['Distance_83'].std() / (len(numeric_data['Distance_83']) ** 0.5)

plt.figure(figsize=(10, 6))
plt.errorbar(['Distance_82', 'Distance_83'], [mean_distance_82, mean_distance_83],
             yerr=[sem_distance_82, sem_distance_83], fmt='o', capsize=5, capthick=2, elinewidth=2)
plt.ylabel('Distance')
plt.title('Average Distance with Error Bars')
plt.grid(True)
plt.show()

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.boxplot([numeric_data['Distance_82'], numeric_data['Distance_83']], labels=['Distance_82', 'Distance_83'])
plt.ylabel('Distance')
plt.title('Box Plot of Distance')

plt.subplot(1, 2, 2)
plt.hist(numeric_data['Distance_82'], bins=30, alpha=0.5, label='Distance_82')
plt.hist(numeric_data['Distance_83'], bins=30, alpha=0.5, label='Distance_83')
plt.xlabel('Distance')
plt.ylabel('Frequency')
plt.title('Histogram of Distance')
plt.legend()

plt.tight_layout()
plt.show()
