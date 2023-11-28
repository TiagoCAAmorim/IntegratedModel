import os
from context import reservoir
import matplotlib.pyplot as plt

debug_mode = True

path = os.path.abspath(os.path.dirname(__file__))
def save_plot(plt, name):
    plt.savefig(path+'/plots/sim/'+name+'.png')
    # plt.show()

def simple_plot(x,y, x_label, y_label, title, file):
    _ = plt.figure()
    plt.plot(x, y)
    plt.grid()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    save_plot(plt,file)

def simple_2D_2f():
    model = reservoir.Simple2D_OW()
    model.set_p_init(340.)
    model.set_k(1000.)
    model.set_phi(0.3)

    model.set_hi(600.)
    model.set_hj(600.)
    model.set_hk(30.)
    model.set_ni(5)
    model.set_nj(5)

    # model.set_bo(1.01)
    # model.set_uo(130.)
    model.pvt.set_api(15.)
    model.pvt.set_gor(2.)
    model.pvt.set_dg(0.6)
    model.pvt.set_t(0.6)

    model.set_bw(1.)
    model.set_uw(1.)

    model.kr.sat.set_swi(0.20)
    model.kr.sat.set_swc(0.20)
    model.kr.sat.set_sorw(0.16)
    model.kr.set_nw(2.0)
    model.kr.set_now(1.5)
    model.kr.set_krw_max(0.63)
    model.kr.set_kro_max(1.0)

    model.set_rw(4 * 2.54 / 100.)
    model.set_skin(0.)
    model.set_pwf(330.)
    model.set_qwi(350.)
    model.set_t_end(300. * 5.)

    # model.initialize()
    model.run_simulation(2.0)

    t = model.get_t()
    s1 = model.get_sw_cell(0,0)
    s2 = model.get_sw_cell(int(model.get_ni()/2),int(model.get_nj()/2))
    s3 = model.get_sw_cell(model.get_ni()-1,model.get_nj()-1)

    _ = plt.figure()
    plt.plot(t, s1, label="Sw1")
    plt.plot(t, s2, label="Sw2")
    plt.plot(t, s3, label="Sw3")

    ax = plt.gca()
    ax.legend()
    plt.grid()
    plt.xlabel('t [d]')
    plt.ylabel('Sw')
    plt.title('Simulation')
    save_plot(plt,'sim_sw')

    p1 = model.get_pr_cell(0,0)
    p2 = model.get_pr_cell(int(model.get_ni()/2),int(model.get_nj()/2))
    p3 = model.get_pr_cell(model.get_ni()-1,model.get_nj()-1)

    _ = plt.figure()
    plt.plot(t, p1, label="Pr1")
    plt.plot(t, p2, label="Pr2")
    plt.plot(t, p3, label="Pr3")

    ax = plt.gca()
    ax.legend()
    plt.grid()
    plt.xlabel('t [d]')
    plt.ylabel('Pr [bar]')
    plt.title('Simulation')
    save_plot(plt,'sim_pr')

    qo = model.get_well_qo()
    qw = model.get_well_qw()

    _ = plt.figure()
    plt.plot(t, qo, label="Qo")
    plt.plot(t, qw, label="Qw")

    ax = plt.gca()
    ax.legend()
    plt.grid()
    plt.xlabel('t [d]')
    plt.ylabel('[m3/d]')
    plt.title('Simulation')
    save_plot(plt,'sim_well')

    simple_plot(t, model.get_voil(), 't [d]', 'Voil [MMm3]', 'Simulation', 'sim_voil')

    if model.get_ni() > 1 and model.get_nj() > 1:
        _ = plt.figure()
        sw = model.get_sw_map(-1)
        plt.contourf(sw)
        plt.colorbar(label='Contour levels')
        plt.title('Sw Map: end of simulation')
        save_plot(plt,'sim_sw_final')

        _ = plt.figure()
        sw = model.get_sw_map(int(len(t)/2))
        plt.contourf(sw)
        plt.colorbar(label='Contour levels')
        plt.title('Sw Map: mid of simulation')
        save_plot(plt,'sim_sw_mid')

        _ = plt.figure()
        sw = model.get_sw_map(1)
        plt.contourf(sw)
        plt.colorbar(label='Contour levels')
        plt.title('Sw Map: start of simulation')
        save_plot(plt,'sim_sw_start')

        _ = plt.figure()
        pr = model.get_pr_map(-1)
        plt.contourf(pr)
        plt.colorbar(label='Contour levels')
        plt.title('Pr Map: end of simulation')
        save_plot(plt,'sim_pr_final')

        _ = plt.figure()
        pr = model.get_pr_map(1)
        plt.contourf(pr)
        plt.colorbar(label='Contour levels')
        plt.title('Pr Map: start of simulation')
        save_plot(plt,'sim_pr_start')

        _ = plt.figure()
        pr = model.get_pr_map(int(len(t)/2))
        plt.contourf(pr)
        plt.colorbar(label='Contour levels')
        plt.title('Pr Map: Mid of simulation')
        save_plot(plt,'sim_pr_mid')


if __name__ == "__main__":
    simple_2D_2f()
    pass
