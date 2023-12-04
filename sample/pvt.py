import math
import common
import numpy as np

class PVT:

    def __init__(self):
        self._wfr = 0.

        self._api = None
        self._do = None
        self._dw = 1.0
        self._dg = None
        self._rho_air = 1.2 # kg/m3
        self._rhow = 1000. # kg/m3
        self._rhomix = None

        self._t = None
        self._p = None
        self._t_std = 20.
        self._p_std = 1.01325 # 1 atm

        self._rs = None
        self._p_bubble = None
        self._gor = None

        self._bo = None
        self._bg = None
        self._bw = 1.
        self._bmix = None

        self._bo_bubble = None
        self._co_bubble = None

        self._t_pc = None
        self._p_pc = None
        self._t_pr = None
        self._p_pr = None
        self._y_co2 = 0.
        self._y_h2s = 0.
        self._y_n2 = 0.
        self._z = None

        self._uo_do = None
        self._uo = None
        self._uw = 1.
        self._umix = None

        self._emulsion = True
        self._ronningsen_k = {
            'shear_rate':np.array([30., 100., 500.]),
            'shear_rate_log':np.log10([30., 100., 500.]),
            'k1':np.array([0.01334, 0.0412, -0.06671]),
            'k2':np.array([-0.003801, -0.002605, -0.000775]),
            'k3':np.array([4.338, 3.841, 3.484]),
            'k4':np.array([0.02698, 0.02497, 0.005])}
        self._q = None
        self._d = None

        self.variables = common.VariablesList({
            'wfr':['Water fraction', '-'],
            'api':['Oil API degree', 'oAPI'],
            'do':['Oil relative density', '-'],
            'dg':['Gas relative density', '-'],
            'dw':['Water relative density', '-'],
            'rhoo':['Oil density', 'kg/m3'],
            'rhog':['Gas density', 'kg/m3'],
            'rhow':['Water density', 'kg/m3'],
            'rhomix':['Mixture density', 'kg/m3'],
            't':['In place temperature', 'oC'],
            'p':['In place pressure', 'bar'],
            'gor':['Gas oil ratio', 'std m3/std m3'],
            'rs':['Oil solubility ratio', 'std m3/std m3'],
            'p_bubble':['Bubble point pressure', 'bar'],
            'bo':['Oil formation volume factor', '-'],
            'bg':['Gas formation volume factor', '-'],
            'bw':['Water formation volume factor', '-'],
            'bmix':['Mixture formation volume factor', '-'],
            'bo_bubble':['Oil formation volume factor at the bubble point pressure', '-'],
            'co_bubble':['Oil compressibility at the bubble point pressure', '1/bar'],
            't_pc':['Pseudo-critical temperature', 'oC'],
            'p_pc':['Pseudo-critical pressure', 'bar'],
            't_pr':['Pseudo-reducible temperature', '-'],
            'p_pr':['Pseudo-reducible pressure', '-'],
            'y_co2':['CO2 content in gas', '-'],
            'y_h2s':['H2S content in gas', '-'],
            'y_n2':['N2 content in gas', '-'],
            'z':['Gas z factor', '-'],
            'uo_do':['Dead oil viscosity', 'cp'],
            'uo':['Oil viscosity', 'cp'],
            'uw':['Water viscosity', 'cp'],
            'umix':['Mixture viscosity', 'cp'],
            'q':['Fluid rate', 'm3/s'],
            'd':['Pipe diameter', 'm'],
            })

    def copy(self):
        pvt = PVT()

        pvt._wfr = self._wfr

        pvt._api = self._api
        pvt._do = self._do
        pvt._dw = self._dw
        pvt._dg = self._dg
        pvt._rho_air = self._rho_air
        pvt._rhow = self._rhow
        pvt._rhomix = self._rhomix

        pvt._t = self._t
        pvt._p = self._p
        pvt._t_std = self._t_std
        pvt._p_std = self._p_std

        pvt._rs = self._rs
        pvt._p_bubble = self._p_bubble
        pvt._gor = self._gor

        pvt._bo = self._bo
        pvt._bg = self._bg
        pvt._bw = self._bw
        pvt._bmix = self._bmix

        pvt._bo_bubble = self._bo_bubble
        pvt._co_bubble = self._co_bubble

        pvt._t_pc = self._t_pc
        pvt._p_pc = self._p_pc
        pvt._t_pr = self._t_pr
        pvt._p_pr = self._p_pr
        pvt._y_co2 = self._y_co2
        pvt._y_h2s = self._y_h2s
        pvt._y_n2 = self._y_n2
        pvt._z = self._z

        pvt._uo_do = self._uo_do
        pvt._uo = self._uo
        pvt._uw = self._uw
        pvt._umix = self._umix

        pvt._emulsion = self._emulsion
        pvt._q = self._q
        pvt._d = self._d
        return pvt

    def _check_value(self,value, min_value, max_value):
        if value < min_value or value > max_value:
            raise NameError(f'Invalid value ({value}). Valid values: [{min_value},{max_value}].')

    def set_wfr(self, wfr):
        self._check_value(wfr,0.,1.)
        self._wfr = wfr
    def set_api(self, api):
        self._check_value(api,1.,100.)
        self._api = api
        self._do = 141.5 / (131.5 + self._api)
    def set_do(self, do):
        self._check_value(do,0.01,10.)
        self._do = do
        self._api = 141.5 / self._do - 131.5
    def set_rho(self, rhoo):
        self._check_value(rhoo,10.,10000.)
        self.set_do(rhoo / self._rhow)
    def set_dg(self, dg):
        self._check_value(dg,0.1,10.)
        self._dg = dg
    def set_rhog(self, rhog):
        self._check_value(rhog / self._rho_air,0.1,10.)
        self._dg = rhog / self._rho_air
    def set_dw(self, dw):
        self._check_value(dw,0.01,10.)
        self._dw = dw
    def set_rhow(self, rhow):
        self._check_value(rhow,10.,10000.)
        self._dw = rhow / self._rhow
    def set_gor(self, gor):
        self._check_value(gor,0.,100000.)
        self._gor = gor
    def set_t(self, t):
        self._check_value(t,-273.15,1.e6)
        self._t = t
    def set_p(self, p):
        self._check_value(p,0.01,1.e6)
        self._p = p
    def set_rs(self, rs):
        self._check_value(rs,0.,100000.)
        self._rs = rs
    def set_p_bubble(self, p):
        self._check_value(p,0.01,1.e6)
        self._p_bubble = p
    def set_bo(self, bo):
        self._check_value(bo,0.01,10.)
        self._bo = bo
    def set_bg(self, bg):
        self._check_value(bg,1e-20,10.)
        self._bg = bg
    def set_bw(self, bw):
        self._check_value(bw,0.01,10.)
        self._bw = bw
    def set_bo_bubble(self, bo):
        self._check_value(bo,0.01,10.)
        self._bo_bubble = bo
    def set_co_bubble(self, co):
        self._check_value(co,1e-20,1e6)
        self._co_bubble = co
    def set_t_pc(self, t):
        self._check_value(t,-273.15,1.e6)
        self._t_pc = t
    def set_p_pc(self, p):
        self._check_value(p,0.01,1.e6)
        self._p_pc = p
    def set_t_pr(self, t):
        self._check_value(t,1e-20,1e6)
        self._t_pr = t
    def set_p_pr(self, p):
        self._check_value(p,1e-20,1e6)
        self._p_pr = p
    def set_y_co2(self, y):
        self._check_value(y,0,1.)
        self._y_co2 = y
    def set_y_h2s(self, y):
        self._check_value(y,0,1.)
        self._y_h2s = y
    def set_y_n2(self, y):
        self._check_value(y,0,1.)
        self._y_n2 = y
    def set_z(self, z):
        self._check_value(z,1e-20,1e6)
        self._z = z
    def set_uo_do(self, u):
        self._check_value(u,1e-20,1e6)
        self._uo_do = u
    def set_uo(self, u):
        self._check_value(u,1e-20,1e6)
        self._uo = u
    def set_emulsion(self, use):
        self._emulsion = use
    def set_q(self, q):
        self._q = q
    def set_d(self, d):
        self._d = d

    def reset_API(self):
        self._api = None
        self._do = None
    def reset_do(self):
        self.reset_API()
    def reset_dg(self):
        self._dg = None
    def reset_dw(self):
        self._dw = None
    def reset_t(self):
        self._t = None
    def reset_p(self):
        self._p = None
    def reset_tp(self):
        self.reset_t()
        self.reset_p()
    def reset_rs(self):
        self._rs = None
    def reset_gor(self):
        self._gor = None
    def reset_p_bubble(self):
        self._p_bubble = None
    def reset_bo(self):
        self._bo = None
    def reset_bg(self):
        self._bg = None
    def reset_bw(self):
        self._bw = None
    def reset_bo_bubble(self):
        self._bo_bubble = None
    def reset_co_bubble(self):
        self._co_bubble = None
    def reset_t_pc(self):
        self._t_pc = None
    def reset_p_pc(self):
        self._p_pc = None
    def reset_t_pr(self):
        self._t_pr = None
    def reset_p_pr(self):
        self._p_pr = None
    def reset_y_co2(self):
        self._y_co2 = None
    def reset_y_h2s(self):
        self._y_h2s = None
    def reset_y_n2(self):
        self._y_n2 = None
    def reset_z(self):
        self._z = None
    def reset_uo_do(self):
        self._uo_do = None
    def reset_uo(self):
        self._uo = None

    def get_API(self):
        return self._api
    def get_do(self):
        return self._do
    def get_rhoo_std(self):
        if self._do is None:
            return None
        return self._do * self._rhow
    def get_rhoo_in_place(self, auto=False):
        if self._do is None or self._dg is None:
            return None
        if auto:
            if self._rs is None:
                self.calculate_rs_Standing()
            if self._bo is None:
                self.calculate_bo_Standing(auto)
        else:
            if self._rs is None or self._bo is None:
                return None
        return (self.get_rhoo_std() + self._rs * self.get_rhog_std()) / self._bo
    def get_dg(self):
        return self._dg
    def get_rhog_std(self):
        if self._dg is None:
            return None
        return self._dg * self._rho_air
    def get_rhog_in_place(self, auto=False):
        if self._dg is None:
            return None
        if auto:
            if self._bg is None:
                self.calculate_bg(auto)
        else:
            if self._bg is None:
                return None
        return self.get_rhog_std() / self._bg
    def get_dw(self):
        return self._dw
    def get_rhow_std(self):
        if self._dw is None:
            return None
        return self._dw * self._rhow
    def get_rho(self, auto=False):
        if self._wfr > 0. and self._dw is None:
            return None
        if self._wfr == 1.:
            return self._dw * self._rhow
        rhoo = self.get_rhoo_in_place(auto)
        if self._wfr < 1. and rhoo is None:
            return None
        if self._wfr == 0.:
            return rhoo
        return (1-self._wfr) * rhoo + self._wfr * self._dw * self._rhow
    def get_t(self):
        return self._t
    def get_p(self):
        return self._p
    def get_rs(self):
        return self._rs
    def get_gor(self):
        return self._gor
    def get_p_bubble(self):
        return self._p_bubble
    def get_bo(self):
        return self._bo
    def get_bg(self):
        return self._bg
    def get_bw(self):
        return self._bw
    def get_b(self):
        if self._wfr == 1.:
            return self._bw
        if self._wfr == 0.:
            return self._bo
        return (1-self._wfr) * self._bo + self._wfr * self._bw
    def get_bo_bubble(self):
        return self._bo_bubble
    def get_co_bubble(self):
        return self._co_bubble
    def get_t_pc(self):
        return self._t_pc
    def get_p_pc(self):
        return self._p_pc
    def get_t_pr(self):
        return self._t_pr
    def get_p_pr(self):
        return self._p_pr
    def get_y_co2(self):
        return self._y_co2
    def get_y_h2s(self):
        return self._y_h2s
    def get_y_n2(self):
        return self._y_n2
    def get_z(self):
        return self._z
    def get_gas_mw(self):
        return 29. * self.get_dg()
    def get_uo_do(self):
        return self._uo_do
    def get_uo(self):
        return self._uo
    def get_wfr(self):
        return self._wfr

    def get_wfr_crit(self):
        if self._emulsion:
            return max(0.15, 0.5-0.1108*math.log10(self.get_uo()/1.))
        else:
            return -1.

    def get_u_emulsion(self):
        if self._q is None or self._d is None:
            print("### Could not calculate shear rate. Inform volumetric rate and/or diameter in PVT. ###")
            return self.get_u()
        shear_rate = 32. * self._q / (math.pi * math.pow(self._d, 3.))
        k1 = np.interp(shear_rate, self._ronningsen_k['shear_rate'], self._ronningsen_k['k1'])
        k2 = np.interp(shear_rate, self._ronningsen_k['shear_rate'], self._ronningsen_k['k2'])
        k3 = np.interp(shear_rate, self._ronningsen_k['shear_rate'], self._ronningsen_k['k3'])
        k4 = np.interp(shear_rate, self._ronningsen_k['shear_rate'], self._ronningsen_k['k4'])
        ln_ur = k1 + k2 * self.get_t() + k3 * self.get_wfr() + k4 * self.get_t() * self.get_wfr()
        return math.exp(max(0., ln_ur)) * self.get_uo()

    def get_u(self):
        if self._wfr == 1.:
            return self._uw
        if self._wfr == 0.:
            return self._uo
        if self._wfr < self.get_wfr_crit():
            return self.get_u_emulsion()
        else:
            return (1-self._wfr) * self._uo + self._wfr * self._uw

    def _raise_error_variable(self, variable):
        raise NameError(f'{self.variables.get_description(variable)} not set.')

    def _check_api(self):
        if self._api is None:
            self._raise_error_variable('api')
        return True
    def _check_do(self):
        if self._do is None:
            self._raise_error_variable('do')
        return True
    def _check_dg(self):
        if self._dg is None:
            self._raise_error_variable('dg')
        return True
    def _check_dw(self):
        if self._dw is None:
            self._raise_error_variable('dw')
        return True
    def _check_t(self):
        if self._t is None:
            self._raise_error_variable('t')
        return True
    def _check_p(self):
        if self._p is None:
            self._raise_error_variable('p')
        return True
    def _check_rs(self):
        if self._rs is None:
            self._raise_error_variable('rs')
        return True
    def _check_gor(self):
        if self._gor is None:
            self._raise_error_variable('gor')
        return True
    def _check_p_bubble(self):
        if self._p_bubble is None:
            self._raise_error_variable('p_bubble')
        return True
    def _check_bo(self):
        if self._bo is None:
            self._raise_error_variable('bo')
        return True
    def _check_bg(self):
        if self._bg is None:
            self._raise_error_variable('bg')
        return True
    def _check_bw(self):
        if self._bw is None:
            self._raise_error_variable('bw')
        return True
    def _check_bo_bubble(self):
        if self._bo_bubble is None:
            self._raise_error_variable('bo_bubble')
        return True
    def _check_co_bubble(self):
        if self._co_bubble is None:
            self._raise_error_variable('co_bubble')
        return True
    def _check_t_pc(self):
        if self._t_pc is None:
            self._raise_error_variable('t_pc')
        return True
    def _check_p_pc(self):
        if self._p_pc is None:
            self._raise_error_variable('p_pc')
        return True
    def _check_t_pr(self):
        if self._t_pr is None:
            self._raise_error_variable('t_pr')
        return True
    def _check_p_pr(self):
        if self._p_pr is None:
            self._raise_error_variable('p_pr')
        return True
    def _check_y_co2(self):
        if self._y_co2 is None:
            self._raise_error_variable('y_co2')
        return True
    def _check_y_h2s(self):
        if self._y_h2s is None:
            self._raise_error_variable('y_h2s')
        return True
    def _check_y_n2(self):
        if self._y_n2 is None:
            self._raise_error_variable('y_n2')
        return True
    def _check_z(self):
        if self._z is None:
            self._raise_error_variable('z')
        return True
    def _check_uo_do(self):
        if self._uo_do is None:
            self._raise_error_variable('uo_do')
        return True
    def _check_uo(self):
        if self._uo is None:
            self._raise_error_variable('uo')
        return True

    def _check(self, variables):
        for variable in variables:
            match variable.lower():
                case 'api':
                    _ = self._check_api()
                case 'do':
                    _ = self._check_do()
                case 'dg':
                    _ = self._check_dg()
                case 'dw':
                    _ = self._check_dw()
                case 't':
                    _ = self._check_t()
                case 'p':
                    _ = self._check_p()
                case 'rs':
                    _ = self._check_rs()
                case 'gor':
                    _ = self._check_gor()
                case 'p_bubble':
                    _ = self._check_p_bubble()
                case 'bo':
                    _ = self._check_bo()
                case 'bg':
                    _ = self._check_bg()
                case 'bw':
                    _ = self._check_bw()
                case 'bo_bubble':
                    _ = self._check_bo_bubble()
                case 'co_bubble':
                    _ = self._check_co_bubble()
                case 't_pc':
                    _ = self._check_t_pc()
                case 'p_pc':
                    _ = self._check_p_pc()
                case 't_pr':
                    _ = self._check_t_pr()
                case 'p_pr':
                    _ = self._check_p_pr()
                case 'y_co2':
                    _ = self._check_y_co2()
                case 'y_h2s':
                    _ = self._check_y_h2s()
                case 'y_n2':
                    _ = self._check_y_n2()
                case 'z':
                    _ = self._check_z()
                case 'uo_do':
                    _ = self._check_uo_do()
                case 'uo':
                    _ = self._check_uo()
                case '_':
                    raise NameError('Unknown variable.')
        return True

    def calculate_rs_Standing(self):
        self._check(['dg','p','api','t','gor'])
        x = 0.0125 * self._api - 0.00091 * (1.8 * self._t + 32)
        y = self._p * math.pow(10, x)
        z = 0.1373 * self._dg * math.pow(y, 1.205)
        self._rs = min(z, self._gor)

    def calculate_p_bubble_Standing(self):
        self._check(['dg','gor','api','t'])
        x = 0.0125 * self._api - 0.00091 * (1.8 * self._t + 32)
        y = self._gor / self._dg / 0.1373
        self._p_bubble = math.pow(y, 1/1.205) * math.pow(10, -x)

    def calculate_p_bubble_Standing_Original(self):
        self._check(['dg','gor','api','t'])
        x = 0.0125 * self._api - 0.00091 * (1.8 * self._t + 32)
        y = 5.615 * self._gor / self._dg
        z = math.pow(y, 0.83) * math.pow(10, -x)
        self._p_bubble = 1.305 * (z - 1.4)

    def calculate_co_bubble_Standing(self, auto=False):
        self._check(['t','dg','api'])
        if auto:
            if self._rs is None:
                self.calculate_rs_Standing()
            if self._p_bubble is None:
                self.calculate_p_bubble_Standing()
        else:
            self._check(['rs','p_bubble'])
        x = -1433. + 5 * 5.615 * self._gor
        y = 17.2*(1.8 * self._t + 32.)
        z = -1180. * self._dg + 12.61 * self._api
        w = 1E5 * self._p_bubble
        self._co_bubble = (x + y + z) / w

    def calculate_bo_bubble_Standing(self):
        self._check(['dg','do','t','gor'])
        x = 5.615 * self._gor * math.pow(self._dg / self._do, 0.5)
        y = 1.25 * (1.8 * self._t + 32)
        self._bo_bubble = 0.9759 +  12E-5 * math.pow(x + y, 1.2)

    def calculate_bo_Standing(self, auto=False):
        self._check(['p'])
        if auto:
            if self._p_bubble is None:
                self.calculate_p_bubble_Standing()
        else:
            self._check(['p_bubble'])
        if self._p > self._p_bubble:
            if auto:
                if self._bo_bubble is None:
                    self.calculate_bo_bubble_Standing()
                if self._co_bubble is None:
                    self.calculate_co_bubble_Standing(auto)
            else:
                self._check(['co_bubble','bo_bubble'])
            bo = self._bo_bubble * math.exp(self._co_bubble * (self._p_bubble - self._p))
            self._check_value(bo, 1e-3, 1e3)
            self._bo = bo
        else:
            self._check(['dg','do','t'])
            if auto:
                if self._rs is None:
                    self.calculate_rs_Standing()
            else:
                self._check(['rs'])
            x = 5.615 * self._rs * math.pow(self._dg / self._do, 0.5)
            y = 1.25 * (1.8 * self._t + 32)
            self._bo = 0.9759 +  12E-5 * math.pow(x + y, 1.2)

    def calculate_bo_Standing_linear(self, auto=False):
        self._check(['p'])
        if auto:
            if self._p_bubble is None:
                self.calculate_p_bubble_Standing()
        else:
            self._check(['p_bubble'])
        if self._p > self._p_bubble:
            if auto:
                if self._bo_bubble is None:
                    self.calculate_bo_bubble_Standing()
                if self._co_bubble is None:
                    self.calculate_co_bubble_Standing()
            else:
                self._check(['co_bubble','bo_bubble'])
            bo = self._bo_bubble * (1 + self._co_bubble * (self._p_bubble - self._p))
            # self._check_value(bo, 1e-3, 1e3)
            self._bo = bo
        else:
            self._check(['dg','do','t'])
            if auto:
                if self._rs is None:
                    self.calculate_rs_Standing()
            else:
                self._check(['rs'])
            x = 5.615 * self._rs * math.pow(self._dg / self._do, 0.5)
            y = 1.25 * (1.8 * self._t + 32)
            self._bo = 0.9759 +  12E-5 * math.pow(x + y, 1.2)

    def calculate_p_pc_Standing(self):
        self._check(['dg','y_co2','y_h2s','y_n2'])
        x = 706. - 51.7 * self._dg - 11.1 * self._dg * self._dg
        y = 440. * self._y_co2 + 600. * self._y_h2s - 170. * self._y_n2
        self._p_pc = (x + y) / 14.503773773375086

    def calculate_t_pc_Standing(self, auto=False):
        self._check(['dg','y_co2','y_h2s','y_n2'])
        x = 187. + 330. * self._dg - 71.5 * self._dg * self._dg
        y = - 80. * self._y_co2 + 130. * self._y_h2s - 250. * self._y_n2
        self._t_pc = (x + y - 491.67) * 5./9.

    def calculate_p_pr(self, auto=False):
        self._check(['p'])
        if auto:
            if self._p_pc is None:
                self.calculate_p_pc_Standing()
        else:
            self._check(['p_pc'])
        self._p_pr = self._p / self._p_pc

    def calculate_t_pr(self, auto=False):
        self._check(['t'])
        if auto:
            if self._t_pc is None:
                self.calculate_t_pc_Standing()
        else:
            self._check(['t_pc'])
        self._t_pr = (self._t  + 273.15)/ (self._t_pc + 273.15)

    def calculate_z_Standing(self, auto=False):
        if auto:
            if self._p_pr is None:
                self.calculate_p_pr(True)
            if self._t_pr is None:
                self.calculate_t_pr(True)
        else:
            self._check(['p_pr','t_pr'])
        self._check_value(self._p_pr, 0, 13)
        self._check_value(self._t_pr, 1.2, 2.4)
        p = self._p_pr
        t = self._t_pr
        a = 1.39 * math.pow(t - 0.92, 0.5) - 0.36 * t - 0.101
        b = (0.62 - 0.23 * t) * p + ( 0.066/(t - 0.86) -0.037) * p * p + 0.32 / math.pow(10, 9*(t - 1)) * math.pow(p,6)
        c = 0.132 - 0.32 * math.log10(t)
        d = math.pow(10, 0.3106 - 0.49 * t + 0.1824 *t * t)
        self._z = a + (1 - a) / math.exp(b) + c * math.pow(p, d)

    def calculate_bg(self, auto=False):
        self._check(['p','t'])
        if auto:
            if self._z is None:
                self.calculate_z_Standing(auto)
        else:
            self._check(['z'])
        self._bg = self._z * self._p_std / self._p * (self._t + 273.15) / (self._t_std + 273.15)

    def calculate_uo_do_Standing(self):
        self._check(['t','api'])
        a = math.pow(10, 0.43 + 8.33 / self._api)
        x = 0.32 + 1.8E7 / math.pow(self._api, 4.53)
        y = math.pow(360 / (1.8 * self._t + 232), a)
        self._uo_do = x * y

    def calculate_uo_Standing(self, auto=False):
        if auto:
            if self._rs is None:
                self.calculate_rs_Standing()
            if self._uo_do is None:
                self.calculate_uo_do_Standing()
        else:
            self._check(['rs','uo_do'])
        rs = 5.615 * self._rs
        A = math.pow(10, rs * (2.2E-7 * rs - 7.4E-4))
        b = 0.68 / math.pow(10, 8.62E-5 * rs) + 0.25 / math.pow(10, 1.1E-3 * rs) + 0.062 / math.pow(10, 3.74E-3 * rs)
        self._uo = A * math.pow(self._uo_do, b)
