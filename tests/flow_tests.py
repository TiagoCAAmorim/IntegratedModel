import os
from context import flow
import matplotlib.pyplot as plt

debug_mode = True

path = os.path.abspath(os.path.dirname(__file__))
def save_plot(plt, name):
    plt.savefig(path+'/plots/'+name+'.png')
    # plt.show()

def simple_plot(x,y, x_label, y_label, title, file):
    _ = plt.figure()
    plt.plot(x, y)
    plt.grid()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    save_plot(plt,file)

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
    print(f'    Pressure in: {trunk.get_p_in():.3f} bar.')
    print(f'    Pressure out: {trunk.get_p_out():.3f} bar.')
    print('  Calculation from Outlet to Inlet')
    trunk.set_p_in(None)
    trunk.set_q_in(None)
    trunk.solve_in_flow()
    print(f'    Pressure in: {trunk.get_p_in():.3f} bar.')
    print(f'    Pressure out: {trunk.get_p_out():.3f} bar.')

def vertical_test():
    print('1000 m Vertical trunk')
    trunk = flow.SubFlowElement()
    define_common_parameters(trunk)
    trunk.set_h(1600.)
    trunk.set_z_in(0.)
    trunk.set_z_out(1000.)
    print('  Calculation from Inlet to Outlet')
    trunk.solve_out_flow()
    print(f'    Pressure in: {trunk.get_p_in():.3f} bar.')
    print(f'    Pressure out: {trunk.get_p_out():.3f} bar.')
    print('  Calculation from Outlet to Inlet')
    trunk.set_p_in(None)
    trunk.set_q_in(None)
    trunk.solve_in_flow()
    print(f'    Pressure in: {trunk.get_p_in():.3f} bar.')
    print(f'    Pressure out: {trunk.get_p_out():.3f} bar.')

def horizontal_divided_test():
    print('1000 m Horizontal trunk with divisions')
    trunk = flow.FlowElement(debug_mode=debug_mode)
    define_common_parameters(trunk)
    trunk.set_number_divisions(10)
    trunk.set_h(1600.)
    trunk.set_z_in(0.)
    trunk.set_z_out(0.)

    print('  Calculation from Inlet to Outlet')
    trunk.solve_out_flow()
    print(f'    Pressure in: {trunk.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]:.3f} bar.')

    _ = plt.figure()
    plt.plot([0] + trunk.get_h_cumulative(), [trunk.get_p_in()[0]] + trunk.get_p_out())

    print('  Calculation from Outlet to Inlet')
    trunk.set_p_in(None)
    trunk.set_q_in(None)
    trunk.solve_in_flow()
    print(f'    Pressure in: {trunk.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]:.3f} bar.')

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
    trunk = flow.FlowElement(debug_mode=debug_mode)
    define_common_parameters(trunk)
    trunk.set_number_divisions(10)
    trunk.set_h(1600.)
    trunk.set_z_in(0.)
    trunk.set_z_out(1000.)

    print('  Calculation from Inlet to Outlet')
    trunk.solve_out_flow()
    print(f'    Pressure in: {trunk.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]:.3f} bar.')

    _ = plt.figure()
    plt.plot([0] + trunk.get_h_cumulative(), [trunk.get_p_in()[0]] + trunk.get_p_out())

    print('  Calculation from Outlet to Inlet')
    trunk.set_p_in(None)
    trunk.set_q_in(None)
    trunk.solve_in_flow()
    print(f'    Pressure in: {trunk.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]:.3f} bar.')

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
    trunk = flow.FlowElement(debug_mode=False)
    define_common_parameters(trunk)
    trunk.set_h(1600.)
    trunk.set_z_in(0.)
    trunk.set_z_out(1000.)
    print('  Calculation from Inlet to Outlet')
    print(f'    Pressure in: {trunk.get_p_in()[0]:.3f} bar.')

    n_list = [1, 5, 10, 20, 50, 100, 500, 1000]
    p_list = []
    for n in n_list:
        trunk.set_number_divisions(n)
        trunk.solve_out_flow()
        p_list.append(trunk.get_p_out()[-1])
        print(f'    Pressure out ({n} segments): {p_list[-1]:.3f} bar.')

    _ = plt.figure()
    plt.plot(n_list, p_list)
    plt.grid()
    plt.xlabel('Number of segments in calculation')
    plt.ylabel('p out [bar]')
    plt.title('Vertical Trunk')
    save_plot(plt,'vertical_sensibility')

