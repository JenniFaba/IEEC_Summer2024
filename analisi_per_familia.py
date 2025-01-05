#Script 6 de Python

#Procedim amb l'anàlisi final del catàleg, en el què fem els polar plots i altres gràfiques relacionades amb les magnituds i les òrbites

#Separem els casos per famílies, en total trobem que n'hi ha 45 amb més de 200 observacions en total. Treballem amb aquestes.



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from collections import Counter
from scipy.optimize import curve_fit


#carregar fitxer
dades_cataleg = pd.read_csv('cataleg_final.txt', delimiter='\t', header=None)

#escollir familia
families = dict(Counter(dades_cataleg.iloc[:,18]))

noms_families= list(families.keys())
quantitat_sat_familia  = list(families.values())


#més de 200
threshold = 200 #families tal que tenen més de 200 observacions
families200 = {k: v for k, v in families.items() if v > threshold}

noms_families200 = list(families200.keys())
quantitat_sat_familia200  = list(families200.values())


#histograma families
plt.figure(figsize=(10, 6))
plt.bar(noms_families200, quantitat_sat_familia200)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.title('Histogram')
plt.xlabel('Family names')
plt.ylabel('Frequency')
plt.show()
plt.close()


#familia particular
familia_esc = dades_cataleg.iloc[:,18][0]
dades_familia = dades_cataleg[dades_cataleg.iloc[:,18] == familia_esc]



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


#Intent d'adjustos, deixo el codi per a futures ocasions.
# #poly
# degree = 1
# coefficients = np.polyftit(mag, h, degree)
# polynomial = np.poly1d(coefficients)
# x_fit1 = np.linspace(mag.min(), mag.max(), 100)
# y_fit1 = polynomial(x_fit1)

#exp
# def sin_model(x, a, b, c):
#     return a*np.sin(b*x)+c

# popt, pcov = curve_fit(sin_model, data, mag,  p0=(250,7, 3))
# a, b, c = popt

# x_fit = np.linspace(data.min(), data.max(), 100)
# y_fit = sin_model(x_fit, *popt)


plt.scatter(data, mag)
# plt.plot(x_fit1, y_fit1, color='red', label=f'Pol Fit (degree {degree})')
# plt.plot(x_fit, y_fit, color='green', label=f'Sin Fit (a={a:.3f}, b={b:.3f})')
plt.xlabel('Julian Date')
plt.ylabel('Calibrated magnitude')
plt.title(familia_esc)
plt.show()


plt.scatter(mag,h)
# plt.plot(x_fit1, y_fit1, color='red', label=f'Pol Fit (degree {degree})')
# plt.plot(x_fit, y_fit, color='green', label=f'Sin Fit (a={a:.3f}, b={b:.3f})')
plt.xlabel('Calibrated Magnitude')
plt.ylabel('Height')
plt.title(familia_esc)
plt.show()


# #geo: 35786km>meo> leo: <2000km
mean_apo = np.mean(apo) #llarg
mean_peri = np.mean(peri) #curt

plt.hist(apo, bins=100, edgecolor='blue')
plt.axvline(mean_apo, color='red', label='Mean')
plt.title('Histogram')
plt.xlabel('Apogee')
plt.ylabel('Frequency')
plt.grid(False)
plt.show()
plt.close()

plt.hist(peri, bins=100, edgecolor='blue')
plt.axvline(mean_peri, color='red', label='Mean')
plt.title('Histogram')
plt.xlabel('Perigee')
plt.ylabel('Frequency')
plt.grid(False)
plt.show()
plt.close()



# #separar segons alçades orbites (nomes en cas que peri i apo no siguin semblants)
# index_orbita = np.where((apo>mean_apo))
# h = h[index_orbita]
# data = data[index_orbita]
# mag = mag[index_orbita]
# alt = alt[index_orbita]
# az = az[index_orbita]
# alt_sun = alt_sun[index_orbita]
# az_sun = az_sun[index_orbita]
# peri = peri[index_orbita]
# apo = apo[index_orbita]
# length = length[index_orbita]
# diametre = diametre[index_orbita]



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


# no corregit
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_facecolor('darkblue')


colors = [(1, 0, 0), (1, 0.65, 0), (1, 1, 0), (1, 1, 1)]
cmap_name = 'custom_cmap'
custom_cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=50)

ax.set_theta_offset(np.pi/2)
ax.set_theta_direction(-1)
sc = ax.scatter(az_val, alt_val, c = mag_val, cmap = custom_cmap, s = 5, alpha = 0.8)
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
fig.text(0.05, 0.8, 'No corregida', fontsize=12, color='black')
fig.text(0.05, 0.7, f'Geo Transfer. Height: {np.mean(h_val):.4f}km', fontsize=12, color='black')
# Height: {np.mean(height_val_no_out):.4f}km
plt.title(familia_esc)
plt.show()
plt.close()


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