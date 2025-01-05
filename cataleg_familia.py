#Script 4 de Python

# S'utilitza només per a afegir al catàleg cataleg_amb_satcat.txt una columna amb el nom de la família

# Creem arxiu: cataleg_amb_satcat_familia.txt


import pandas as pd
from collections import Counter
import re


dades = pd.read_csv('cataleg_amb_satcat.txt', delimiter='\t', header=None)
noms_sat = dades.iloc[:,12]

obs_sat = dict(Counter(noms_sat))
nom_sat = list(obs_sat.keys())
quantitat_obs_sat = list(obs_sat.values())

def class_string(s):
    match = re.match(r'^[a-zA-Z]+', s)
    if match:
        return match.group(0)
    return s 

dades['familia'] = dades.iloc[:,12].apply(class_string)

dades.to_csv('cataleg_amb_satcat_familia.txt', sep='\t', index=False, header=False)
