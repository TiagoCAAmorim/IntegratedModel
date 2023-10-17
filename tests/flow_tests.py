import os
from context import flow
# import matplotlib.pyplot as plt  

# path = os.path.abspath(os.path.dirname(__file__))
# def save_plot(plt, name):
#     plt.savefig(path+'/plots/'+name+'.png')
#     # plt.show()

def define_common_parameters():
    trunk = flow.FlowElement()
    trunk.pvt.set_api(15.)
    trunk.pvt.set_gor(20.)
    trunk.pvt.set_dg(0.6)
    trunk.set_t_in(50.)
    trunk.set_d(6 * 2.54/100.)
    trunk.set_e(0.6 / 1000)
    return trunk

def define_trunk1():
    trunk = define_common_parameters()    
    trunk.set_p_in(340)
    trunk.set_h(1600.)
    trunk.set_z_in(-1600. + -1320.)
    trunk.set_z_out(-1320.)
    return trunk

def define_trunk2():
    trunk = define_common_parameters()    
    trunk.set_h(500.)
    trunk.set_z_in(-1320.)
    trunk.set_z_out(-1320.)
    return trunk

def define_trunk3():
    trunk = define_common_parameters()    
    trunk.set_h(1320.)
    trunk.set_z_in(-1320.)
    trunk.set_z_out(0.)
    return trunk

def horizontal_test():
    print('1000 m Horizontal trunk')
    trunk = define_trunk1()
    trunk.set_z_in(0.)
    trunk.set_z_out(0.)
    trunk.set_q_in(1000.)
    trunk.solve_out_flow()
    print(f'  Pressure in: {trunk.get_p_in()} bar.')
    print(f'  Pressure out: {trunk.get_p_out()} bar.')

def vertical_test():
    print('1000 m Vertical trunk')
    trunk = define_trunk1()
    trunk.set_z_in(0.)
    trunk.set_z_out(1000.)
    trunk.set_q_in(1000.)
    trunk.solve_out_flow()
    print(f'  Pressure in: {trunk.get_p_in()} bar.')
    print(f'  Pressure out: {trunk.get_p_out()} bar.')

# def horizontal_test():
    # trunk = flow.FlowElement()


if __name__ == "__main__":
    # horizontal_test()
    vertical_test()