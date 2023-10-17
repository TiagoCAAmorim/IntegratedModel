class VariablesList:
    def __init__(self, variables_list):
        self._variables = variables_list

    def get_list(self):
        out = dict()
        for k,v in self._variables.items():
            out[k] = list()
            for vi in v:
                out[k].append(vi)
        return out
    def print_list(self,indent=''):
        for k,v in self._variables.items():
            print(f'{indent}{k}: {v[0]} [{v[1]}]')
    def get_description(self, var):
        if var.lower() in self._variables.keys():
            return self._variables[var.lower()][0]
    def get_unit(self, var):
        if var.lower() in self._variables.keys():
            return self._variables[var.lower()][1]