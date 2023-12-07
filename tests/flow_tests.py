import os
from context import flow
from context import common
import matplotlib.pyplot as plt

debug_mode = True

path = os.path.abspath(os.path.dirname(__file__))
def save_plot(plot, name):
    plot.savefig(path+'/plots/flow/'+name+'.png')
    plot.close()

def simple_plot(x,y, x_label, y_label, title, file):
    _ = plt.figure()
    plt.plot(x, y)
    plt.grid()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    save_plot(plt,file)

    common.make_columns_file(x, y, x_label, y_label, path+'/plots/flow/'+file+'.txt')

def define_common_parameters(line, diameter=6.):
    line.pvt.set_api(15.)
    line.pvt.set_gor(2.)
    line.pvt.set_dg(0.6)

    line.set_d(diameter * 2.54/100.)
    line.set_e(0.6 / 1000.)

    line.set_p_in(300.)
    line.set_t_in(50.)

    line.set_q_std(1000.)

def horizontal_test():
    print('1000 m Horizontal Line')
    line = flow.SubFlowElement()
    define_common_parameters(line)
    line.set_h(1600.)
    line.set_z_in(0.)
    line.set_z_out(0.)
    print('  Calculation from Inlet to Outlet')
    line.solve_out_flow()
    print(f'    Pressure in: {line.get_p_in():.3f} bar.')
    print(f'    Pressure out: {line.get_p_out():.3f} bar.')
    print('  Calculation from Outlet to Inlet')
    line.set_p_in(None)
    line.set_q_in(None)
    line.solve_in_flow()
    print(f'    Pressure in: {line.get_p_in():.3f} bar.')
    print(f'    Pressure out: {line.get_p_out():.3f} bar.')

def vertical_test():
    print('1600 m Vertical Line')
    line = flow.SubFlowElement()
    define_common_parameters(line)
    line.set_h(1600.)
    line.set_z_in(0.)
    line.set_z_out(1600.)
    print('  Calculation from Inlet to Outlet')
    line.solve_out_flow()
    print(f'    Pressure in: {line.get_p_in():.3f} bar.')
    print(f'    Pressure out: {line.get_p_out():.3f} bar.')
    print('  Calculation from Outlet to Inlet')
    line.set_p_in(None)
    line.set_q_in(None)
    line.solve_in_flow()
    print(f'    Pressure in: {line.get_p_in():.3f} bar.')
    print(f'    Pressure out: {line.get_p_out():.3f} bar.')

def horizontal_divided_test():
    print('1000 m Horizontal Line with divisions')
    line = flow.FlowElement(debug_mode=debug_mode)
    define_common_parameters(line)
    line.set_number_divisions(10)
    line.set_h(1600.)
    line.set_z_in(0.)
    line.set_z_out(0.)

    print('  Calculation from Inlet to Outlet')
    line.solve_out_flow()
    print(f'    Pressure in: {line.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {line.get_p_out()[-1]:.3f} bar.')

    _ = plt.figure()
    plt.plot([0] + line.get_h_cumulative(), [line.get_p_in()[0]] + line.get_p_out(), 'b-')

    print('  Calculation from Outlet to Inlet')
    line.set_p_in(None)
    line.set_q_in(None)
    line.solve_in_flow()
    print(f'    Pressure in: {line.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {line.get_p_out()[-1]:.3f} bar.')

    plt.plot([0] + line.get_h_cumulative(), line.get_p_in() + [line.get_p_out()[-1]], 'r--')
    ax = plt.gca()
    ax.legend(['Inlet to Outlet', 'Outlet to Inlet'])
    plt.grid()
    plt.xlabel('Lenght along element [m]')
    plt.ylabel('p [bar]')
    plt.title('1000 m Horizontal Line')
    save_plot(plt,'horizontal')

def vertical_divided_test():
    print('1600 m Vertical Line with divisions')
    line = flow.FlowElement(debug_mode=debug_mode)
    define_common_parameters(line)
    line.set_number_divisions(10)
    line.set_h(1600.)
    line.set_z_in(0.)
    line.set_z_out(1600.)

    print('  Calculation from Inlet to Outlet')
    line.solve_out_flow()
    print(f'    Pressure in: {line.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {line.get_p_out()[-1]:.3f} bar.')

    _ = plt.figure()
    plt.plot([0] + line.get_h_cumulative(), [line.get_p_in()[0]] + line.get_p_out())

    print('  Calculation from Outlet to Inlet')
    line.set_p_in(None)
    line.set_q_in(None)
    line.solve_in_flow()
    print(f'    Pressure in: {line.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {line.get_p_out()[-1]:.3f} bar.')

    plt.plot([0] + line.get_h_cumulative(), line.get_p_in() + [line.get_p_out()[-1]])
    ax = plt.gca()
    ax.legend(['Inlet to Outlet', 'Outlet to Inlet'])
    plt.grid()
    plt.xlabel('Lenght along element [m]')
    plt.ylabel('p [bar]')
    plt.title('1600 m Vertical Line')
    save_plot(plt,'vertical')

