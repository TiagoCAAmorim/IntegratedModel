import math
import common

class IPR:

    def __init__(self):
        self._pi = None
        self._pr = None
        
        self.variables = common.VariablesList({
            'pi':['Productivity index', 'm3/d/bar'],
            'pr':['Reservoir pressure', 'bar'],
            're':['Reservoir equivalent radius', 'm'],
            'rw':['Well radius', 'm'],
            'u':['Produced fluids mixture viscosity', 'cP'],
            'k':['Effective permeability', 'mD'],
            'h':['Length open to flow', 'm'],
            })          
        
    def set_pi(self, pi):
        self._pi = pi
    def get_pi(self):
        return self._pi
    def set_pr(self, pr):
        self._pr = pr
    def get_pr(self):
        return self._pr
    
    def get_q(self, pwf):
        return self._pi * (self._pr - pwf)
    
    def calculate_simple_pi(self, re, rw, k, mu, h):
        c = 2 * math.pi / (math.log(re / rw) - 3/4)
        self._pi = c * k * h / mu # Needs unit conversion!
