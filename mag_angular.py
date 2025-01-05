# Script 6.1 de Python

# 1. Calculem l'angle sòlid que ocupen els satèllits a l'espai (Omega = A/dist^2), per intentar trobar-ne una relació amb la magnitud
#https://lco.global/spacebook/sky/using-angles-describe-positions-and-apparent-sizes-objects/

#2. Polar plot de tots els satèl·lits geoestacionaris junts. Intentem veure algun gradient en la magnitud.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from collections import Counter

#carregar fitxer
dades_cataleg = pd.read_csv('cataleg_final.txt', delimiter='\t', header=None)


# 1. Angle sòlid
#dades
alt = np.array(dades_cataleg.iloc[:,4])
az = np.array(dades_cataleg.iloc[:,5])
alt_sun = np.array(dades_cataleg.iloc[:,7])
az_sun = np.array(dades_cataleg.iloc[:,8])
area = np.array(dades_cataleg.iloc[:,19])
h = np.array(dades_cataleg.iloc[:,21])
mag = np.array(dades_cataleg.iloc[:,10])

#outliers en les alçades
Q1 = np.percentile(h,25)
Q3 = np.percentile(h,75)
IQR = Q3 - Q1

lower_thres = Q1 - 3* IQR
upper_thres = Q3 + 3 * IQR

index_bo = np.where((h >= lower_thres) & (h <= upper_thres))
h = h[index_bo]
area = area[index_bo]
mag = mag[index_bo]
alt = alt[index_bo]
az = az[index_bo]
alt_sun = alt_sun[index_bo]
az_sun = az_sun[index_bo]


#outliers mags
Q1a = np.percentile(mag,25)
Q3a = np.percentile(mag,75)
IQRa = Q3a - Q1a

lower_thresa = Q1a - 3 * IQRa
upper_thresa = Q3a + 3 * IQRa

index_boa = np.where((mag >= lower_thresa) & (mag <= upper_thresa))
h = h[index_boa]
area = area[index_boa]
mag = mag[index_boa]
alt = alt[index_boa]
az = az[index_boa]
alt_sun = alt_sun[index_boa]
az_sun = az_sun[index_boa]


Omega = area / ((h*1000)*(h*1000))
# theta = area * 206.265 / (h*1000) #Angle que ocupa en 1D

plt.scatter(Omega, mag)
plt.xlabel('Solid Angle')
plt.ylabel('Calibrated magnitude')
plt.show()



#2. Polar plot de tots els geoestacionaris junts
#escollir familia
families = dict(Counter(dades_cataleg.iloc[:,18]))

threshold = 200 #families tal que tenen més de 200 observacions
families200 = {k: v for k, v in families.items() if v > threshold}

noms_families200 = list(families200.keys())
quantitat_sat_familia200  = list(families200.values())


index = [0,2,3,4,8,10,12,13,15,20,24,25,26,27,28,29,30,31,33,34,35,37,38,39,41,43]

familia_esc = np.array(noms_families200)[[0,2,3,4,8,10,12,13,15,20,24,25,26,27,28,29,30,31,33,34,35,37,38,39,41,43]]

dades_familia = dades_cataleg[dades_cataleg.iloc[:,18].isin(familia_esc)]

#dades
alt = np.array(dades_familia.iloc[:,4])
az = np.array(dades_familia.iloc[:,5])
alt_sun = np.array(dades_familia.iloc[:,7])
az_sun = np.array(dades_familia.iloc[:,8])
peri = np.array(dades_familia.iloc[:,16])
apo = np.array(dades_familia.iloc[:,15])
length = np.array(dades_familia.iloc[:,13])
diametre = np.array(dades_familia.iloc[:,14])
height = np.array(dades_familia.iloc[:,17]) #de la mitjana de perigeu apogeu, però usem h, la calculada amb la fórmula
h = np.array(dades_familia.iloc[:,21])
mag = np.array(dades_familia.iloc[:,10])
data = np.array(dades_familia.iloc[:,1])
area = np.array(dades_cataleg.iloc[:,19])