def vertical_sensibility_test():
    print('1600 m Vertical Line with divisions - sensibility')
    line = flow.FlowElement(debug_mode=False)
    define_common_parameters(line)
    line.set_h(1600.)
    line.set_z_in(0.)
    line.set_z_out(1600.)
    print('  Calculation from Inlet to Outlet')
    print(f'    Pressure in: {line.get_p_in()[0]:.3f} bar.')

    n_list = [pow(2,i) for i in range(10)]
    p_list = []
    for n in n_list:
        line.set_number_divisions(n)
        line.solve_out_flow()
        p_list.append(line.get_p_out()[-1])
        print(f'    Pressure out ({n} segments): {p_list[-1]:.3f} bar.')

    _ = plt.figure()
    plt.semilogx(n_list, p_list,'-ob')
    plt.grid(True, which='both')
    plt.xlabel('Number of segments in calculation')
    plt.ylabel('p out [bar]')
    plt.title('1600 m Vertical Line')
    save_plot(plt,'vertical_sensibility')

def horizontal_two_elements_test():
    print('1000 m Horizontal Line as two elements')
    line = flow.CompositeFlowElement(debug_mode=debug_mode)
    define_common_parameters(line)
    line.set_number_divisions(5)

    line.add_element()
    line.current_element.set_h(800.)
    line.current_element.set_z_in(0.)
    line.current_element.set_z_out(0.)

    line.add_element()
    line.current_element.set_h(800.)
    line.current_element.set_z_in(0.)
    line.current_element.set_z_out(0.)

    print('  Calculation from Inlet to Outlet')
    line.solve_out_flow()
    print(f'    Pressure in: {line.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {line.get_p_out()[-1]:.3f} bar.')

    _ = plt.figure()
    plt.plot([0] + line.get_h_cumulative(), [line.get_p_in()[0]] + line.get_p_out())

    print('  Calculation from Outlet to Inlet')
    line.set_p_in(None)
    line.set_q_in(None)
    line.solve_in_flow()
    print(f'    Pressure in: {line.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {line.get_p_out()[-1]:.3f} bar.')

    plt.plot([0] + line.get_h_cumulative(), line.get_p_in() + [line.get_p_out()[-1]])
    ax = plt.gca()
    ax.legend(['Inlet to Outlet', 'Outlet to Inlet'])
    plt.grid()
    plt.xlabel('Lenght along element [m]')
    plt.ylabel('p [bar]')
    plt.title('1000 m Horizontal Line as Two Elements')
    save_plot(plt,'horizontal2')

def vertical_two_elements_test():
    print('1600 m Vetical Line as two elements')
    line = flow.CompositeFlowElement(debug_mode=debug_mode)
    define_common_parameters(line)
    line.set_number_divisions(5)

    line.add_element()
    line.current_element.set_h(800.)
    line.current_element.set_z_in(0.)
    line.current_element.set_z_out(800.)

    line.add_element()
    line.current_element.set_h(800.)
    line.current_element.set_z_in(800.)
    line.current_element.set_z_out(1600.)

    print('  Calculation from Inlet to Outlet')
    line.solve_out_flow()
    print(f'    Pressure in: {line.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {line.get_p_out()[-1]:.3f} bar.')
    _ = plt.figure()
    plt.plot([0] + line.get_h_cumulative(), [line.get_p_in()[0]] + line.get_p_out())

    print('  Calculation from Outlet to Inlet')
    line.set_p_out(line._elements[-1].get_p_out()[-1])
    line.set_q_out(line._elements[-1].get_q_out()[-1])
    line.set_p_in(None)
    line.set_q_in(None)
    line.solve_in_flow()
    print(f'    Pressure in: {line.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {line.get_p_out()[-1]:.3f} bar.')

    plt.plot([0] + line.get_h_cumulative(), line.get_p_in() + [line.get_p_out()[-1]])
    ax = plt.gca()
    ax.legend(['Inlet to Outlet', 'Outlet to Inlet'])
    plt.grid()
    plt.xlabel('Lenght along element [m]')
    plt.ylabel('p [bar]')
    plt.title('1600 m Vetical Line as Two Elements')
    save_plot(plt,'vertical2')

