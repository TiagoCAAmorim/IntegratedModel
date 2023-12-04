import math
import pvt
import ipr
import common
import reservoir

class SubFlowElement:

    def __init__(self, element=None, debug=False):
        self._eps = 1E-12
        self._max_iter = 100
        self._g = 9.81 # m/s^2

        self._z_in = 0
        self._z_out = 0
        self._p = None
        self._p_in = None
        self._p_out = None
        self._p_delta = None
        self._t = None
        self._t_in = None
        self._t_out = None
        self._t_delta = None

        self._m_rate = None
        self._q = None
        self._q_in = None
        self._q_out = None
        self._v = None
        self._v_in = None
        self._v_out = None

        self._d = None
        self._e = None
        self._h = None

        self._f = None
        self._re = None
        self._hl = None

        self.pvt = pvt.PVT()

        self._debug = debug

        if element is not None:
            self._copy_all_properties(element)

        self.variables = common.VariablesList({
            'z_in':['Inlet height', 'm'],
            'z_out':['Outlet height', 'm'],
            'p':['Average pressure', 'bar'],
            'p_in':['Inlet pressure', 'bar'],
            'p_out':['Outlet pressure', 'bar'],
            'p_delta':['Outlet - inlet pressure', 'bar'],
            't':['Average temperature', 'oC'],
            't_in':['Inlet temperature', 'oC'],
            't_out':['Outlet temperature', 'oC'],
            't_delta':['Outlet - inlet temperature', 'oC'],

            'm_rate':['Mass flow rate', 'kg/s'],
            'q':['Average volumetric flow rate', 'm3/d'],
            'q_in':['Inlet volumetric flow rate', 'm3/d'],
            'q_out':['Outlet volumetric flow rate', 'm3/d'],
            'v':['Average velocity', 'm/s'],
            'v_in':['Inlet velocity', 'm/s'],
            'v_out':['Outlet velocity', 'm/s'],

            'd':['Internal diameter', 'm'],
            'e':['Rugosity', 'm'],
            'h':['Element length', 'm'],
            'f':['Friction factor', '-'],
            're':['Reynolds number', '-'],
            'hl':['Head loss', 'm'],

            'pvt':['PVT object','-']
            })

    def _copy_all_properties(self, element):
        self._z_in = element._z_in
        self._z_out = element._z_out
        self._p = element._p
        self._p_in = element._p_in
        self._p_out = element._p_out
        self._p_delta = element._p_delta
        self._t = element._t
        self._t_in = element._t_in
        self._t_out = element._t_out
        self._t_delta = element._t_delta
        self._m_rate = element._m_rate
        self._q = element._q
        self._q_in = element._q_in
        self._q_out = element._q_out
        self._v = element._v
        self._v_in = element._v_in
        self._v_out = element._v_out
        self._d = element._d
        self._e = element._e
        self._h = element._h
        self._f = element._f
        self._re = element._re
        self._hl = element._hl
        self.pvt = element.pvt.copy()

    def copy(self):
        element = SubFlowElement()

        element._z_in = self._z_in
        element._z_out = self._z_out
        element._p = self._p
        element._p_in = self._p_in
        element._p_out = self._p_out
        element._p_delta = self._p_delta
        element._t = self._t
        element._t_in = self._t_in
        element._t_out = self._t_out
        element._t_delta = self._t_delta

        element._m_rate = self._m_rate
        element._q = self._q
        element._q_in = self._q_in
        element._q_out = self._q_out
        element._v = self._v
        element._v_in = self._v_in
        element._v_out = self._v_out

        element._d = self._d
        element._e = self._e
        element._h = self._h

        element._f = self._f
        element._re = self._re
        element._hl = self._hl

        element.pvt = self.pvt.copy()

        return element

    def _log(self, message):
        if self._debug:
            print(message)

    def get_variables_list(self):
        return self.variables.get_list()

    def set_z_in(self,z):
        self._z_in = z
    def set_z_out(self,z):
        self._z_out = z
    def set_p_in(self,p):
        self._p_in = p
    def set_p_out(self,p):
        self._p_out = p
    def set_p(self,p):
        self._p = p
    def set_t_in(self,t):
        self._t_in = t
    def set_t_out(self,t):
        self._t_out = t
    def set_q_in(self,q):
        self._q_in = q
    def set_q_out(self,q):
        self._q_out = q
    def set_d(self,d):
        self._d = d
    def set_e(self,e):
        self._e = e
    def set_h(self,h):
        self._h = h

    def get_z_in(self):
        return self._z_in
    def get_z_out(self):
        return self._z_out
    def get_p(self):
        return self._p
    def get_p_in(self):
        return self._p_in
    def get_p_out(self):
        return self._p_out
    def get_t(self):
        return self._t
    def get_t_in(self):
        return self._t_in
    def get_t_out(self):
        return self._t_out
    def get_m_rate(self):
        return self._m_rate
    def get_q(self):
        return self._q
    def get_q_in(self):
        return self._q_in
    def get_q_out(self):
        return self._q_out
    def get_v(self):
        return self._v
    def get_v_in(self):
        return self._v_in
    def get_v_out(self):
        return self._v_out
    def get_d(self):
        return self._d
    def get_e(self):
        return self._e
    def get_h(self):
        return self._h
    def get_f(self):
        return self._f
    def get_re(self):
        return self._re
    def get_hl(self):
        return self._hl

    def get_p_bubble(self):
        return self.pvt.get_p_bubble()
    def get_rs(self):
        return self.pvt.get_rs()
    def get_gor(self):
        return self.pvt.get_gor()
    def get_u(self):
        return self.pvt.get_u()
    def get_b(self):
        return self.pvt.get_b()

    def calculate_p(self):
        self._p = (self._p_in + self._p_out) / 2.
    def calculate_t(self):
        self._t = (self._t_in + self._t_out) / 2.
    def calculate_q(self):
        self._q = (self._q_in + self._q_out) / 2.
    def calculate_v(self):
        self._v = (self._v_in + self._v_out) / 2.

    def calculate_rhoo(self, p, t):
        self.pvt.set_t(t)
        self.pvt.set_p(p)
        self.pvt.calculate_rs_Standing()
        self.pvt.calculate_p_bubble_Standing()
        self.pvt.calculate_co_bubble_Standing()
        self.pvt.calculate_bo_bubble_Standing()
        self.pvt.calculate_bo_Standing()

    def calculate_q_in(self):
        self.calculate_rhoo(self._p_in, self._t_in)
        self._q_in = self._m_rate / self.pvt.get_rho() * (24*60*60)
    def calculate_q_out(self):
        self.calculate_rhoo(self._p_out, self._t_out)
        self._q_out = self._m_rate / self.pvt.get_rho() * (24*60*60)

    def set_q_std(self, q):
        self.calculate_m_rate_std(q)
        if (self._p_in is not None) and (self._t_in is not None):
            self.calculate_q_in()
        if (self._p_out is not None) and (self._t_out is not None):
            self.calculate_q_out()

    def get_q_std(self):
        self.calculate_rhoo(self.pvt._p_std, self.pvt._t_std)
        return self._m_rate / self.pvt.get_rho() * (24*60*60)

    def calculate_m_rate_in(self):
        self.calculate_rhoo(self._p_in, self._t_in)
        self._m_rate = self.pvt.get_rho() * self._q_in / (24*60*60)
    def calculate_m_rate_out(self):
        self.calculate_rhoo(self._p_out, self._t_out)
        self._m_rate = self.pvt.get_rho() * self._q_out / (24*60*60)
    def calculate_m_rate_std(self, q_std):
        self.calculate_rhoo(self.pvt._p_std, self.pvt._t_std)
        self._m_rate = self.pvt.get_rho() * q_std / (24*60*60)

    def calculate_v_in(self):
        self.calculate_rhoo(self._p_in, self._t_in)
        self._v_in = 4 * self._m_rate / (self.pvt.get_rho() * math.pi * self._d ** 2)
    def calculate_v_out(self):
        self.calculate_rhoo(self._p_out, self._t_out)
        self._v_out = 4 * self._m_rate / (self.pvt.get_rho() * math.pi * self._d ** 2)

    def calculate_uo(self, p, t):
        self.pvt.set_t(t)
        self.pvt.set_p(p)
        self.pvt.calculate_rs_Standing()
        self.pvt.calculate_uo_do_Standing()
        self.pvt.calculate_uo_Standing()

    def calculate_Reynolds(self):
        self.calculate_uo(self._p, self._t)
        self.calculate_rhoo(self._p, self._t)
        self.pvt.set_q(self._m_rate / self.pvt.get_rho())
        self._re = 4 * self._m_rate / (self.pvt.get_u()/1000. * math.pi * self._d)

    def calculate_f(self):
        f0 = 64 / self._re
        if self._re < 2300:
            self._f = f0
        else:
            sqrt_f = 1./math.sqrt(f0)
            sqrt_f0 = 2. * sqrt_f
            while (abs(sqrt_f - sqrt_f0)/sqrt_f > 0.001):
                sqrt_f0 = sqrt_f
                sqrt_f = 1.14 - 2.*math.log10(self._e / self._d + 9.35/self._re * sqrt_f0)
            f = 1./math.pow(sqrt_f, 2)
            if self._re > 4000:
                self._f = f
            else:
                self._f = f0 + (f - f0) * (self._re - 2300.) / (4000. - 2300.)

    def calculate_head_loss(self):
        self._hl = self._f * self._h * self._v ** 2 / (self._d * 2 * self._g)

    def calculate_delta_z(self):
        return self._z_out - self._z_in

    def calculate_delta_v2_g(self):
        return (self._v_out ** 2 - self._v_in ** 2) / (2 * self._g)

    def calculate_delta_p(self):
        self.calculate_rhoo(self._p, self._t)
        self.calculate_Reynolds()
        self.calculate_f()
        self.calculate_v_in()
        self.calculate_v_out()
        self.calculate_v()
        dz = self.calculate_delta_z()
        self.calculate_head_loss()
        hl = self._hl
        htm = 0.  # not implemented yet
        dv2 = self.calculate_delta_v2_g()
        deltap = -1E-5 * self.pvt.get_rho() * self._g * (dz + hl + htm + dv2)
        self._log(f'  dz = {dz:0.2f}\thl = {hl:0.2f}\tdv2 = {dv2:0.2f}\tdeltap = {deltap:0.2f}\trho = {self.pvt.get_rho():0.2f}\tu = {self.pvt.get_u():0.2f}\tRe = {self.get_re():0.2f}')
        return deltap

    def calculate_p_in(self):
        self.set_p_in(self._p_out - self.calculate_delta_p())
    def calculate_p_out(self):
        self.set_p_out(self._p_in + self.calculate_delta_p())

    def calculate_delta_t(self):
        return 0.

    def calculate_t_in(self):
        self._t_in = self._t_out - self.calculate_delta_t()
    def calculate_t_out(self):
        self._t_out = self._t_in + self.calculate_delta_t()

    def solve_flow(self, p_0, t_0,
                   set_p_function, set_t_function,
                   calculate_p_function, calculate_t_function,
                   calculate_q_function, calculate_v_function):
        set_p_function(p_0)
        set_t_function(t_0)
        self.calculate_p()
        self.calculate_t()
        p_old = self.get_p()
        t_old = self.get_t()
        i = 0
        while i<self._max_iter:
            calculate_p_function()
            calculate_t_function() # not implemented yet
            self.calculate_p()
            self.calculate_t()
            if abs(p_old - self._p)/abs(self._p) < self._eps and abs(t_old - self._t)/abs(self._t + 273.15) < self._eps:
                break
            p_old = self.get_p()
            t_old = self.get_t()
            i += 1
        if i == self._max_iter:
            print(f'Failed to converge: P_error={abs(p_old - self._p)/abs(self._p)*100.:.3g}%, P_in={self._p_in:.2f}, P_mean={self._p:.2f}, P_out={self._p_out:.2f}')
        calculate_q_function()
        calculate_v_function()

    def solve_out_flow(self):
        self.calculate_m_rate_in()
        self.solve_flow(self.get_p_in(), self.get_t_in(),
                        self.set_p_out, self.set_t_out,
                        self.calculate_p_out, self.calculate_t_out,
                        self.calculate_q_out, self.calculate_v_out)

    def solve_in_flow(self):
        self.calculate_m_rate_out()
        self.solve_flow(self.get_p_out(), self.get_t_out(),
                        self.set_p_in, self.set_t_in,
                        self.calculate_p_in, self.calculate_t_in,
                        self.calculate_q_in, self.calculate_v_in)

