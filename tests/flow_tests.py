import os
from context import flow
import matplotlib.pyplot as plt

path = os.path.abspath(os.path.dirname(__file__))
def save_plot(plt, name):
    plt.savefig(path+'/plots/'+name+'.png')
    # plt.show()

def define_common_parameters(trunk):
    trunk.pvt.set_api(15.)
    trunk.pvt.set_gor(20.)
    trunk.pvt.set_dg(0.6)

    trunk.set_d(6. * 2.54/100.)
    trunk.set_e(0.6 / 1000.)

    trunk.set_p_in(340.)
    trunk.set_t_in(50.)

    trunk.set_q_std(1000.)

def horizontal_test():
    print('1000 m Horizontal trunk')
    trunk = flow.SubFlowElement()
    define_common_parameters(trunk)
    trunk.set_h(1600.)
    trunk.set_z_in(0.)
    trunk.set_z_out(0.)
    print('  Calculation from Inlet to Outlet')
    trunk.solve_out_flow()
    print(f'    Pressure in: {trunk.get_p_in()} bar.')
    print(f'    Pressure out: {trunk.get_p_out()} bar.')
    print('  Calculation from Outlet to Inlet')
    trunk.set_p_in(None)
    trunk.set_q_in(None)
    trunk.solve_in_flow()
    print(f'    Pressure in: {trunk.get_p_in()} bar.')
    print(f'    Pressure out: {trunk.get_p_out()} bar.')

def vertical_test():
    print('1000 m Vertical trunk')
    trunk = flow.SubFlowElement()
    define_common_parameters(trunk)
    trunk.set_h(1600.)
    trunk.set_z_in(0.)
    trunk.set_z_out(1000.)
    print('  Calculation from Inlet to Outlet')
    trunk.solve_out_flow()
    print(f'    Pressure in: {trunk.get_p_in()} bar.')
    print(f'    Pressure out: {trunk.get_p_out()} bar.')
    print('  Calculation from Outlet to Inlet')
    trunk.set_p_in(None)
    trunk.set_q_in(None)
    trunk.solve_in_flow()
    print(f'    Pressure in: {trunk.get_p_in()} bar.')
    print(f'    Pressure out: {trunk.get_p_out()} bar.')

def horizontal_divided_test():
    print('1000 m Horizontal trunk with divisions')
    trunk = flow.FlowElement()
    define_common_parameters(trunk)
    trunk.set_number_divisions(10)
    trunk.set_h(1600.)
    trunk.set_z_in(0.)
    trunk.set_z_out(0.)

    print('  Calculation from Inlet to Outlet')
    trunk.solve_out_flow()
    print(f'    Pressure in: {trunk.get_p_in()[0]} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]} bar.')

    _ = plt.figure()
    plt.plot([0] + trunk.get_h_cumulative(), [trunk.get_p_in()[0]] + trunk.get_p_out())

    print('  Calculation from Outlet to Inlet')
    trunk.set_p_in(None)
    trunk.set_q_in(None)
    trunk.solve_in_flow()
    print(f'    Pressure in: {trunk.get_p_in()[0]} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]} bar.')

    plt.plot([0] + trunk.get_h_cumulative(), trunk.get_p_in() + [trunk.get_p_out()[-1]])
    ax = plt.gca()
    ax.legend(['Inlet to Outlet', 'Outlet to Inlet'])
    plt.grid()
    plt.xlabel('Lenght along element [m]')
    plt.ylabel('p [bar]')
    plt.title('Horizontal Trunk')
    save_plot(plt,'horizontal')

def vertical_divided_test():
    print('1000 m Vertical trunk with divisions')
    trunk = flow.FlowElement()
    define_common_parameters(trunk)
    trunk.set_number_divisions(10)
    trunk.set_h(1600.)
    trunk.set_z_in(0.)
    trunk.set_z_out(1000.)

    print('  Calculation from Inlet to Outlet')
    trunk.solve_out_flow()
    print(f'    Pressure in: {trunk.get_p_in()[0]} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]} bar.')

    _ = plt.figure()
    plt.plot([0] + trunk.get_h_cumulative(), [trunk.get_p_in()[0]] + trunk.get_p_out())

    print('  Calculation from Outlet to Inlet')
    trunk.set_p_in(None)
    trunk.set_q_in(None)
    trunk.solve_in_flow()
    print(f'    Pressure in: {trunk.get_p_in()[0]} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]} bar.')

    plt.plot([0] + trunk.get_h_cumulative(), trunk.get_p_in() + [trunk.get_p_out()[-1]])
    ax = plt.gca()
    ax.legend(['Inlet to Outlet', 'Outlet to Inlet'])
    plt.grid()
    plt.xlabel('Lenght along element [m]')
    plt.ylabel('p [bar]')
    plt.title('Vertical Trunk')
    save_plot(plt,'vertical')

def vertical_sensibility_test():
    print('1000 m Vertical trunk with divisions - sensibility')
    trunk = flow.FlowElement()
    define_common_parameters(trunk)
    trunk.set_h(1600.)
    trunk.set_z_in(0.)
    trunk.set_z_out(1000.)
    print('  Calculation from Inlet to Outlet')
    print(f'    Pressure in: {trunk.get_p_in()[0]} bar.')

    n_list = [1, 5, 10, 20, 50, 100, 500, 1000]
    p_list = []
    for n in n_list:
        trunk.set_number_divisions(n)
        trunk.solve_out_flow()
        p_list.append(trunk.get_p_out()[-1])
        print(f'    Pressure out ({n} segments): {p_list[-1]} bar.')

    _ = plt.figure()
    plt.plot(n_list, p_list)
    plt.grid()
    plt.xlabel('Number of segments in calculation')
    plt.ylabel('p out [bar]')
    plt.title('Vertical Trunk')
    save_plot(plt,'vertical_sensibility')

