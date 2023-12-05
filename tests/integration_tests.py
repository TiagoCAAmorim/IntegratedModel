import os
from context import integrated_model
import matplotlib.pyplot as plt

debug_mode = True

path = os.path.abspath(os.path.dirname(__file__))
def save_plot(plot, name):
    plot.savefig(path+'/plots/sim/'+name+'.png')
    plot.close()

def simple_plot(x,y, x_label, y_label, title, file):
    _ = plt.figure()
    plt.plot(x, y)
    plt.grid()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    save_plot(plt,file)

def set_system_prod(line):
    line.set_d(4. * 2.54/100.)
    line.set_e(0.6 / 1000.)
    line.set_number_divisions(100)

    line.add_element()
    line.current_element.set_h(1600.)
    line.current_element.set_z_in(-1600. + -1320.)
    line.current_element.set_z_out(-1320.)
    line.current_element.set_number_divisions(5)

    line.add_element(True)  #ESP

    line.add_element()
    line.current_element.set_h(500.)
    line.current_element.set_z_in(-1320.)
    line.current_element.set_z_out(-1320.)
    line.current_element.set_number_divisions(5)

    line.add_element()
    line.current_element.set_h(1320.)
    line.current_element.set_z_in(-1320.)
    line.current_element.set_z_out(0.)
    line.current_element.set_number_divisions(5)

def set_system_inj(line):
    line.set_d(4. * 2.54/100.)
    line.set_e(0.6 / 1000.)
    line.set_number_divisions(100)

    line.add_element()
    line.current_element.set_h(1320.)
    line.current_element.set_z_in(0.)
    line.current_element.set_z_out(-1320.)
    line.current_element.set_number_divisions(5)

    line.add_element()
    line.current_element.set_h(500.)
    line.current_element.set_z_in(-1320.)
    line.current_element.set_z_out(-1320.)
    line.current_element.set_number_divisions(5)

    line.add_element()
    line.current_element.set_h(1600.)
    line.current_element.set_z_in(-1320.)
    line.current_element.set_z_out(-1600. + -1320.)
    line.current_element.set_number_divisions(5)

def set_pvt(pvt):
    pvt.set_api(15.)
    pvt.set_gor(2.)
    pvt.set_dg(0.6)
    pvt.set_emulsion(True)

def set_reservoir(model):
    # model.set_p_init(340.)
    model.set_k(1000.)
    model.set_phi(0.15)

    model.set_hi(600.)
    model.set_hj(600.)
    model.set_hk(80.)
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
    model.set_rw_inj(4 * 2.54 / 100.)
    model.set_skin_inj(0.)
    # model.set_pwf(330.)
    model.set_qwi(1000.)

    model.set_t_end(5.)
    model.set_max_dsw(0.005)
    model.set_max_dpr(5.)
    model.set_max_dt(10.)
    model.set_min_dt(0.1)
    model.set_first_cell_dsw(0.05)

def test1():
    model = integrated_model.Integration(debug=False)
    model.set_file_name('results.txt')
    model.set_out_folder(path+'/plots/integration/')

    set_pvt(model.pvt)
    set_reservoir(model.reservoir)

    set_system_prod(model.flow_prod)

    model.flow_prod.set_esp_delta_p(50.)
    model.flow_prod.set_esp_eff(0.6)
    model.flow_prod.set_esp_eff_coef(200.)

    set_system_inj(model.flow_inj)

    model.water_pump.set_eff(0.75)

    model.separator.set_ks(0.03)
    model.separator.set_d(0.75)

    model.gas_compressor.set_eff(0.76)
    model.gas_compressor.set_k(1.4)
    model.gas_compressor.set_p_out(120.)

    model.set_gas_loss(0.02)

    model.emission.set_mole_pc('co2', 0.8 )
    model.emission.set_mole_pc('ch4', 95.3)
    model.emission.set_mole_pc('c2h6', 1.7)
    model.emission.set_mole_pc('c3h8', 0.5)
    model.emission.set_mole_pc('c4h10', 0.1)
    model.emission.set_mole_pc('n2', 1.6)
    model.emission.generator.set_power([0, 0.1, 10, 20, 40, 100])
    model.emission.generator.set_fuel([0, 65000, 75000, 126000, 250000, 750000])

    model.set_reservoir_t(50.)
    model.set_reservoir_p(340.)
    model.set_well_head_t(50.)
    model.set_well_head_p(20.)

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