def horizontal_two_elements_test():
    print('1000 m Horizontal trunk as two elements')
    trunk = flow.CompositeFlowElement(debug_mode=debug_mode)
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
    print(f'    Pressure in: {trunk.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]:.3f} bar.')

    _ = plt.figure()
    plt.plot([0] + trunk.get_h_cumulative(), [trunk.get_p_in()[0]] + trunk.get_p_out())

    print('  Calculation from Outlet to Inlet')
    trunk.set_p_in(None)
    trunk.set_q_in(None)
    trunk.solve_in_flow()
    print(f'    Pressure in: {trunk.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]:.3f} bar.')

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
    trunk = flow.CompositeFlowElement(debug_mode=debug_mode)
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
    print(f'    Pressure in: {trunk.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]:.3f} bar.')
    _ = plt.figure()
    plt.plot([0] + trunk.get_h_cumulative(), [trunk.get_p_in()[0]] + trunk.get_p_out())

    print('  Calculation from Outlet to Inlet')
    trunk.set_p_out(trunk._elements[-1].get_p_out()[-1])
    trunk.set_q_out(trunk._elements[-1].get_q_out()[-1])
    trunk.set_p_in(None)
    trunk.set_q_in(None)
    trunk.solve_in_flow()
    print(f'    Pressure in: {trunk.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]:.3f} bar.')

    plt.plot([0] + trunk.get_h_cumulative(), trunk.get_p_in() + [trunk.get_p_out()[-1]])
    ax = plt.gca()
    ax.legend(['Inlet to Outlet', 'Outlet to Inlet'])
    plt.grid()
    plt.xlabel('Lenght along element [m]')
    plt.ylabel('p [bar]')
    plt.title('Vertical Trunk as Two Elements')
    save_plot(plt,'vertical2')

def define_system_ex1(debug_mode):
    trunk = flow.CompositeFlowElement(debug_mode=debug_mode)
    define_common_parameters(trunk)
    trunk.set_number_divisions(100)

    trunk.add_element()
    trunk.current_element.set_h(1600.)
    trunk.current_element.set_z_in(-1600. + -1320.)
    trunk.current_element.set_z_out(-1320.)
    trunk.current_element.set_number_divisions(160)

    trunk.add_element()
    trunk.current_element.set_h(500.)
    trunk.current_element.set_z_in(-1320.)
    trunk.current_element.set_z_out(-1320.)
    trunk.current_element.set_number_divisions(5)

    trunk.add_element()
    trunk.current_element.set_h(1320.)
    trunk.current_element.set_z_in(-1320.)
    trunk.current_element.set_z_out(0.)
    trunk.current_element.set_number_divisions(132)

    return trunk

def system_ex1():
    print('System with 3 Elements - Example 1')

    trunk = define_system_ex1(debug_mode=debug_mode)
    print('  Calculation from Inlet to Outlet')
    trunk.solve_out_flow()
    print(f'    Pressure in: {trunk.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]:.3f} bar.')

    _ = plt.figure()
    plt.plot([0] + trunk.get_h_cumulative(), [trunk.get_p_in()[0]] + trunk.get_p_out())

    print('  Calculation from Outlet to Inlet')
    trunk.set_p_out(trunk._elements[-1].get_p_out()[-1])
    trunk.set_q_out(trunk._elements[-1].get_q_out()[-1])
    trunk.set_p_in(None)
    trunk.set_q_in(None)
    trunk.solve_in_flow()
    print(f'    Pressure in: {trunk.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]:.3f} bar.')

    plt.plot([0] + trunk.get_h_cumulative(), trunk.get_p_in() + [trunk.get_p_out()[-1]])

    plt.plot(trunk.get_h_cumulative(), trunk.get_p_bubble())

    ax = plt.gca()
    ax.legend(['Inlet to Outlet', 'Outlet to Inlet','Bubble pressure'])
    plt.grid()
    plt.xlabel('Lenght along element [m]')
    plt.ylabel('p [bar]')
    plt.title('System with 3 Elements - Example 1')
    save_plot(plt,'system1')

