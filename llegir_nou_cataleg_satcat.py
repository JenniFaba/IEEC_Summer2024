#Script 3 de Python

#A partir de cataleg_complet.txt i de l'arxiu satcat.tsv, catàleg on es troben classificats els diferents satèl·lits.
# Aquest últim conté informació addicional, pel que fusionem ambdòs catàlegs (comparant els noms dels satèl·lits que ja teniem
# per tal de completar el nostre.

#Creem l'arxiu: 'cataleg_amb_satcat.txt'


import pandas as pd
import re


# header_list=['JCAT',	'Satcat',	'Piece',	'Type',	'Name',	'PLName',	'LDate',	'Parent',	'SDate',	'Primary', 'DDate',	'Status',	'Dest',	'Owner',	'State',	'Manufacturer',	'Bus',	'Motor',	'Mass',	'MassFlag',	'DryMass',	'DryFlag',	'TotMass',	'TotFlag',	'Length',	'LFlag',	'Diameter',	'DFlag',	'Span',	'SpanFlag',	'Shape',	'ODate',	'Perigee',	'PF',	'Apogee',	'AF',	'Inc',	'IF',	'OpOrbit',	'OQUAL',	'AltNames']
dades_satcat = pd.read_csv('satcat.tsv', delimiter='\t', header=0)
dades_cataleg = pd.read_csv('cataleg_complet.txt', delimiter='\t', header=None)

dades_satcat = dades_satcat.iloc[1:,:] #treure primera fila de Nans
noms = dades_satcat.iloc[:,2]


noms_format = []
noms1 = []
pattern = re.compile(r'\d\d\d\d')
for i in range(1,len(noms)+1,1):
    if pattern.findall(noms[i]):
        if len(noms[i])==9:
            if '-' in noms[i]:
                noms1.append(noms[i])
                noms_format.append(noms[i].replace("-", ""))

noms_cataleg = dades_cataleg.iloc[:,0]
noms_cataleg = noms_cataleg.copy()
noms_cataleg_I = []
for i in range(len(noms_cataleg)):
    noms_cataleg_I.append(noms_cataleg[i].replace("I", "", 1))

for i in range(len(noms_format)):
    noms_format[i]=noms_format[i][2:]



dades_cataleg['nou_nom1'] = noms_cataleg_I
dades_cataleg_format = dades_cataleg[dades_cataleg.iloc[:, 11].isin(noms_format)]
dades_satcat_format = dades_satcat[dades_satcat.iloc[:,2].isin(noms1)]

dades_satcat_1 = dades_satcat_format[['Piece', 'Length', 'Diameter', 'Apogee', 'Perigee', 'Name', ]]
dades_satcat_1 = dades_satcat_1.copy()
dades_satcat_1['nou_nom2'] = noms_format

length = []
diameter = []
apogee = []
perigee = []
nom_sat = []
nou_nom = []
noms_dict = {dades_satcat_1.iloc[i,6]: i for i in range(len(dades_satcat_1))}
for i in range(len(dades_cataleg_format)):
    if dades_cataleg_format.iloc[i,11] in noms_format:
        j = noms_dict[dades_cataleg_format.iloc[i,11]]
        length.append(float(dades_satcat_1.iloc[j,1]))
        diameter.append(float(dades_satcat_1.iloc[j,2]))
        apogee.append(int(dades_satcat_1.iloc[j,3]))
        perigee.append(int(dades_satcat_1.iloc[j,4]))
        nom_sat.append(dades_satcat_1.iloc[j,5])
        nou_nom.append(dades_satcat_1.iloc[j,0])

height = []
for i in range(len(dades_cataleg_format)):
    height.append((apogee[i]+perigee[i])/2)

dades_satcat_format = dades_satcat_format.copy()
dades_cataleg_format['nom_sat'] = nom_sat
dades_cataleg_format['length'] = length
dades_cataleg_format['diameter'] = diameter
dades_cataleg_format['apogee'] = apogee
dades_cataleg_format['perigee'] = perigee
dades_cataleg_format['height'] = height
dades_cataleg_format['nou_nom1'] = nou_nom

dades_cataleg_format.to_csv('cataleg_amb_satcat.txt', sep='\t', index=False, header=False)

