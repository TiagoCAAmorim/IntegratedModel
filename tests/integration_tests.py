import os
from context import integration
import matplotlib.pyplot as plt

debug_mode = True

path = os.path.abspath(os.path.dirname(__file__))
def save_plot(plt, name):
    plt.savefig(path+'/plots/integration/'+name+'.png')
    # plt.show()

def simple_plot(x,y, x_label, y_label, title, file):
    _ = plt.figure()
    plt.plot(x, y)
    plt.grid()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    save_plot(plt,file)

def set_system_prod(line):
    line.set_d(6. * 2.54/100.)
    line.set_e(0.6 / 1000.)
    line.set_number_divisions(100)

    line.add_element()
    line.current_element.set_h(1600.)
    line.current_element.set_z_in(-1600. + -1320.)
    line.current_element.set_z_out(-1320.)
    line.current_element.set_number_divisions(160)

    line.add_element()
    line.current_element.set_h(500.)
    line.current_element.set_z_in(-1320.)
    line.current_element.set_z_out(-1320.)
    line.current_element.set_number_divisions(5)

    line.add_element()
    line.current_element.set_h(1320.)
    line.current_element.set_z_in(-1320.)
    line.current_element.set_z_out(0.)
    line.current_element.set_number_divisions(132)

def set_system_inj(line):
    line.set_d(6. * 2.54/100.)
    line.set_e(0.6 / 1000.)
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

def set_pvt(pvt):
    pvt.set_api(15.)
    pvt.set_gor(2.)
    pvt.set_dg(0.6)

def set_reservoir(model):
    # model.set_p_init(340.)
    model.set_k(1000.)
    model.set_phi(0.3)

    model.set_hi(300.)
    model.set_hj(300.)
    model.set_hk(20.)
    model.set_ni(5)
    model.set_nj(5)

    # model.set_bo(1.01)
    # model.set_uo(130.)
    # model.set_bw(1.)
    # model.set_uw(1.)

    model.kr.sat.set_swi(0.20)
    model.kr.sat.set_swc(0.20)
    model.kr.sat.set_sorw(0.16)
    model.kr.set_nw(2.0)
    model.kr.set_now(1.5)
    model.kr.set_krw_max(0.63)
    model.kr.set_kro_max(1.0)

    model.set_rw(4 * 2.54 / 100.)
    model.set_skin(0.)
    # model.set_pwf(330.)
    model.set_qwi(350.)
    model.set_t_end(300. * 2.)

def test1():
    model = integration.Integration(debug=True)

    set_pvt(model.pvt)
    set_reservoir(model.reservoir)

    set_system_prod(model.flow_prod)
    set_system_inj(model.flow_inj)

    model.water_pump.set_eff(0.65)
    model.separator.set_ks(0.03)
    model.separator.set_d(0.75)

    model.gas_compressor.set_eff(0.76)
    model.gas_compressor.set_k(1.4)

    model.emission.set_mole_pc('co2', 0.8 )
    model.emission.set_mole_pc('ch4', 95.3)
    model.emission.set_mole_pc('c2h6', 1.7)
    model.emission.set_mole_pc('c3h8', 0.5)
    model.emission.set_mole_pc('c4h10', 0.1)
    model.emission.set_mole_pc('n2', 1.6)
    model.emission.turbine.set_rates([0, 1,  1e6, 2.0e6, 2.1e6, 2.2e6, 2.3e6, 2.4e6, 2.5e6, 2.6e6, 2.7e6, 2.8e6, 2.9e6, 3.0e6, 5.0e6])
    model.emission.turbine.set_power([0, 4.1, 4.1, 4.1, 4.1, 4.4, 4.8, 5.1, 5.4, 5.8, 6.1, 6.4, 6.8, 7.1, 14.2])

    model.set_reservoir_t(50.)
    model.set_reservoir_p(340.)
    model.set_well_head_t(50.)
    model.set_well_head_p(20.)

    # model.initialize()
    # model.advance_simulation(0.1)

    model.run_simulation(2.0)

    t = model.reservoir.get_t()
    p1 = model.reservoir.get_pr_cell(0,0)
    p2 = model.reservoir.get_pr_cell(int(model.reservoir.get_ni()/2),int(model.reservoir.get_nj()/2))
    p3 = model.reservoir.get_pr_cell(model.reservoir.get_ni()-1,model.reservoir.get_nj()-1)

    _ = plt.figure()
    plt.plot(t, p1, label="Pr1")
    plt.plot(t, p2, label="Pr2")
    plt.plot(t, p3, label="Pr3")

    ax = plt.gca()
    ax.legend()
    plt.grid()
    plt.xlabel('t')
    plt.ylabel('Pr [bar]')
    plt.title('Simulation')
    save_plot(plt,'sim_pr')

    # model.run_simulation(2.0)

        # pump = topside.WaterPump()
    # pump.set_qw(350. * 24.)



if __name__ == "__main__":
    test1()
    pass
