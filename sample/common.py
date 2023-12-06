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

def make_columns_file(list1, list2, column_name1, column_name2, file_name):
    if len(list1) != len(list2):
        print("Error: Lists must have the same length.")
        return
    with open(file_name, 'w') as file:
        file.write(f"{column_name1}\t{column_name2}\n")
        for val1, val2 in zip(list1, list2):
            file.write(f"{val1}\t{val2}\n")