import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from data_cleaning import demographic

def plot(data, demo, year):
    x = np.arange(len(demographic(data, demo, year)[demo]))

    fig, ax = plt.subplots()

    ax.bar(x, demographic(data, demo, year)['percent'])
    ax.set_xticks(x)
    ax.set_xticklabels(demographic(data, demo, year)[demo]);

    plt.show()







if __name__ in '__main__':
    
    print(plot(data07, 'sex', 2007))