def define_system_ex1(debug_mode, dp_ESP=50., diameter=6.):
    line = flow.CompositeFlowElement(debug_mode=debug_mode)
    define_common_parameters(line, diameter)
    line.set_number_divisions(100)

    line.add_element()
    line.current_element.set_h(1600.)
    line.current_element.set_z_in(-1600. + -1320.)
    line.current_element.set_z_out(-1320.)
    line.current_element.set_number_divisions(50)

    line.add_element(True) #ESP
    line.current_element.set_delta_p(dp_ESP)

    line.add_element()
    line.current_element.set_h(500.)
    line.current_element.set_z_in(-1320.)
    line.current_element.set_z_out(-1320.)
    line.current_element.set_number_divisions(20)

    line.add_element()
    line.current_element.set_h(1320.)
    line.current_element.set_z_in(-1320.)
    line.current_element.set_z_out(0.)
    line.current_element.set_number_divisions(50)

    return line

def system_ex1(wfr=0.0, dp_ESP=50.0, diameter=6.):
    print(f'System with 3 Elements - Example 1: wfr = {wfr*100:0.0f}%')

    line = define_system_ex1(debug_mode=debug_mode, dp_ESP=dp_ESP,  diameter=diameter)
    line.pvt.set_wfr(wfr)
    line.pvt.set_emulsion(True)
    line.set_esp_eff(0.5)
    line.update_pvt()
    print('  Calculation from Inlet to Outlet')
    line.solve_out_flow()
    print(f'    Pressure in: {line.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {line.get_p_out()[-1]:.3f} bar.')
    print(f'    ESP Power demand: {line.get_esp_power():.3f} MW')
    print(f'    ESP Efficiency: {line.get_esp_true_eff()*100.:.2f}%')

    _ = plt.figure()
    plt.plot([0] + line.get_h_cumulative(), [line.get_p_in()[0]] + line.get_p_out())

    print('  Calculation from Outlet to Inlet')
    line.set_p_out(line._elements[-1].get_p_out()[-1])
    line.set_q_out(line._elements[-1].get_q_out()[-1])
    line.set_p_in(None)
    line.set_q_in(None)
    line.solve_in_flow()
    print(f'    Pressure in: {line.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {line.get_p_out()[-1]:.3f} bar.')
    print(f'    ESP Power demand: {line.get_esp_power():.3f} MW')
    print(f'    ESP Efficiency: {line.get_esp_true_eff()*100.:.2f}%')

    plt.plot([0] + line.get_h_cumulative(), line.get_p_in() + [line.get_p_out()[-1]])

    plt.plot(line.get_h_cumulative(), line.get_p_bubble())

    ax = plt.gca()
    ax.legend(['Inlet to Outlet', 'Outlet to Inlet','Bubble pressure'])
    plt.grid()
    plt.xlabel('Lenght along element [m]')
    plt.ylabel('p [bar]')
    plt.title(f'System with 3 Elements: wfr = {wfr*100:0.0f}%')
    save_plot(plt,f'system1_{wfr*100:0.0f}pc')
    filename = path+'/plots/flow/'+f'system1_{wfr*100:0.0f}pc_{dp_ESP:0.0f}bar_{diameter:0.0f}pol'+'.txt'
    common.make_columns_file([0] + line.get_h_cumulative(), line.get_p_in() + [line.get_p_out()[-1]], "Length_m", "Pressure_bar", filename)

def system_ex1_emulsion():
    print('System with 3 Elements - Example 1: Emulsion')

    line = define_system_ex1(debug_mode=False)
    line.pvt.set_emulsion(True)
    line.update_pvt()
    print('  Calculation from Inlet to Outlet')

    n = 201
    wfr_list = [i/(n-1) for i in range(n)]
    phead = []
    for wfr in wfr_list:
        line.pvt.set_wfr(wfr)
        line.update_pvt()
        line.solve_out_flow()
        phead.append(line.get_p_out()[-1])
        print(f'  WCUT = {wfr*100.:.1f}%\tPhead = {phead[-1]:.3f} bar')

    simple_plot(wfr_list, phead, 'Water Cut [-]', 'Head pressure [bar]', 'Sensibility to Emulsion', 'system1_emulsion')

