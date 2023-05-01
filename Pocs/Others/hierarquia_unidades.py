import pandas as pd
import json

unidades = pd.DataFrame({
    'id': [1,2,3,4,5,6],
    'nome': [
        'Matriz',
        'Unidade 1', 
        'Unidade 2', 
        'Unidade 1.1', 
        'Unidade 2.1', 
        'Unidade 1.1.1'
    ],
    'unidadeId': [0, 1, 1, 2, 3, 4]
    })

class Hierarchy:

    def __init__(self, data, data_name, recursive_key, columns=None):
        self.data = data
        self.data_name = data_name
        self.recursive_key = recursive_key
        self.properties = {k for k in self.data.keys() if (columns is None or k in columns)}

    def build_json(self, output_data=[], father=0):
        output_data = []
        for _, d in self.data[self.data[self.recursive_key] == father].iterrows():
            body = {p : d[p] for p in self.properties}
            output_data.append({
            **body,
            self.data_name: self.build_json(output_data, d['id'])
        })
        return output_data

hierarquia_unidades = Hierarchy(data=unidades, data_name='unidades', recursive_key='unidadeId', columns=['id', 'nome'])
output_data = hierarquia_unidades.build_json()
print(json.dumps(output_data, indent=2))