def horizontal_two_elements_test():
    print('1000 m Horizontal trunk as two elements')
    trunk = flow.CompositeFlowElement()
    define_common_parameters(trunk)
    trunk.set_number_divisions(5)

    trunk.add_element()
    trunk.current_element.set_h(800.)
    trunk.current_element.set_z_in(0.)
    trunk.current_element.set_z_out(0.)

    trunk.add_element()
    trunk.current_element.set_h(800.)
    trunk.current_element.set_z_in(0.)
    trunk.current_element.set_z_out(0.)

    print('  Calculation from Inlet to Outlet')
    trunk.solve_out_flow()
    print(f'    Pressure in: {trunk.get_p_in()[0]} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]} bar.')

    _ = plt.figure()
    plt.plot([0] + trunk.get_h_cumulative(), [trunk.get_p_in()[0]] + trunk.get_p_out())

    print('  Calculation from Outlet to Inlet')
    trunk.set_p_in(None)
    trunk.set_q_in(None)
    trunk.solve_in_flow()
    print(f'    Pressure in: {trunk.get_p_in()[0]} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]} bar.')

    plt.plot([0] + trunk.get_h_cumulative(), trunk.get_p_in() + [trunk.get_p_out()[-1]])
    ax = plt.gca()
    ax.legend(['Inlet to Outlet', 'Outlet to Inlet'])
    plt.grid()
    plt.xlabel('Lenght along element [m]')
    plt.ylabel('p [bar]')
    plt.title('Horizontal Trunk as Two Elements')
    save_plot(plt,'horizontal2')

def vertical_two_elements_test():
    print('1000 m Horizontal trunk as two elements')
    trunk = flow.CompositeFlowElement()
    define_common_parameters(trunk)
    trunk.set_number_divisions(5)

    trunk.add_element()
    trunk.current_element.set_h(800.)
    trunk.current_element.set_z_in(0.)
    trunk.current_element.set_z_out(500.)

    trunk.add_element()
    trunk.current_element.set_h(800.)
    trunk.current_element.set_z_in(500.)
    trunk.current_element.set_z_out(1000.)

    print('  Calculation from Inlet to Outlet')
    trunk.solve_out_flow()
    print(f'    Pressure in: {trunk.get_p_in()[0]} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]} bar.')
    _ = plt.figure()
    plt.plot([0] + trunk.get_h_cumulative(), [trunk.get_p_in()[0]] + trunk.get_p_out())

    print('  Calculation from Outlet to Inlet')
    trunk.set_p_out(trunk._elements[-1].get_p_out()[-1])
    trunk.set_q_out(trunk._elements[-1].get_q_out()[-1])
    trunk.set_p_in(None)
    trunk.set_q_in(None)
    trunk.solve_in_flow()
    print(f'    Pressure in: {trunk.get_p_in()[0]} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]} bar.')

    plt.plot([0] + trunk.get_h_cumulative(), trunk.get_p_in() + [trunk.get_p_out()[-1]])
    ax = plt.gca()
    ax.legend(['Inlet to Outlet', 'Outlet to Inlet'])
    plt.grid()
    plt.xlabel('Lenght along element [m]')
    plt.ylabel('p [bar]')
    plt.title('Vertical Trunk as Two Elements')
    save_plot(plt,'vertical2')

def define_system_ex1():
    trunk = flow.CompositeFlowElement()
    define_common_parameters(trunk)
    trunk.set_number_divisions(100)

    trunk.add_element()
    trunk.current_element.set_h(1600.)
    trunk.current_element.set_z_in(-1600. + -1320.)
    trunk.current_element.set_z_out(-1320.)

    trunk.add_element()
    trunk.current_element.set_h(500.)
    trunk.current_element.set_z_in(-1320.)
    trunk.current_element.set_z_out(-1320.)
    trunk.current_element.set_number_divisions(10)

    trunk.add_element()
    trunk.current_element.set_h(1320.)
    trunk.current_element.set_z_in(-1320.)
    trunk.current_element.set_z_out(0.)

    return trunk

def system_ex1():
    print('System with 3 Elements - Example 1')

    trunk = define_system_ex1()
    print('  Calculation from Inlet to Outlet')
    trunk.solve_out_flow()
    print(f'    Pressure in: {trunk.get_p_in()[0]} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]} bar.')

    _ = plt.figure()
    plt.plot([0] + trunk.get_h_cumulative(), [trunk.get_p_in()[0]] + trunk.get_p_out())

    print('  Calculation from Outlet to Inlet')
    trunk.set_p_out(trunk._elements[-1].get_p_out()[-1])
    trunk.set_q_out(trunk._elements[-1].get_q_out()[-1])
    trunk.set_p_in(None)
    trunk.set_q_in(None)
    trunk.solve_in_flow()
    print(f'    Pressure in: {trunk.get_p_in()[0]} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]} bar.')

    plt.plot([0] + trunk.get_h_cumulative(), trunk.get_p_in() + [trunk.get_p_out()[-1]])
    ax = plt.gca()
    ax.legend(['Inlet to Outlet', 'Outlet to Inlet'])
    plt.grid()
    plt.xlabel('Lenght along element [m]')
    plt.ylabel('p [bar]')
    plt.title('System with 3 Elements - Example 1')
    save_plot(plt,'system1')

if __name__ == "__main__":
    horizontal_test()
    horizontal_divided_test()
    horizontal_two_elements_test()
    vertical_test()
    vertical_divided_test()
    vertical_two_elements_test()
    vertical_sensibility_test()
    system_ex1()
    pass
