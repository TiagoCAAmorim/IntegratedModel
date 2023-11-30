import math
import pvt
import numpy as np

day_to_s = 60.*60.*24.
R_si = 8314.

class Separator:

    def __init__(self):
        self._ks = None
        self._d = None
        self.pvt = pvt.PVT()

    def set_ks(self, value):
        self._ks = value
    def set_d(self, value):
        self._d = value

    def calculate_max_rates(self):
        rho_o = self.pvt.get_rhoo_in_place(auto=True)
        rho_g = self.pvt.get_rhog_in_place(auto=True)

        vg_max = self._ks * math.sqrt( (rho_o-rho_g)/rho_g)
        fg = 1.
        qg_max = (math.pi * self._d*self._d / 4.) * fg * vg_max * day_to_s
        qo_max = qg_max / self.pvt.get_gor()
        return qo_max, qg_max

class WaterPump:

    def __init__(self):
        self._eff = None
        self._qw = None

    def set_eff(self, value):
        self._eff = value

    def set_qw(self, value):
        self._qw = value

    def get_power_from_head(self, head):
        qm = self._qw / day_to_s * 1000.
        return head * qm * 9.81 / self._eff * 1E-6

    def get_power_from_delta_p(self, delta_p):
        head = delta_p / (9.81 * 1000.)
        return self.get_power_from_head(head)

class GasCompressor:

    def __init__(self):
        self._eff = None
        self._qg = None
        self._k = None
        self._n = None
        self._p_out = None
        self.pvt = pvt.PVT()

    def set_eff(self, value):
        self._eff = value

    def set_qg(self, value):
        self._qg = value

    def set_k(self, value):
        self._k = value

    def set_p_out(self, value):
        self._p_out = value

    def get_n(self):
        alpha = self._eff * self._k / (self._k - 1.)
        self._n = -alpha / (1 - alpha)

    def get_power(self):
        self.get_n()
        qmg = self._qg / day_to_s * self.pvt.get_rhog_std()
        self.pvt.calculate_z_Standing(auto=True)
        h_poly = self._n / (self._n - 1.) * self.pvt.get_z() * R_si * (self.pvt.get_t() + 273.15) / self.pvt.get_gas_mw()
        h_poly *= (math.pow(self._p_out / self.pvt.get_p(), (self._n - 1.) / self._n) - 1.)
        p_poly = h_poly * qmg / self._eff
        return p_poly * 1e-6

class GasTurbine:

    def __init__(self):
        self._rates = None
        self._power = None

    def set_rates(self, values):
        self._rates = np.array(list(values))

    def set_power(self, values):
        self._power = np.array(list(values))

    def get_fuel(self, power_demand):
        return np.interp(power_demand, self._power, self._rates)

class CO2_Emission:

    def __init__(self):
        self._mole_pc = {'co2':0., 'ch4':0., 'c2h6':0., 'c3h8':0., 'c4h10':0., 'n2':0., 'other':0.}
        self._mw = {'co2':44., 'ch4':16., 'c2h6':30., 'c3h8':44., 'c4h10':58., 'n2':28., 'other':1e-20}
        self._c = {'co2':1., 'ch4':1., 'c2h6':2., 'c3h8':3., 'c4h10':4., 'n2':0., 'other':0.}
        self._emission = None
        self.turbine = GasTurbine()

    def set_mole_pc(self, component, value):
        if component in self._mole_pc.keys():
            self._mole_pc[component] = value
        else:
            print("Component not implemented!")

    def set_other_mw(self, value):
        self._mw['other'] = value
    def set_other_c(self, value):
        self._c['other'] = value

    def get_relative_emission(self):
        return self._emission

    def calculate_relative_emission(self):
        mole_pc = np.array(list(self._mole_pc.values()))
        mw = np.array(list(self._mw.values()))
        c_list = np.array(list(self._c.values()))
        total_moles = mole_pc.sum()
        if total_moles == 0.:
            print("Enter gas composition.")
            return
        if total_moles != 1.:
            mole_pc = mole_pc / total_moles
        mw_gas = np.dot(mole_pc, mw)
        weight_pc = mole_pc * mw / mw_gas
        c_weigth_pc = 12. * (c_list / mw)
        c_weigth_total = np.dot(weight_pc, c_weigth_pc)
        self._emission = mw_gas * c_weigth_total * 44. / 12. / 23.685

    def get_emission(self, power_demand):
        self.calculate_relative_emission()
        return self._emission * self.turbine.get_fuel(power_demand)
