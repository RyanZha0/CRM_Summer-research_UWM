import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

def animate(i):
    # Read data from CSV
    data = pd.read_csv('./data.csv')
    
    x = data['Timestamp']
    y1 = data['Distance_82']  
    y2 = data['Distance_83']  

    plt.cla()

    plt.plot(x, y1, label='Anchor1')  
    plt.plot(x, y2, label='Anchor2')  

    plt.xlabel('Time')  
    plt.ylabel('Distance')  
    plt.title('Distance over Time')  

    plt.legend(loc='upper left')  # Ensure legend is updated
    plt.tight_layout()

# Set up animation
ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()