def system_ex1_vfp():
    print('System with 3 Elements - (q,p) plot')

    line = define_system_ex1(debug_mode=False)
    line.set_p_out(10.)
    line.set_t_out(50.)
    line.ipr.set_pi(40.)
    line.ipr.set_pr(340.)

    q_std = [10., 100., 200., 500., 600., 700., 800., 900., 1000., 1500., 2000., 2500., 2600., 2700., 2800., 2900., 3000., 3500., 4000.]
    pwf = []
    q_ipr = []
    for q in q_std:
        line.set_q_std(q)
        line.solve_in_flow()
        pwf.append(line.get_p_in()[0])
        q_ipr.append(line.ipr.get_q(pwf[-1]))

    line.solve_operation_point()
    print(f'Operation point: pwf = {line.get_pwf():.3f} bar, q = {line.ipr.get_q(line.get_pwf()):.3f} m3/d')

    _ = plt.figure()
    plt.plot(q_std, pwf, '-b')
    plt.plot(q_ipr, pwf, '-r')
    plt.plot(line.ipr.get_q(line.get_pwf()), line.get_pwf(), 'o')
    ax = plt.gca()
    ax.legend(['VFP', 'IPR', 'Operation'])
    plt.grid()
    plt.xlabel('Q [std m3/d]')
    plt.ylabel('Pwf [bar]')
    plt.title('System with 3 Elements')
    save_plot(plt,'system1_qp')

    print('System with 3 Elements - Flow Calculation on the Operation Point')
    line.set_q_std(line.ipr.get_q(line.get_pwf()))
    line.solve_in_flow()
    print(f'    Pressure in: {line.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {line.get_p_out()[-1]:.3f} bar.')

    _ = plt.figure()
    plt.plot([0] + line.get_h_cumulative(), [line.get_p_in()[0]] + line.get_p_out())
    plt.plot(line.get_h_cumulative(), line.get_p_bubble())
    ax = plt.gca()
    ax.legend(['Pressure', 'Bubble pressure'])
    plt.grid()
    plt.xlabel('Length [m]')
    plt.ylabel('P [bar]')
    plt.title('System with 3 Elements')
    save_plot(plt,'system1_operation')

    simple_plot(line.get_h_cumulative(), line.get_u(),
                'Length [m]', 'uo [cP]',
                'System with 3 Elements', 'system1_uo')
    simple_plot(line.get_h_cumulative(), line.get_rs(),
                'Length [m]', 'rs [m3/m3]',
                'System with 3 Elements', 'system1_rs')
    simple_plot(line.get_h_cumulative(), line.get_b(),
                'Length [m]', 'bo [-]',
                'System with 3 Elements', 'system1_bo')
    simple_plot(line.get_h_cumulative(), line.get_re(),
                'Length [m]', 'Reynolds number',
                'System with 3 Elements', 'system1_Re')
    simple_plot(line.get_h_cumulative(), line.get_f(),
                'Length [m]', 'friction factor [-]',
                'System with 3 Elements', 'system1_f')
    simple_plot(line.get_h_cumulative(), line.get_v(),
                'Length [m]', 'Velocity [m/s]',
                'System with 3 Elements', 'system1_v')
    simple_plot(line.get_h_cumulative(), line.get_q_in(),
                'Length [m]', 'Flow rate [m3/d]',
                'System with 3 Elements', 'system1_q')
    hl_m = [100*hl/(h+1e-20) for (hl,h) in zip(line.get_hl(),line.get_h())]
    simple_plot(line.get_h_cumulative(), hl_m,
                'Length [m]', 'Head loss / linear distance [m/100 m]',
                'System with 3 Elements', 'system1_hl')

