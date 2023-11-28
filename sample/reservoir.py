# import math
import numpy as np
import relative_permeability
# import pvt
from tqdm import tqdm

unit_conv = 0.00852702 # units: bar, mD, cP, m, m3/d

class Simple2D_OW:

    def __init__(self):
        self._ni = None
        self._nj = None
        self._nk = 1
        self._hi = None
        self._hj = None
        self._hk = None

        self._phi = None
        self._k = None
        self._p_init = None
        self.kr = relative_permeability.Corey()
        # self.pvt = pvt.PVT()
        self._bo = None
        self._bw = None
        self._uo = None
        self._uw = None

        self._qwi = None
        self._rw = None
        self._skin = 0.
        self._pwf = None
        self._wi = None

        self._max_dsw = None
        self._max_dp = None
        self._max_dt = None
        self._min_dt = None
        self._t_end = None


        self._di_mat = None
        self._dj_mat = None
        self._phi_mat = None
        self._k_mat = None
        self._pr_mat = None
        self._sw_mat = None

        self._ncells = None
        self._nvars = None
        self._t_list = []
        self._x_list = []
        self._x_current = None
        self._a = None
        self._b = None


    def set_ni(self, value):
        self._ni = value
    def set_nj(self, value):
        self._nj = value
    def set_hi(self, value):
        self._hi = value
    def set_hj(self, value):
        self._hj = value
    def set_hk(self, value):
        self._hk = value

    def set_phi(self, value):
        self._phi = value
    def set_k(self, value):
        self._k = value
    def set_p_init(self, value):
        self._p_init = value

    def set_bo(self, value):
        self._bo = value
    def set_bw(self, value):
        self._bw = value
    def set_uo(self, value):
        self._uo = value
    def set_uw(self, value):
        self._uw = value

    def set_qwi(self, value):
        self._qwi = value
    def set_rw(self, value):
        self._rw = value
    def set_skin(self, value):
        self._skin = value
    def set_pwf(self, value):
        self._pwf = value

    def set_max_dsw(self, value):
        self._max_dsw = value
    def set_max_dp(self, value):
        self._max_dp = value
    def set_max_dt(self, value):
        self._max_dt = value
    def set_min_dt(self, value):
        self._min_dt = value
    def set_t_end(self, value):
        self._t_end = value


    def get_ni(self):
        return self._ni
    def get_nj(self):
        return self._nj
    def get_hi(self):
        return self._hi
    def get_hj(self):
        return self._hj
    def get_hk(self):
        return self._hk

    def get_phi(self):
        return self._phi
    def get_k(self):
        return self._k
    def get_p_init(self):
        return self._p_init

    def get_bo(self):
        return self._bo
    def get_bw(self):
        return self._bw
    def get_uo(self):
        return self._uo
    def get_uw(self):
        return self._uw

    def get_qwi(self):
        return self._qwi
    def get_rw(self):
        return self._rw
    def get_skin(self):
        return self._skin
    def get_pwf(self):
        return self._pwf

    def get_max_dsw(self):
        return self._max_dsw
    def get_max_dp(self):
        return self._max_dp
    def get_max_dt(self):
        return self._max_dt
    def get_min_dt(self):
        return self._min_dt
    def get_t_end(self):
        return self._t_end

    def reset_sim(self):
        self._t_list = []
        self._x_list = []

    def initialize(self):
        self._di_mat = np.full((self.get_ni(), self.get_nj()), self.get_hi() / self.get_ni())
        self._dj_mat = np.full((self.get_ni(), self.get_nj()), self.get_hj() / self.get_nj())
        self._phi_mat = np.full((self.get_ni(), self.get_nj()), self.get_phi())
        self._k_mat = np.full((self.get_ni(), self.get_nj()), self.get_k())
        self._pr_mat = np.full((self.get_ni(), self.get_nj()), self.get_p_init())
        self._sw_mat = np.full((self.get_ni(), self.get_nj()), self.kr.sat.get_swi())

        self._ncells = self.get_ni() * self.get_nj()
        self._nvars = 2 * self._ncells

    def start_simulation(self):
        a = self._dj_mat[-1,-1] / self._di_mat[-1,-1]
        ro = self._di_mat[-1,-1] * np.exp(-(a*np.pi - np.log(a))/(1. + a*a))
        self._wi = unit_conv * 2. * np.pi * self._k_mat[-1, -1] * self.get_hk() / (np.log(ro/self.get_rw()) + self.get_skin())

        self._t_list = [0.]
        x = np.zeros(self._nvars)
        x[::2] = self._pr_mat.flatten()
        x[1::2] = self._sw_mat.flatten()
        x = x.reshape((self._nvars, 1))
        self._x_list.append(x.copy())

    def get_cell_number(self, i, j):
        return i+1 + j * self.get_ni()

    def get_kro(self, x, i1, j1, i2, j2):
        c1 = self.get_cell_number(i1,j1)
        c2 = self.get_cell_number(i2,j2)
        if c1 == c2:
            sw1 = x[c1*2-1]
            return self.kr.get_krow_2f(sw1)
        p1 = x[c1*2-2]
        p2 = x[c2*2-2]
        if (p1 > p2):
            sw = x[c1*2-1]
        else:
            sw = x[c2*2-1]
        return self.kr.get_krow_2f(sw)

    def get_krw(self, x, i1, j1, i2, j2):
        c1 = self.get_cell_number(i1,j1)
        c2 = self.get_cell_number(i2,j2)
        if c1 == c2:
            sw1 = x[c1*2-1]
            return self.kr.get_krw_2f(sw1)
        p1 = x[c1*2-2]
        p2 = x[c2*2-2]
        if (p1 > p2):
            sw = x[c1*2-1]
        else:
            sw = x[c2*2-1]
        return self.kr.get_krw_2f(sw)

    def get_tr(self, x, i1, j1, i2, j2):
        c1 = self.get_cell_number(i1,j1)
        c2 = self.get_cell_number(i2,j2)
        k1 = self._k_mat[i1,j1]
        k2 = self._k_mat[i2,j2]
        k = 2 * k1 * k2 / (k1 + k2)
        if c1 == c2:
            return 0., 0.
        if i1 == i2:
            tr = k * self._di_mat[i1,j1] * self.get_hk() / self._dj_mat[i1,j1]
        else:
            tr = k * self._dj_mat[i1,j1] * self.get_hk() / self._di_mat[i1,j1]
        tro = unit_conv * tr * self.get_kro(x, i1, j1, i2, j2) / (self.get_bo() * self.get_uo())
        trw = unit_conv * tr * self.get_krw(x, i1, j1, i2, j2) / (self.get_bw() * self.get_uw())
        return tro, trw

    def build_k(self, x, dt):
        k = np.zeros((self._nvars, self._nvars))
        for j in range(self._nj):
            for i in range(self._ni):
                cell2 = []
                if i > 0:
                    cell2.append({'i':i-1,'j':j})
                if i < (self.get_ni()-1):
                    cell2.append({'i':i+1,'j':j})
                if j > 0:
                    cell2.append({'i':i,'j':j-1})
                if j < (self.get_nj()-1):
                    cell2.append({'i':i,'j':j+1})
                p = self.get_cell_number(i,j)
                for c in cell2:
                    tro, trw = self.get_tr(x, i, j, c['i'], c['j'])
                    p2 = self.get_cell_number(c['i'],c['j'])
                    k[2*p-2,2*p-2] -= tro
                    k[2*p-1,2*p-2] -= trw
                    k[2*p-2,2*p2-2] = tro
                    k[2*p-1,2*p2-2] = trw
                vp_dt = self._di_mat[i,j] * self._dj_mat[i,j] * self.get_hk() * self._phi_mat[i,j] / dt
                k[2*p-2,2*p-1] = vp_dt / self.get_bo()
                k[2*p-1,2*p-1] = -1. * vp_dt / self.get_bw()
        k[-2,-2] -= self._wi * self.get_kro(x, self.get_ni()-1, self.get_nj()-1, self.get_ni()-1, self.get_nj()-1) / (self.get_bo() * self.get_uo())
        k[-1,-2] -= self._wi * self.get_krw(x, self.get_ni()-1, self.get_nj()-1, self.get_ni()-1, self.get_nj()-1) / (self.get_bw() * self.get_uw())
        return k

    def build_f(self, dt):
        f = np.zeros((self._nvars, 1))
        for j in range(self._nj):
            for i in range(self._ni):
                p = self.get_cell_number(i,j)
                vp_dt = self._di_mat[i,j] * self._dj_mat[i,j] * self.get_hk() * self._phi_mat[i,j] / dt
                sw_previous = self._x_list[-1][2*p-1]
                f[2*p-2,0] = vp_dt / self.get_bo() * sw_previous
                f[2*p-1,0] = -1. * vp_dt / self.get_bw() * sw_previous
        f[1,0] -= self.get_qwi()
        f[-2,0] -= self._wi * self.get_kro(self._x_list[-1], self.get_ni()-1, self.get_nj()-1, self.get_ni()-1, self.get_nj()-1) / (self.get_bo() * self.get_uo()) * self.get_pwf()
        f[-1,0] -= self._wi * self.get_krw(self._x_list[-1], self.get_ni()-1, self.get_nj()-1, self.get_ni()-1, self.get_nj()-1) / (self.get_bw() * self.get_uw()) * self.get_pwf()
        return f

    def build_r(self, x, dt):
        k = self.build_k(x, dt)
        f = self.build_f(dt)
        r = np.dot(k, x) - f
        return r

    def solve_next_dt(self, dt):
        if len(self._x_list) == 0:
            self.initialize()
            self.start_simulation()
        x = self._x_list[-1].copy()
        n = 0
        # r = self.build_r(x, dt)
        while n < 10:
            x_last = x.copy()
            k = self.build_k(x, dt)
            f = self.build_f(dt)
            x =  np.linalg.solve(k,f)

            # if len(self._t_list) == 1:
            #     np.savetxt('x_prev_mat.csv', self._x_list[-1], delimiter=',')
            #     np.savetxt('k_mat.csv', k, delimiter=',')
            #     np.savetxt('f_mat.csv', f, delimiter=',')
            #     np.savetxt('x_mat.csv', x, delimiter=',')

            if np.linalg.norm(x-x_last) < 0.01:
                self._x_current = x
                return
            n += 1
        print("Didn't converge!")
        self._x_current = x
        return

    def try_pwf(self, pwf, dt):
        self.set_pwf(pwf)
        self.solve_next_dt(dt)
        pr = float(self._x_current[-2])
        sw = float(self._x_current[-1])
        qo = self._wi * self.kr.get_krow_2f(sw) / (self.get_bo() * self.get_uo()) * (pr - self.get_pwf())
        qw = self._wi * self.kr.get_krw_2f(sw)  / (self.get_bw() * self.get_uw()) * (pr - self.get_pwf())
        return qo, qw

    def run_simulation(self, dt, add_current_solution=False):
        if (len(self._t_list) == 0):
            self.initialize()
            self.start_simulation()
        if not add_current_solution:
            progress_bar = tqdm(total=100, desc="Progress", bar_format="{percentage:3.0f}% {elapsed} {bar}")
        t = self._t_list[-1]
        while t < self._t_end:
            dti = min(dt, self._t_end - self._t_list[-1])
            if not add_current_solution:
                self.solve_next_dt(dti)
            self._x_list.append(self._x_current)
            t = min(self._t_list[-1] + dti, self._t_end)
            self._t_list.append(t)
            if add_current_solution:
                return
            percentage_completion = min(0.999, t / self._t_end) * 100
            progress_bar.update(percentage_completion - progress_bar.n)
        progress_bar.close()
        print("End of simulation.")

    def get_t(self):
        return self._t_list

    def get_sw_cell(self,i , j):
        p = self.get_cell_number(i, j)
        sw = [x[2*p-1] for x in self._x_list]
        return sw

    def get_pr_cell(self,i , j):
        p = self.get_cell_number(i, j)
        pr = [x[2*p-2] for x in self._x_list]
        return pr

    def get_well_qo(self):
        sw = self.get_sw_cell(self.get_ni()-1, self.get_nj()-1)
        pr = self.get_pr_cell(self.get_ni()-1, self.get_nj()-1)
        qo = [self._wi * self.kr.get_krow_2f(s) / (self.get_bo() * self.get_uo()) * (p - self.get_pwf()) for p,s in zip(pr, sw)]
        qo = [float(q) for q in qo]
        return qo

    def get_well_qw(self):
        sw = self.get_sw_cell(self.get_ni()-1, self.get_nj()-1)
        pr = self.get_pr_cell(self.get_ni()-1, self.get_nj()-1)
        qw = [self._wi * self.kr.get_krw_2f(s) / (self.get_bw() * self.get_uw()) * (p - self.get_pwf()) for p,s in zip(pr, sw)]
        qw = [float(q) for q in qw]
        return qw

    def get_pr_map(self, t_index):
        x = self._x_list[t_index]
        return x[::2].flatten().reshape((self.get_ni(),self.get_nj()))

    def get_sw_map(self, t_index):
        x = self._x_list[t_index]
        return x[1::2].flatten().reshape((self.get_ni(),self.get_nj()))
