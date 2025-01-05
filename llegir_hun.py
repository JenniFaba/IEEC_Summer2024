#Script 1 de Pyhton

#Llegim els arxius hun i n'extraiem la informació útil. Usem algunes llibreries de python per a obtenir la posició del Sol
#en el moment de la observació i la posició de l'objecte en altitud i azimuth.
#Creem l'arxiu: cataleg.txt


import glob 
import numpy as np
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, Angle
from astropy.time import Time
import astropy.units as u
import ephem
import pandas as pd
import matplotlib.pyplot as plt


string_names = glob.glob("C:\\Users\\jenni\\OneDrive\\Escritorio\\practiques_estiu2024\\montsec\\dades\\*.hun")
names = []
for i in range(len(string_names)):
    filename = string_names[i]
    with open(filename) as file:
        for index, line in enumerate(file):
            if index!=0:
                processedline = line.rstrip()
                list_names = processedline.split()
                names.append(list_names)

names = np.asarray(names, dtype="object")

#l’objecte, la data d’observació, les coordenades, la magnitud, i si la traça és vàlida o no, 
# i el nom de la imatge original (agafar només els valid =y i selected = True)

dades_reduides = [[] for i in range(len(names))]
columnes = [0, 1, 2, 3, 4, 7, 16, 18] #object, date, ra, dec, mag, valid, name_file, selected
for i in range(len(names)):
    for j in columnes:
        dades_reduides[i].append(names[i][j])

counter=0
for i in range(len(dades_reduides)):
    if dades_reduides[i][5]=='y':
        counter +=1


dades_seleccionades = []
for i in range(len(dades_reduides)):
    if dades_reduides[i][5]=='y':
        dades_seleccionades.append(dades_reduides[i])

dades_seleccionades = np.asarray(dades_seleccionades, dtype="object")
 
#julian date
def datetime_to_julian(date_str):
    jd = Time(date_str, format='isot', scale='utc').jd
    return jd
# YYYY-MM-DD HH:MM:SS.sss

time_gregorian=[]
for i in range(len(dades_seleccionades)):
    dades_seleccionades[i][5]=dades_seleccionades[i][6]
    time_gregorian.append(dades_seleccionades[i,1])
    dades_seleccionades[i][1]=datetime_to_julian(dades_seleccionades[i][1])


#dades_seleccionades conté les columnes que volem i la data en calendari julià
dades_seleccionades = dades_seleccionades[:,:6]

#objecte, julià, ra, dec, mag, name_image


#canvi de coordenades (RA,DE)-->(h, az)
#ICRS frame (International Celestial Reference System)


# TJO location
# per a les coord (alt, az) del Sol en cada instant
# sobre ephem (de la home page):  
# An input string '1.23' is parsed as degrees of declination (or hours, when setting right ascension) but a float 1.23 is assumed to be in radians. 
# Angles returned by PyEphem are even more confusing: print them, and they display degrees; but do math with them, and you will find they are radians.


jds = []
for i in range(len(dades_seleccionades)):
    jds.append(dades_seleccionades[i][1]) #les julian dates inicials. ephem no reconeix aquest format

JDS = Time(jds, format = 'jd').datetime #el format que reconeix ephem es el datetime

TJO = ephem.Observer()
TJO.lat = '42:03:05' 
TJO.lon = '00:43:46'
TJO.elevation = 1570

sun = ephem.Sun()

#Fem prova per veure que tot quadra (és a dir, màxims a migdia i mínims a mitjanit)
alt_sun, az_sun = [], [] 
for jd in JDS:
    TJO.date = jd
    sun.compute(TJO)
    alt_sun.append(sun.alt)
    az_sun.append(sun.az)


alt_sun = np.array(alt_sun)*180/np.pi #ephem dona radiants, ho passem a graus
az_sun = np.array(az_sun)*180/np.pi

plt.plot(JDS, alt_sun, '.')
plt.show()
plt.close()

plt.plot(JDS, az_sun, '.')
plt.show()
plt.close()



# per al reference frame
latitude = 42+3/60+5/3600
longitude = 43/60+46/3600
altitude = 1570
location = EarthLocation(lat=latitude * u.deg, lon=longitude * u.deg, height=altitude * u.m)

#magnituds instrumentals sense N
mag = dades_seleccionades[:,4]
# mag-25,65+noves (punt zero) (no agafar les que no tinguin punt 0)
mag_withoutN = [float(x.replace('N', '')) for x in mag]


dades_noves = []
for i in range(len(dades_seleccionades)):
    celestial_coords = SkyCoord(float(dades_seleccionades[i,2]) * u.deg, float(dades_seleccionades[i,3]) * u.deg, frame='icrs')
    altaz_frame = AltAz(obstime=Time(time_gregorian[i], format='isot', scale='utc'), location=location)
    spherical_coords = celestial_coords.transform_to(altaz_frame)
    dades_noves.append((dades_seleccionades[i][0], dades_seleccionades[i][1], dades_seleccionades[i,2], dades_seleccionades[i,3], Angle(spherical_coords.alt, unit='deg').degree, Angle(spherical_coords.az,unit='deg').degree, mag_withoutN[i], alt_sun[i], az_sun[i], dades_seleccionades[i][5] ))

dades_noves = np.array(dades_noves).reshape(len(dades_seleccionades), 10)

#creem el catàleg amb les primeres dades
dades_noves_frame = pd.DataFrame(dades_noves)
dades_noves_frame.to_csv('cataleg.txt', sep=' ', header=False, index=False)

        