def system_ex1_sensibility():
    print('System with 3 Elements - Sensibility')

    line = define_system_ex1(debug_mode=False)
    line.set_p_out(10.)
    line.set_t_out(50.)
    line.ipr.set_pi(40.)
    line.ipr.set_pr(340.)

    p_out = [2., 5., 10., 15., 20., 30.]
    q = []
    for p in p_out:
        line.set_p_out(p)
        line.solve_operation_point()
        q.append(line.ipr.get_q(line.get_pwf()))
    _ = plt.figure()
    plt.plot(p_out, q, 'o-b')
    plt.grid()
    plt.xlabel('P surface [bar]')
    plt.ylabel('Q [std m3/d]')
    plt.title('System with 3 Elements')
    save_plot(plt,'system1_p_out')

    line.set_p_out(10.)
    d_list = [4., 5., 6., 7., 8.]
    q_d = []
    for d in d_list:
        for element in line._elements:
            element.set_d(d * 2.54/100.)
        line.solve_operation_point()
        q_d.append(line.ipr.get_q(line.get_pwf()))
    _ = plt.figure()
    plt.plot(d_list, q_d, 'o-b')
    plt.grid()
    plt.xlabel('Pipe diameter [in]')
    plt.ylabel('Q [std m3/d]')
    plt.title('System with 3 Elements')
    save_plot(plt,'system1_d')

def define_system_ex2(debug_mode, diameter=6.):
    line = flow.CompositeFlowElement(debug_mode=debug_mode)
    define_common_parameters(line, diameter)
    line.pvt.set_wfr(1.)
    line.set_number_divisions(100)

    line.add_element()
    line.current_element.set_h(1320.)
    line.current_element.set_z_in(0.)
    line.current_element.set_z_out(-1320.)
    line.current_element.set_number_divisions(132)

    line.add_element()
    line.current_element.set_h(500.)
    line.current_element.set_z_in(-1320.)
    line.current_element.set_z_out(-1320.)
    line.current_element.set_number_divisions(5)

    line.add_element()
    line.current_element.set_h(1600.)
    line.current_element.set_z_in(-1320.)
    line.current_element.set_z_out(-1600. + -1320.)
    line.current_element.set_number_divisions(160)

    return line

def system_ex2(diameter=6.):
    print('System with 3 Elements - Example 2: water injector')

    line = define_system_ex2(debug_mode=debug_mode)

    line.set_p_in(146.)
    line.set_t_out(50.)
    line.set_q_std(350. * 24.)

    print('  Calculation from Inlet to Outlet')
    line.solve_out_flow()
    print(f'    Pressure in: {line.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {line.get_p_out()[-1]:.3f} bar.')

    _ = plt.figure()
    plt.plot([0] + line.get_h_cumulative(), [line.get_p_in()[0]] + line.get_p_out())

    print('  Calculation from Outlet to Inlet')
    line.set_p_out(line._elements[-1].get_p_out()[-1])
    line.set_q_out(line._elements[-1].get_q_out()[-1])
    line.set_p_in(None)
    line.set_q_in(None)
    line.solve_in_flow()
    print(f'    Pressure in: {line.get_p_in()[0]:.3f} bar.')
    print(f'    Pressure out: {line.get_p_out()[-1]:.3f} bar.')

    plt.plot([0] + line.get_h_cumulative(), line.get_p_in() + [line.get_p_out()[-1]])

    plt.plot(line.get_h_cumulative(), line.get_p_bubble())

    ax = plt.gca()
    ax.legend(['Inlet to Outlet', 'Outlet to Inlet','Bubble pressure'])
    plt.grid()
    plt.xlabel('Lenght along element [m]')
    plt.ylabel('p [bar]')
    plt.title('System with 3 Elements: Qwi')
    save_plot(plt,f'system2_{diameter:0.0f}_pol')
    common.make_columns_file(list1=[0] + line.get_h_cumulative(),
                             list2=line.get_p_in() + [line.get_p_out()[-1]],
                             column_name1="Length_m",
                             column_name2="Pressure_bar",
                             file_name=path+f'/plots/flow/system2_{diameter:0.0f}_pol.txt')

if __name__ == "__main__":
    horizontal_test()
    horizontal_divided_test()
    horizontal_two_elements_test()
    vertical_test()
    vertical_divided_test()
    vertical_two_elements_test()
    vertical_sensibility_test()

    system_ex1(0.0)
    system_ex1(0.1)
    system_ex1(0.2)
    system_ex1(0.3)
    system_ex1(0.4)

    system_ex1(0.2, 0.)
    system_ex1(0.2, 50.)
    system_ex1(0.2, 100.)

    system_ex1(0.2, 100., 4.)
    system_ex1(0.2, 100., 5.)
    system_ex1(0.2, 100., 4.)
    system_ex1(0.2, 100., 6.)
    system_ex1(0.2, 100., 8.)

    system_ex1_emulsion()
    system_ex1_vfp()
    system_ex1_sensibility()

    system_ex2(4.)
    system_ex2(6.)
    system_ex2(8.)
