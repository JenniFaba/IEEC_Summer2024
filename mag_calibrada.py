#Script 2 de Python.

# A partir de l'arxiu mag0.txt, afegim una nova columna al nostre catàleg amb la magnitud corregida (on es té en compte la magnitud
# instrumental i el punt 0 de l'aparell).

#Obtenim el l'arxiu: cataleg_complet.txt


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



dades = pd.read_csv('cataleg.txt', delimiter=' ')
arxiu_mag = pd.read_csv('mag0.txt', delimiter = '\t', header=None)

#dades arxiu imatges mag 0
nom_imatges = [x.replace('V', 'U') for x in arxiu_mag[0]]
nom_imatges = [x.replace('.fits.gz', '') for x in nom_imatges]
nom_imatges = [x.replace('imatges3', 'imatges') for x in nom_imatges]
nom_imatges = [x.replace('imatges5', 'imatges') for x in nom_imatges]
nom_imatges = np.asarray(nom_imatges)
mag_0 = np.array(arxiu_mag.iloc[:,1])


index_nonull = np.where(mag_0!=0)
nom_imatges_net = nom_imatges[index_nonull]
mag_0net = mag_0[index_nonull]


# només ens quedem amb les files que tenen el nom de la imatge que te mag0 (valor no NULL a la columna)
dades_filtre = dades[dades.iloc[:, 9].isin(nom_imatges_net)]
nom_cataleg = np.array(dades_filtre.iloc[:,9])
mag = np.array(dades_filtre.iloc[:,6])

plt.hist(mag, bins=100, edgecolor='blue')
mean_mag = np.mean(mag)
q5 = np.percentile(mag, 5)
q95 = np.percentile(mag, 95)
plt.axvline(mean_mag, color='red', label='Mean')
plt.axvline(q5, color='green', label='5th Percentile')
plt.axvline(q95, color='green', label='95th Percentile')

plt.title('Histogram')
plt.xlabel('Instrumental magnitude')
plt.ylabel('Frequency')
plt.grid(False)
plt.show()

mag_cal = np.zeros(len(mag))
imatges_dict = {nom_imatges_net[i]: i for i in range(len(nom_imatges_net))}
for j in range(len(nom_cataleg)):
    if nom_cataleg[j] in imatges_dict:
        i = imatges_dict[nom_cataleg[j]]
        mag_cal[j] = mag[j] - 25.65 + mag_0net[i]

dades_filtre = dades_filtre.copy()
dades_filtre['mag_calibrada'] = mag_cal
dades_filtre.to_csv('cataleg_complet.txt', sep='\t', index=False, header=False)

