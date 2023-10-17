import os
from context import flow
import matplotlib.pyplot as plt  

path = os.path.abspath(os.path.dirname(__file__))
def save_plot(plt, name):
    plt.savefig(path+'/plots/'+name+'.png')
    # plt.show()


if __name__ == "__main__":
    pass