class FlowElement(SubFlowElement):

    def __init__(self, debug_mode=False):
        super().__init__()
        self._n = 1
        self._elements = [] # SubFlowElement()

        self._variables = {
            'n':['Number of subdivisions', '-'],
            'elements':['List of SubFlowElements', '-']
            }
        self._variables.update(super().get_variables_list())
        self.variables = common.VariablesList(self._variables)
        self._debug = debug_mode

    def copy(self):
        element = FlowElement()

        element._z_in = self._z_in
        element._z_out = self._z_out
        element._p = self._p
        element._p_in = self._p_in
        element._p_out = self._p_out
        element._p_delta = self._p_delta
        element._t = self._t
        element._t_in = self._t_in
        element._t_out = self._t_out
        element._t_delta = self._t_delta

        element._m_rate = self._m_rate
        element._q = self._q
        element._q_in = self._q_in
        element._q_out = self._q_out
        element._v = self._v
        element._v_in = self._v_in
        element._v_out = self._v_out

        element._d = self._d
        element._e = self._e
        element._h = self._h

        element._f = self._f
        element._re = self._re
        element._hl = self._hl

        element.pvt = self.pvt.copy()
        element._n = self._n
        element._elements = self._elements.copy()

        return element

    def _log(self, message):
        if self._debug:
            print(message)

    def get_variables_list(self):
        return self.variables.get_list()

    def set_number_divisions(self, n):
        self._n = n

    def _get_results_elements(self, get_method_name, default_value):
        if len(self._elements) == 0:
            return [default_value]
        else:
            x = []
            for element in self._elements:
                method = getattr(element, get_method_name)
                x.append(method())
            return x

    def get_z_in(self):
        return self._get_results_elements('get_z_in', self._z_in)
    def get_z_out(self):
        return self._get_results_elements('get_z_out', self._z_out)
    def get_p(self):
        return self._get_results_elements('get_p', self._p)
    def get_p_in(self):
        return self._get_results_elements('get_p_in', self._p_in)
    def get_p_out(self):
        return self._get_results_elements('get_p_out', self._p_out)
    def get_t(self):
        return self._get_results_elements('get_t', self._t)
    def get_t_in(self):
        return self._get_results_elements('get_t_in', self._t_in)
    def get_t_out(self):
        return self._get_results_elements('get_t_out', self._t_out)
    def get_m_rate(self):
        return self._get_results_elements('get_m_rate', self._m_rate)
    def get_q(self):
        return self._get_results_elements('get_q', self._q)
    def get_q_in(self):
        return self._get_results_elements('get_q_in', self._q_in)
    def get_q_out(self):
        return self._get_results_elements('get_q_out', self._q_out)
    def get_v(self):
        return self._get_results_elements('get_v', self._v)
    def get_v_in(self):
        return self._get_results_elements('get_v_in', self._v_in)
    def get_v_out(self):
        return self._get_results_elements('get_v_out', self._v_out)
    def get_d(self):
        return self._get_results_elements('get_d', self._d)
    def get_e(self):
        return self._get_results_elements('get_e', self._e)
    def get_h(self):
        return self._get_results_elements('get_h', self._h)
    def get_f(self):
        return self._get_results_elements('get_f', self._f)
    def get_re(self):
        return self._get_results_elements('get_re', self._re)
    def get_hl(self):
        return self._get_results_elements('get_hl', self._hl)
    def get_p_bubble(self):
        return self._get_results_elements('get_p_bubble', 0)
    def get_rs(self):
        return self._get_results_elements('get_rs', 0)
    def get_gor(self):
        return self._get_results_elements('get_gor', 0)
    def get_u(self):
        return self._get_results_elements('get_u', 0)
    def get_b(self):
        return self._get_results_elements('get_b', 0)

    def get_h_cumulative(self):
        h = self.get_h()
        return [sum(h[:i + 1]) for i in range(len(h))]

    def _build_element_list(self):
        self._elements = [SubFlowElement(self, self._debug) for _ in range(self._n)]
        for i, element in enumerate(self._elements):
            element._h = self._h / self._n
            element._z_in = self._z_in + i * (self._z_out - self._z_in)/ self._n
            element._z_out = self._z_in + (i + 1) * (self._z_out - self._z_in)/ self._n

    def _print_flow_data_in(self, name, element):
        if isinstance(element.get_p_in(), list):
            self._log(f'    {name}: p= {element._p_in:6.2f} bar\tt= {element._t_in:6.2f} oC\tq= {element._q_in:7.2f} m3/d')
        else:
            self._log(f'    {name}: p= {element.get_p_in():6.2f} bar\tt= {element.get_t_in():6.2f} oC\tq= {element.get_q_in():7.2f} m3/d')
    def _print_flow_data_out(self, name, element):
        if isinstance(element.get_p_out(), list):
            self._log(f'    {name}: p= {element._p_out:6.2f} bar\tt= {element._t_out:6.2f} oC\tq= {element._q_out:7.2f} m3/d')
        else:
            self._log(f'    {name}: p= {element.get_p_out():6.2f} bar\tt= {element.get_t_out():6.2f} oC\tq= {element.get_q_out():7.2f} m3/d')

    def solve_out_flow(self):
        self._print_flow_data_in(name='Input data ', element=self)
        self._build_element_list()
        self._elements[0].solve_out_flow()
        prev_element = self._elements[0]
        self._print_flow_data_out(name=f'Sub-element {1:3d}', element=prev_element)
        for i,element in enumerate(self._elements[1:]):
            element.set_p_in(prev_element.get_p_out())
            element.set_t_in(prev_element.get_t_out())
            element.set_q_in(prev_element.get_q_out())
            prev_element = element
            element.solve_out_flow()
            self._print_flow_data_out(name=f'Sub-element {i+2:3d}', element=prev_element)
        self.set_p_out(self._elements[-1].get_p_out())
        self.set_t_out(self._elements[-1].get_t_out())
        self.set_q_out(self._elements[-1].get_q_out())

    def solve_in_flow(self):
        self._print_flow_data_out(name='Output data', element=self)
        self._build_element_list()
        self._elements[-1].solve_in_flow()
        prev_element = self._elements[-1]
        self._print_flow_data_in(name=f'Sub-element {self._n:3d}', element=prev_element)
        for i,element in enumerate(self._elements[-2::-1]):
            element.set_p_out(prev_element.get_p_in())
            element.set_t_out(prev_element.get_t_in())
            element.set_q_out(prev_element.get_q_in())
            element.solve_in_flow()
            prev_element = element
            self._print_flow_data_in(name=f'Sub-element {self._n-i-1:3d}', element=prev_element)
        self.set_p_in(self._elements[0].get_p_in())
        self.set_t_in(self._elements[0].get_t_in())
        self.set_q_in(self._elements[0].get_q_in())

