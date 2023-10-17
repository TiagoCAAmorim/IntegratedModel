import math
import pvt
import common

class FlowElement:

    def __init__(self):
        self._eps = 1E-6
        self._max_iter = 100
        self._g = 9.81 # m/s^2

        self._z_in = 0
        self._z_out = 0
        self._p = None
        self._p_in = None
        self._p_out = None
        self._t = None
        self._t_in = None
        self._t_out = None

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
        
        self.variables = common.VariablesList({
            'z_in':['Inlet height', 'm'],
            'z_out':['Outlet height', 'm'],
            'p':['Average pressure', 'bar'],
            'p_in':['Inlet pressure', 'bar'],
            'p_out':['Outlet pressure', 'bar'],
            't':['Average temperature', 'oC'],
            't_in':['Inlet temperature', 'oC'],
            't_out':['Outlet temperature', 'oC'],

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
            })
        
    def set_z_in(self,z):
        self._z_in = z
    def set_z_out(self,z):
        self._z_out = z
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
    def set_v_in(self,v):
        self._v_in = v
    def set_v_out(self,v):
        self._v_out = v
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
    def get_t_out(self):
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

    def calculate_m_rate(self):
        self.calculate_rhoo(self._p_in, self._t_in)
        self._m_rate = self.pvt.get_rhoo_in_place() * self._q_in / (24*60*60)
    
    def calculate_v_in(self):
        self.calculate_rhoo(self._p_in, self._t_in)
        self._v_in = 4 * self._m_rate / (self.pvt.get_rhoo_in_place() * math.pi * self._d ** 2)

    def calculate_v_out(self):
        self.calculate_rhoo(self._p_out, self._t_out)
        self._v_out = 4 * self._m_rate / (self.pvt.get_rhoo_in_place() * math.pi * self._d ** 2)
    
    def calculate_uo(self, p, t):
        self.pvt.set_t(t)
        self.pvt.set_p(p)
        self.pvt.calculate_rs_Standing()
        self.pvt.calculate_uo_do_Standing()
        self.pvt.calculate_uo_Standing()

    def calculate_Reynolds(self):
        self.calculate_uo(self._p, self._t)
        self._re = 4 * self._m_rate / (self.pvt.get_uo()/1000 * math.pi * self._d)

    def calculate_f(self):
        if self._re < 2300:
            self._f = 64 / self._re
        else:
            self._f = 0.0055 * (1 + math.pow(2E4 * self._e / self._d + 1E6 / self._re, 1/3.))

    def calculate_head_loss(self):
        self._hl = self._f * self._h * self._v ** 2 / (self._d * 2 * self._g)

    def calculate_p_out(self):
        self.calculate_rhoo(self._p_out, self._t_out)
        dz = self._z_out - self._z_in
        self.calculate_Reynolds()
        self.calculate_f()
        self.calculate_v_in()
        self.calculate_v_out()
        self.calculate_v()
        self.calculate_head_loss()
        hl = self._hl
        htm = 0. # not implemented yet
        dv2 = (self._v_out ** 2 - self._v_in ** 2) / (2 * self._g)
        self._p_out = self._p_in - 1E-5 * self.pvt.get_rhoo_in_place() * self._g * (dz + hl + htm + dv2)

    def solve_out_flow(self):
        self.calculate_m_rate()
        self.set_p_out(self._p_in)
        self.set_t_out(self._t_in)
        self.calculate_p()
        self.calculate_t()
        p_old = self.get_p()
        t_old = self.get_t()
        i = 0
        while i<self._max_iter:        
            self.calculate_p_out()
            # self.calculate_t_out() # not implemented yet
            self.calculate_p()
            self.calculate_t()
            if abs(p_old - self._p) < self._eps and abs(t_old - self._t) < self._eps:
                break
            p_old = self.get_p()
            t_old = self.get_t()
            i += 1
        pass

class IPR:

    def __init__(self):
        self._pi = None
        self._pr = None
        self._re = None
        self._rw = None
        self._u = None
        self._h = None
        
        self.variables = common.VariablesList({
            'pi':['Productivity index', 'm3/d/bar'],
            'pr':['Reservoir pressure', 'bar'],
            're':['Reservoir equivalent radius', 'm'],
            'rw':['Well radius', 'm'],
            'u':['Produced fluids mixture viscosity', 'cP'],
            'h':['Length open to flow', 'm'],
            })

