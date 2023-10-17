import math
import pvt
import common

class FlowElement:

    def __init__(self):
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
    
    def calculate_velocity(self):
        self._v = 4 * self._m_rate / (self.pvt.get_rhoo_in_place() * math.pi() * self._d ** 2)
    
    def calculate_Reynolds(self):
        self._re = 4 * self._m_rate / (self.pvt.get_uo() * math.pi() * self._d)

    def calculate_f(self):
        if self._re < 2300:
            self._f = 64 / self._re
        else:
            self._f = 0.0055 * (1 + math.pow(2E4 * self._e / self._d + 1E6 / self._re, 1/3.))

    def calculate_head_loss(self):
        self._hl = self._f * self._h * self._v ** 2 / (self._d * 2 * self._g)



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