#outliers en les alçades
Q1 = np.percentile(h,25)
Q3 = np.percentile(h,75)
IQR = Q3 - Q1

lower_thres = Q1 - 3* IQR
upper_thres = Q3 + 3 * IQR

index_bo = np.where((h >= lower_thres) & (h <= upper_thres))
h = h[index_bo]
data = data[index_bo]
mag = mag[index_bo]
alt = alt[index_bo]
az = az[index_bo]
alt_sun = alt_sun[index_bo]
az_sun = az_sun[index_bo]
peri = peri[index_bo]
apo = apo[index_bo]
length = length[index_bo]
diametre = diametre[index_bo]
area = area[index_bo]

#outliers mags
Q1a = np.percentile(mag,25)
Q3a = np.percentile(mag,75)
IQRa = Q3a - Q1a

lower_thresa = Q1a - 3 * IQRa
upper_thresa = Q3a + 3 * IQRa

index_boa = np.where((mag >= lower_thresa) & (mag <= upper_thresa))
h = h[index_boa]
data = data[index_boa]
mag = mag[index_boa]
alt = alt[index_boa]
az = az[index_boa]
alt_sun = alt_sun[index_boa]
az_sun = az_sun[index_boa]
peri = peri[index_boa]
apo = apo[index_boa]
length = length[index_boa]
diametre = diametre[index_boa]
area = area[index_boa]


# polar plot
#altituds positives
valid_index = np.where(alt>0)
alt_sun_val = alt_sun[valid_index]
az_sun_val = az_sun[valid_index]
alt_val = alt[valid_index]
az_val = az[valid_index]
mag_val = mag[valid_index]
height_val = height[valid_index]
peri_val = peri[valid_index]
apo_val = apo[valid_index]
length_val = length[valid_index]
diametre_val = diametre [valid_index]
h_val = h[valid_index]
area_val = area[valid_index]


az_rotada = []
# alt_rotada = []
for i in range(len(az_val)):
    az_rotada.append(az_val[i]-az_sun_val[i])
    # alt_rotada.append(alt_val[i]-alt_sun_val[i])


#adjusts
alt_val = 90- alt_val
#canviar az a rad
az_val = np.array(az_val*np.pi/180)
az_rotada = np.array(az_rotada)*np.pi/180


#corregit
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_facecolor('darkblue')


colors = [(1, 0, 0), (1, 0.65, 0), (1, 1, 0), (1, 1, 1)]
cmap_name = 'custom_cmap'
custom_cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=50)

ax.set_theta_offset(np.pi/2)
ax.set_theta_direction(-1)
sc = ax.scatter(az_rotada, alt_val, c = mag_val, cmap = custom_cmap, s = 5, alpha = 0.8)
ax.set_rlim([0,90])
ax.set_rticks([0,15,30,45,60,75,90])
ax.set_xticklabels(['N','NE','E','SE','S','SW','W','NW'])
ax.set_yticklabels(['90','75','60','45','30','15','0'])
cbar = plt.colorbar(sc)
cbar.set_label('Magnitude')
fig.text(0.05, 0.3, f'Perigee: {np.mean(peri_val):.4f}km', fontsize=12, color='black')
fig.text(0.05, 0.4, f'Apogee: {np.mean(apo_val):.4f}km', fontsize=12, color='black')
fig.text(0.05, 0.5, f'Length: {np.mean(length_val):.4f}m', fontsize=12, color='black')
fig.text(0.05, 0.6, f'Diameter: {np.mean(diametre_val):.4f}m', fontsize=12, color='black')
fig.text(0.05, 0.8, 'Corregida', fontsize=12, color='black')
fig.text(0.05, 0.7, f'Geo. Height: {np.mean(h_val):.4f}km', fontsize=12, color='black')
# Height: {np.mean(height_val_no_out):.4f}km
plt.title('Geo')
plt.show()
plt.close()