class CompositeFlowElement:

    def __init__(self, debug_mode=False):
        self._elements = []
        self.current_element = None
        self._n = 1
        self.pvt = pvt.PVT()
        self.ipr = ipr.IPR()
        self._reservoir = None
        self._dt = None

        self._p_in = None
        self._p_out = None
        self._t_in = None
        self._t_out = None

        self._q_in = None
        self._q_out = None

        self._q_std = None
        # self._qo_std = None
        # self._qg_std = None
        # self._qw_std = None

        self._d = None
        self._e = None

        self._pwf = None
        self._max_iter = 20
        self._eps = 1E-12
        self._debug = debug_mode

        self.variables = common.VariablesList({
            'elements':['List of FlowElements', '-'],
            'current element':['Current FlowElement', '-'],
            'n':['Number of subdivisions by element', '-'],

            'p_in':['Inlet pressure', 'bar'],
            'p_out':['Outlet pressure', 'bar'],
            't_in':['Inlet temperature', 'oC'],
            't_out':['Outlet temperature', 'oC'],

            'm_rate':['Mass flow rate', 'kg/s'],
            'q_in':['Inlet volumetric flow rate', 'm3/d'],
            'q_out':['Outlet volumetric flow rate', 'm3/d'],
            'q_std':['Volumetric flow rate in standard conditions', 'm3/d'],

            'd':['Internal diameter', 'm'],
            'e':['Rugosity', 'm'],

            'pvt':['PVT object','-'],
            'ipr':['IPR object','-'],
            'pwf':['Bottom-hole pressure at the operational point','-'],
            'max_iter':['Maximum interations in operational point calculation','-'],
            })

    def _log(self, message):
        if self._debug:
            print(message)

    def set_number_divisions(self, n):
        self._n = n
    def set_p_in(self,p):
        self._p_in = p
    def set_p_out(self,p):
        self._p_out = p
    def set_t_in(self,t):
        self._t_in = t
    def set_t_out(self,t):
        self._t_out = t
    def set_q_in(self,q):
        self._q_in = q
    def set_q_out(self,q):
        self._q_out = q
    def set_q_std(self,q):
        self._q_std = q
    def set_d(self,d):
        self._d = d
        self.pvt.set_d(d)
    def set_e(self,e):
        self._e = e
    def set_max_iter(self,i):
        self._max_iter = i

    def set_dt(self,value):
        self._dt = value
    def set_reservoir(self, reservoir_obj):
        self._reservoir = reservoir_obj

    def update_pvt(self):
        for element in self._elements:
            element.pvt = self.pvt.copy()

    def add_element(self):
        self._elements.append(FlowElement(self._debug))
        self._elements[-1].pvt = self.pvt.copy()
        self._elements[-1]._n = self._n
        self._elements[-1]._d = self._d
        self._elements[-1]._e = self._e
        if len(self._elements) > 1:
            self._elements[-1].set_z_in(self._elements[-2].get_z_out()[-1])
        else:
            self._elements[-1].set_z_in(self.get_z_in)
            self._elements[-1].set_p_in(self.get_p_in)
            self._elements[-1].set_q_in(self.get_q_in)
            self._elements[-1].set_t_in(self.get_t_in)
        self.current_element = self._elements[-1]

    def _get_results_elements(self, get_method_name):
        x = []
        for element in self._elements:
            method = getattr(element, get_method_name)
            x.extend(method())
        return x

    def get_z_in(self):
        return self._get_results_elements('get_z_in')
    def get_z_out(self):
        return self._get_results_elements('get_z_out')
    def get_p(self):
        return self._get_results_elements('get_p')
    def get_p_in(self):
        return self._get_results_elements('get_p_in')
    def get_p_out(self):
        return self._get_results_elements('get_p_out')
    def get_t(self):
        return self._get_results_elements('get_t')
    def get_t_in(self):
        return self._get_results_elements('get_t_in')
    def get_t_out(self):
        return self._get_results_elements('get_t_out')
    def get_m_rate(self):
        return self._get_results_elements('get_m_rate')
    def get_q(self):
        return self._get_results_elements('get_q')
    def get_q_in(self):
        return self._get_results_elements('get_q_in')
    def get_q_out(self):
        return self._get_results_elements('get_q_out')
    def get_v(self):
        return self._get_results_elements('get_v')
    def get_v_in(self):
        return self._get_results_elements('get_v_in')
    def get_v_out(self):
        return self._get_results_elements('get_v_out')
    def get_d(self):
        return self._get_results_elements('get_d')
    def get_e(self):
        return self._get_results_elements('get_e')
    def get_h(self):
        return self._get_results_elements('get_h')
    def get_f(self):
        return self._get_results_elements('get_f')
    def get_re(self):
        return self._get_results_elements('get_re')
    def get_hl(self):
        return self._get_results_elements('get_hl')
    def get_p_bubble(self):
        return self._get_results_elements('get_p_bubble')
    def get_rs(self):
        return self._get_results_elements('get_rs')
    def get_gor(self):
        return self._get_results_elements('get_gor')
    def get_u(self):
        return self._get_results_elements('get_u')
    def get_b(self):
        return self._get_results_elements('get_b')

    def get_h_cumulative(self):
        h = self.get_h()
        return [sum(h[:i + 1]) for i in range(len(h))]

    def get_q_std(self):
        return self._q_std
    def get_pwf(self):
        return self._pwf

    def _check_element_list(self):
        # check that z_out[i-1] = z_in[i]
        pass

    def solve_out_flow(self):
        self._check_element_list()
        self._elements[0].set_p_in(self._p_in)
        self._elements[0].set_t_in(self._t_in)
        if self._q_in is None:
            self._elements[0].set_q_std(self._q_std)
        else:
            self._elements[0].set_q_in(self._q_in)
        self._log('  Flow element: 1')
        self._elements[0].solve_out_flow()
        prev_element = self._elements[0]
        for i,element in enumerate(self._elements[1:]):
            element.set_p_in(prev_element.get_p_out()[-1])
            element.set_t_in(prev_element.get_t_out()[-1])
            element.set_q_in(prev_element.get_q_out()[-1])
            self._log(f'  Flow element: {i+2}')
            element.solve_out_flow()
            prev_element = element
        self.set_p_out(self._elements[-1].get_p_out()[-1])
        self.set_t_out(self._elements[-1].get_t_out()[-1])
        self.set_q_out(self._elements[-1].get_q_out()[-1])

    def solve_in_flow(self):
        self._check_element_list()
        self._elements[-1].set_p_out(self._p_out)
        self._elements[-1].set_t_out(self._t_out)
        if self._q_out is None:
            self._elements[-1].set_q_std(self._q_std)
        else:
            self._elements[-1].set_q_out(self._q_out)
        self._log(f'  Flow element: {len(self._elements)}')
        self._elements[-1].solve_in_flow()
        prev_element = self._elements[-1]
        for i,element in enumerate(self._elements[-2::-1]):
            element.set_p_out(prev_element.get_p_in()[0])
            element.set_t_out(prev_element.get_t_in()[0])
            element.set_q_out(prev_element.get_q_in()[0])
            self._log(f' Flow element: {len(self._elements) - i - 1}')
            element.solve_in_flow()
            prev_element = element
        self.set_p_in(self._elements[0].get_p_in()[0])
        self.set_t_in(self._elements[0].get_t_in()[0])
        self.set_q_in(self._elements[0].get_q_in()[0])

    def solve_reservoir(self, pwf):
        return self._reservoir.try_pwf(pwf, self._dt)

    def _pwf_error(self, pwf):
        if self._reservoir is None:
            q_std = self.ipr.get_q(pwf)
        else:
            qo_std, qw_std = self.solve_reservoir(pwf)
            q_std = qo_std + qw_std
            wfr = qw_std / q_std
            self.pvt.set_wfr(wfr)
        self.set_q_std(q_std)
        self.solve_in_flow()
        return pwf - self.get_p_in()[0]

    def solve_operation_point(self, pwf_test=None):
        self._log('Operation point search')
        if pwf_test is None:
            p0 = self.ipr.get_pr() * 0.98
        else:
            p0 = pwf_test
        f0 = self._pwf_error(p0)
        self._log(f' i=0, p={p0}, f={f0}')
        if pwf_test is None:
            p1 = self.ipr.get_pr() * 0.96
        else:
            p1 = pwf_test * 0.95
        f1 = self._pwf_error(p1)
        self._log(f' i=1, p={p1}, f={f1}')
        p_best = p0
        f_best = abs(f0)
        if abs(f1) < f_best:
            p_best = p1
            f_best = abs(f1)
        i = 0
        while i < self._max_iter and (abs(f1 - f0) > 1E-12):
            p2 = p1 - f1 * (p1 - p0) / (f1 - f0)
            f2 = self._pwf_error(p2)
            self._log(f' i={i+2}, p={p2}, f={f2}')
            if abs(f2) < f_best:
                p_best = p2
                f_best = abs(f2)
            if f_best < self._eps:
                break
            if abs(p2 - p1) < self._eps:
                break
            p0 = p1
            f0 = f1
            p1 = p2
            f1 = f2
            i += 1
        self._pwf = p_best
