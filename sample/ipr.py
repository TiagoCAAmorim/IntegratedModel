import math
import common

class IPR:

    def __init__(self):
        self._pi = None
        self._pr = None

        self.variables = common.VariablesList({
            'pi':['Productivity index', 'm3/d/bar'],
            'pe':['Drainage area mean pressure', 'bar'],
            're':['Drainage radius', 'm'],
            'rw':['Well radius', 'm'],
            'u':['Produced fluids mixture viscosity', 'cP'],
            'k':['Effective permeability', 'mD'],
            'h':['Length open to flow', 'm'],
            })

    def set_pi(self, pi):
        self._pi = pi
    def set_pr(self, pr):
        self._pr = pr

    def get_pi(self):
        return self._pi
    def get_pr(self):
        return self._pr

    def get_q(self, pwf):
        return self._pi * (self._pr - pwf)

    def calculate_pi_pseudopermanent(self, re, rw, k, mu, h, Bo, S):
        a = 1 / 18.662 # 19.03 * 0.980665
        c = 1 / (math.log(re / rw) - 3/4 + S)
        self._pi = a * c * k * h / (Bo * mu)

    def calculate_pi_permanent(self, re, rw, k, mu, h, Bo, S):
        a = 1 / 18.662 # 19.03 * 0.980665
        c = 1 / (math.log(re / rw) - 1/2 + S)
        self._pi = a * c * k * h / (Bo * mu)
