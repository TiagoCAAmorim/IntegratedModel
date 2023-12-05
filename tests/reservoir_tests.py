import os
from context import reservoir
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

def simple_2D_2f(i, j):
    model = reservoir.Simple2D_OW()
    model.set_p_init(340.)
    model.set_k(1000.)
    model.set_phi(0.15)

    model.set_ni(i)
    model.set_nj(j)
    model.set_hk(30.)
    model.set_hi(600.)
    model.set_hj(model.get_hi() * model.get_nj() / model.get_ni())

    model.set_bo(1.01)
    model.set_uo(130.)
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

    model.set_rw_inj(4 * 2.54 / 100.)
    model.set_skin_inj(0.)
    model.set_qwi(350.)

    model.set_t_end(365.25 * 3.)
    model.set_max_dsw(0.005)
    model.set_max_dpr(5.)
    model.set_max_dt(10.)
    model.set_min_dt(0.1)

    # model.initialize()
    model.run_simulation(0.10)

    t = model.get_t()
    dt = [t[i] - t[i - 1] for i in range(1, len(t))]
    simple_plot(t[1:], dt, "t [d]", "delta t [d]", "Time-steps", "sim_dt")

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
    plt.xlabel('t')
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
    plt.xlabel('t')
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
    plt.xlabel('t')
    plt.ylabel('[m3/d]')
    plt.title('Simulation')
    save_plot(plt,'sim_well')

    if model.get_ni() > 1 and model.get_nj() > 1:
        _ = plt.figure()
        sw = model.get_sw_map(-1)
        plt.contourf(sw)
        plt.colorbar(label='Contour levels')
        plt.title('Sw Map')
        save_plot(plt,'sim_final_sw')


if __name__ == "__main__":
    for i in [5]: #[3, 5, 7, 9, 10]: #, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100]:
        # print(f'i = {i}, j = {1}')
        # simple_2D_2f(i,1)
        print(f'i = {i}, j = {i}')
        simple_2D_2f(i,i)
    pass
