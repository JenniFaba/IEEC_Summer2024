#Script 5 de Python

# Utilitzem les dades TLE disponibles dels satèl·lits observats per tal de poder ampliar la informació del catàleg.
# La informació que ens interessa es l'alçada de l'òrbita en el moment de la observació.
# Per tal d'aconseguir-ho trobem el TLE més pròxim a la data d'observació i n'usem les dades associades. 
# Calculem l'alçada a partir de: SMA - e*cos(mA)-6378 (https://www.orbiter-forum.com/threads/so-you-want-to-calculate-orbits.24431/)


#Obtenim l'arxiu: cataleg_final.txt


import pandas as pd
import numpy as np
from datetime import datetime
from astropy.time import Time
from collections import Counter
import glob 
import os



dades_cataleg = pd.read_csv('cataleg_amb_satcat_familia.txt', delimiter='\t', header=None)
dades_cataleg = dades_cataleg.dropna(subset=[14])
dades_cataleg = dades_cataleg.dropna(subset=[13])
# mirar si hi havia algun que no tingués dades a long/diam
dades_cataleg['area'] = dades_cataleg.iloc[:,13]*dades_cataleg.iloc[:,14]


string_names = glob.glob("C:\\Users\\jenni\\OneDrive\\Escritorio\\practiques_estiu2024\\montsec\\scripts_python\\TLEs\\*.tle")
names = []

for i in range(len(string_names)):
    filename = string_names[i]
    # print(filename)
    with open(filename) as file:
        for index, line in enumerate(file):
            processedline = line.rstrip()
            filename = os.path.basename(string_names[i])
            names.append((processedline, filename))


names = np.asarray(names, dtype="object")

tles = []

#julian date, escollim la mitjanit
def nova_data(date_str):
    dia = date_str[:8]
    dia_format = f"{dia[:4]}-{dia[4:6]}-{dia[6:]}"
    dia_iso = f"{dia_format}T00:00:00"
    return dia_iso


def datetime_to_julian(date_str):
    jd = Time(date_str, format='isot', scale='utc').jd
    return jd


for i in range(0, len(names), 3): #organitzar tles en 3
    if i + 2 < len(names): 
        tle_lines = [names[i][0], names[i+1][0], names[i+2][0]] 
        tles.append(tle_lines[1:])
            

def read_tle(tle): #funcio per a retornar valors dels tles

    values = {}
    format_msg = "{} {} {}.{} {} {} {} {} {} {} {} {}"

    name = tle[0][9:17].strip()
    str_year = int(tle[0][18:20])
    year = 1900 + str_year if str_year >= 57 else 2000 + str_year
    day_frac = tle[0][24:32]
    str_date = "{} {}".format(year, tle[0][20:23])
    epoch = datetime.strptime(str_date, "%Y %j")
    decay = float(tle[0][33:43])
    inclination = float(tle[1][8:16])
    ascending_node = float(tle[1][17:25])
    eccentricity = float("0."+tle[1][26:33])
    perigee = float(tle[1][34:42])
    anomaly = float(tle[1][43:51])
    motion = float(tle[1][52:63])
    num = int(tle[1][63:68])

    orbit = format_msg.format(epoch.year, epoch.month,
                                        epoch.day, day_frac,
                                        inclination, ascending_node,
                                        eccentricity, perigee,
                                        anomaly, motion, decay, num)
    
    return orbit


result = []
for i in range(len(tles)):
    result.append((tles[i], datetime_to_julian(nova_data(names[i][1][25:40])), tles[i][0][9:15]))#crear nou info: info tle, julian date, nom del satellit

for i in range(len(result)): #no cal
    result[i][0][0] = result[i][0][0].replace("+", "")
    result[i][0][0] = result[i][0][0].replace("-", "")

for i in range(len(result)): #treure espais de la última columna
    original= result[i][0][1]
    if original[-6] == " ":
        unida = original.rsplit(' ', 1)
        modified_string = ''.join(unida)
        result[i][0][1] = modified_string

tle_dades = []

#alguns outliers en el format
result[30268][0][1] = result[30268][0][1][:16] + result[30268][0][1][17:33] + " " + result[30268][0][1][33:]
result[30269][0][1] = result[30269][0][1][:16] + result[30269][0][1][17:33] + " " + result[30269][0][1][33:]


for i in range(len(result)):
    tle_dades.append(read_tle(result[i][0]))


dades_noves = []
for i in range(len(result)):
    dades_noves.append((tle_dades[i], result[i][1], result[i][2]))


dades_noves = pd.DataFrame(dades_noves)
nova_info_values = []

for i in range(len(dades_cataleg)):
    key = dades_cataleg.iloc[i,0][1:] 
    info_sate = dades_noves[dades_noves[2] == key] #trobem la info associada al satellit i
    if not info_sate.empty:
        differences = np.abs(info_sate[1] - dades_cataleg.iloc[i, 1])
        min_index = differences.idxmin() #escollim el periode més proper
        nova_info_value = dades_noves.iloc[min_index, 0]
        nova_info_values.append(nova_info_value) #adjuntem la info nova al satellit i
    else:
        nova_info_values.append(None)

dades_cataleg['nova info'] = nova_info_values #adjuntem dades al catàleg dels tles

quantitat_per_dia = dict(Counter(dades_cataleg['nova info'])) #només per a saber que no tots són iguals

dades_cataleg_net =  (dades_cataleg.dropna()).reset_index(drop=True)
dades_cataleg_net['nova info'] = dades_cataleg_net['nova info'].str.split()
dades_cataleg_net =  (dades_cataleg_net.dropna()).reset_index(drop=True)

sma = (dades_cataleg_net.iloc[:,15]+6378+dades_cataleg_net.iloc[:,16]+6378)/2


h = []
for i in range(len(dades_cataleg_net)):
    e = float(dades_cataleg_net.iloc[i,20][5])
    mA = float(dades_cataleg_net.iloc[i,20][7])
    h.append(sma[i] - e*np.cos(mA)-6378)


dades_cataleg_net = dades_cataleg_net.copy()
dades_cataleg_net['h'] = h

dades_cataleg_net.to_csv('cataleg_final.txt', sep='\t', index=False, header=False)






#proba d'en david
# tle1 = "1 47961U 21022AF  24193.16283766  .00473297  00000-0  17806-2 0  9998"
# tle2 = "2 47961  97.4504 106.7449 0007893  91.2899 268.9276 15.86621967182006"
#         2 99998  70.1585 307.6409 0004000  06.3100 304.0400  6.42724015000004
    