def system_ex1_vfp():
    print('System with 3 Elements - (q,p) plot')

    trunk = define_system_ex1(debug_mode=False)
    trunk.set_p_out(10.)
    trunk.set_t_out(50.)
    trunk.ipr.set_pi(40.)
    trunk.ipr.set_pr(340.)

    q_std = [10., 100., 200., 500., 600., 700., 800., 900., 1000., 1500., 2000., 2500., 2600., 2700., 2800., 2900., 3000., 3500., 4000.]
    pwf = []
    q_ipr = []
    for q in q_std:
        trunk.set_q_std(q)
        trunk.solve_in_flow()
        pwf.append(trunk.get_p_in()[0])
        q_ipr.append(trunk.ipr.get_q(pwf[-1]))

    trunk.solve_operation_point()
    print(f'Operation point: pwf = {trunk.get_pwf():.3f} bar, q = {trunk.ipr.get_q(trunk.get_pwf()):.3f} m3/d')

    _ = plt.figure()
    plt.plot(q_std, pwf, '-b')
    plt.plot(q_ipr, pwf, '-r')
    plt.plot(trunk.ipr.get_q(trunk.get_pwf()), trunk.get_pwf(), 'o')
    ax = plt.gca()
    ax.legend(['VFP', 'IPR', 'Operation'])
    plt.grid()
    plt.xlabel('Q [std m3/d]')
    plt.ylabel('Pwf [bar]')
    plt.title('System with 3 Elements - Example 1')
    save_plot(plt,'system1_qp')

    print('System with 3 Elements - Flow Calculation on the Operation Point')
    trunk.set_q_std(trunk.ipr.get_q(trunk.get_pwf()))
    trunk.solve_in_flow()
    print(f'    Pressure in: {trunk.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {trunk.get_p_out()[-1]:.3f} bar.')

    _ = plt.figure()
    plt.plot([0] + trunk.get_h_cumulative(), [trunk.get_p_in()[0]] + trunk.get_p_out())
    plt.plot(trunk.get_h_cumulative(), trunk.get_p_bubble())
    ax = plt.gca()
    ax.legend(['Pressure', 'Bubble pressure'])
    plt.grid()
    plt.xlabel('Length [m]')
    plt.ylabel('P [bar]')
    plt.title('System with 3 Elements - Example 1')
    save_plot(plt,'system1_operation')

    simple_plot(trunk.get_h_cumulative(), trunk.get_uo(),
                'Length [m]', 'uo [cP]',
                'System with 3 Elements - Example 1', 'system1_uo')
    simple_plot(trunk.get_h_cumulative(), trunk.get_rs(),
                'Length [m]', 'rs [m3/m3]',
                'System with 3 Elements - Example 1', 'system1_rs')
    simple_plot(trunk.get_h_cumulative(), trunk.get_bo(),
                'Length [m]', 'bo [-]',
                'System with 3 Elements - Example 1', 'system1_bo')
    simple_plot(trunk.get_h_cumulative(), trunk.get_re(),
                'Length [m]', 'Reynolds number',
                'System with 3 Elements - Example 1', 'system1_Re')
    simple_plot(trunk.get_h_cumulative(), trunk.get_f(),
                'Length [m]', 'friction factor [-]',
                'System with 3 Elements - Example 1', 'system1_f')
    simple_plot(trunk.get_h_cumulative(), trunk.get_v(),
                'Length [m]', 'Velocity [m/s]',
                'System with 3 Elements - Example 1', 'system1_v')
    simple_plot(trunk.get_h_cumulative(), trunk.get_q_in(),
                'Length [m]', 'Flow rate [m3/d]',
                'System with 3 Elements - Example 1', 'system1_q')
    hl_m = [100*hl/h for (hl,h) in zip(trunk.get_hl(),trunk.get_h())]
    simple_plot(trunk.get_h_cumulative(), hl_m,
                'Length [m]', 'Head loss / linear distance [m/100 m]',
                'System with 3 Elements - Example 1', 'system1_hl')

def system_ex1_sensibility():
    print('System with 3 Elements - Sensibility')

    trunk = define_system_ex1(debug_mode=False)
    trunk.set_p_out(10.)
    trunk.set_t_out(50.)
    trunk.ipr.set_pi(40.)
    trunk.ipr.set_pr(340.)

    p_out = [2., 5., 10., 15., 20., 30.]
    q = []
    for p in p_out:
        trunk.set_p_out(p)
        trunk.solve_operation_point()
        q.append(trunk.ipr.get_q(trunk.get_pwf()))
    _ = plt.figure()
    plt.plot(p_out, q, 'o-b')
    plt.grid()
    plt.xlabel('P surface [bar]')
    plt.ylabel('Q [std m3/d]')
    plt.title('System with 3 Elements - Sensibility')
    save_plot(plt,'system1_p_out')

    trunk.set_p_out(10.)
    d_list = [4., 5., 6., 7., 8.]
    q_d = []
    for d in d_list:
        for element in trunk._elements:
            element.set_d(d * 2.54/100.)
        trunk.solve_operation_point()
        q_d.append(trunk.ipr.get_q(trunk.get_pwf()))
    _ = plt.figure()
    plt.plot(d_list, q_d, 'o-b')
    plt.grid()
    plt.xlabel('Pipe diameter [in]')
    plt.ylabel('Q [std m3/d]')
    plt.title('System with 3 Elements - Sensibility')
    save_plot(plt,'system1_d')

if __name__ == "__main__":
    horizontal_test()
    horizontal_divided_test()
    horizontal_two_elements_test()
    vertical_test()
    vertical_divided_test()
    vertical_two_elements_test()
    vertical_sensibility_test()
    system_ex1()
    system_ex1_vfp()
    system_ex1_sensibility()

    pass
