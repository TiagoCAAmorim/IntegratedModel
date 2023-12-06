import os
from context import relative_permeability as kr
from context import common
import matplotlib.pyplot as plt

debug_mode = True

path = os.path.abspath(os.path.dirname(__file__))
def save_plot(plot, name):
    plot.savefig(path+'/plots/kr/'+name+'.png')
    plot.close()

def simple_plot(x,y, x_label, y_label, title, file):
    _ = plt.figure()
    plt.plot(x, y)
    plt.grid()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    save_plot(plt,file)

def save_data(x,y, x_label, y_label, file):
    common.make_columns_file(x, y, x_label, y_label, path+'/plots/kr/'+file+'.txt')

def kr_oil_water_corey():
    rel_perm = kr.Corey()
    rel_perm.sat.set_swi(0.10)
    rel_perm.sat.set_swc(0.20)
    rel_perm.sat.set_sorw(0.16)
    rel_perm.set_nw(2.0)
    rel_perm.set_now(3.0)
    rel_perm.set_krw_max(0.63)
    rel_perm.set_kro_max(0.9)

    sw_init = 0
    sw_end = 1
    steps = 101
    sw_list = [sw_init + i/(steps-1)*(sw_end - sw_init) for i in range(steps)]
    krw = []
    krow = []
    dkrw = []
    dkrow = []
    for sw in sw_list:
        krw.append(rel_perm.get_krw_2f(sw))
        krow.append(rel_perm.get_krow_2f(sw))
        dkrw.append(rel_perm.get_dkrw_2f(sw))
        dkrow.append(rel_perm.get_dkrow_2f(sw))

    save_data(sw_list, krw, 'Sw', 'Krw', 'corey_krw')
    save_data(sw_list, krow, 'Sw', 'Kro', 'corey_kro')

    _ = plt.figure()
    plt.plot(sw_list, krw)
    plt.plot(sw_list, krow)

    ax = plt.gca()
    ax.legend({"Krw","Krow"})
    plt.grid()
    plt.xlabel('Sw')
    plt.ylabel('Kr')
    plt.title('Corey')
    save_plot(plt,'corey')

    _ = plt.figure()
    plt.plot(sw_list, dkrw)
    plt.plot(sw_list, dkrow)

    ax = plt.gca()
    ax.legend({"dKrw","dKrow"})
    plt.grid()
    plt.xlabel('Sw')
    plt.ylabel('dKr')
    plt.title('Corey')
    save_plot(plt,'corey_prime')



if __name__ == "__main__":
    kr_oil_water_corey()
    pass
