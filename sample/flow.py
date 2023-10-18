import math
import pvt
import common

class SubFlowElement:

    def __init__(self):
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
            })
        
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
        self._q_in = self._m_rate / self.pvt.get_rhoo_in_place() * (24*60*60)
    def calculate_q_out(self):
        self.calculate_rhoo(self._p_out, self._t_out)
        self._q_out = self._m_rate / self.pvt.get_rhoo_in_place() * (24*60*60)

    def calculate_m_rate_in(self):
        self.calculate_rhoo(self._p_in, self._t_in)
        self._m_rate = self.pvt.get_rhoo_in_place() * self._q_in / (24*60*60)
    def calculate_m_rate_out(self):
        self.calculate_rhoo(self._p_out, self._t_out)
        self._m_rate = self.pvt.get_rhoo_in_place() * self._q_out / (24*60*60)
    
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
        htm = 0. # not implemented yet
        dv2 = self.calculate_delta_v2_g()
        return -1E-5 * self.pvt.get_rhoo_in_place() * self._g * (dz + hl + htm + dv2)
    
    def calculate_p_in(self):
        self._p_in = self._p_out - self.calculate_delta_p()
    def calculate_p_out(self):
        self._p_out = self._p_in + self.calculate_delta_p()

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
                calculate_q_function()
                calculate_v_function()
                break
            p_old = self.get_p()
            t_old = self.get_t()
            i += 1
        pass
    
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

    def __init__(self):
        super().__init__()
        self._n = 1
        self._elements = [] # SubFlowElement()

        self._variables = {
            'n':['Number of subdivisions', '-'],
            'elements':['List of SubFlowElements', '-']     
            }
        # self.variables = common.VariablesList(self._variables.update(super().variables.get_list()))
        
    def set_number_divisions(self, n):
        self._n = n
    def set_z_in(self,z):
        super().set_z_in(z)
    def set_z_out(self,z):
        super().set_z_out(z)
    def set_p_in(self,p):
        super().set_p_in(p)
    def set_p_out(self,p):
        super().set_p_out(p)
    def set_t_in(self,t):
        super().set_t_in(t)
    def set_t_out(self,t):
        super().set_t_out(t)
    def set_q_in(self,q):
        super().set_q_in(q)
    def set_q_out(self,q):
        super().set_q_out(q)
    def set_v_in(self,v):
        super().set_v_in(v)
    def set_v_out(self,v):
        super().set_v_out(v)
    def set_d(self,d):
        super().set_d(d)
    def set_e(self,e):
        super().set_e(e)
    def set_h(self,h):
        super().set_h(h)

    def get_z_in(self):
        return [element.get_z_in() for element in self._elements]
    def get_z_out(self):
        return [element.get_z_out() for element in self._elements]
    def get_p(self):
        return [element.get_p() for element in self._elements]
    def get_p_in(self):
        return [element.get_p_in() for element in self._elements]
    def get_p_out(self):
        return [element.get_p_out() for element in self._elements]
    def get_t(self):
        return [element.get_t() for element in self._elements]
    def get_t_in(self):
        return [element.get_t_in() for element in self._elements]
    def get_t_out(self):
        return [element.get_t_out() for element in self._elements]
    def get_m_rate(self):
        return [element.get_m_rate() for element in self._elements]
    def get_q(self):
        return [element.get_q() for element in self._elements]
    def get_q_in(self):
        return [element.get_q_in() for element in self._elements]
    def get_q_out(self):
        return [element.get_q_out() for element in self._elements]
    def get_v(self):
        return [element.get_v() for element in self._elements]
    def get_v_in(self):
        return [element.get_v_in() for element in self._elements]
    def get_v_out(self):    
        return [element.get_v_out() for element in self._elements]
    def get_d(self):
        return [element.get_d() for element in self._elements]
    def get_e(self):
        return [element.get_e() for element in self._elements]
    def get_h(self):
        return [element.get_h() for element in self._elements]
    def get_f(self):
        return [element.get_f() for element in self._elements]
    def get_re(self):
        return [element.get_re() for element in self._elements]
    def get_hl(self):
        return [element.get_hl() for element in self._elements]

    def get_h_cumulative(self):
        h = self.get_h()
        return [sum(h[:i + 1]) for i in range(len(h))]

    def _build_element_list(self):
        self._elements = [self.copy() for i in range(self._n)]
        for i, element in enumerate(self._elements):
            element._h = self._h / self._n
            element._z_in = self._z_in + i * (self._z_out - self._z_in)/ self._n
            element._z_out = self._z_in + (i + 1) * (self._z_out - self._z_in)/ self._n

    def solve_out_flow(self):
        self._build_element_list()
        self._elements[0].solve_out_flow()
        for i, element in enumerate(self._elements[1:]):
            self._elements[i+1].set_p_in(self._elements[i].get_p_out())
            self._elements[i+1].set_t_in(self._elements[i].get_t_out())
            self._elements[i+1].set_q_in(self._elements[i].get_q_out())
            self._elements[i+1].set_v_in(self._elements[i].get_v_out())
            self._elements[i+1].solve_out_flow()

    def solve_in_flow(self):
        self._build_element_list()
        self._elements[-1].solve_in_flow()
        n = self._n
        for i, element in enumerate(self._elements[-2::-1]):
            self._elements[n-i-2].set_p_out(self._elements[n-i-1].get_p_in())
            self._elements[n-i-2].set_t_out(self._elements[n-i-1].get_t_in())
            self._elements[n-i-2].set_q_out(self._elements[n-i-1].get_q_in())
            self._elements[n-i-2].set_v_out(self._elements[n-i-1].get_v_in())
            self._elements[n-i-2].solve_in_flow()

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

