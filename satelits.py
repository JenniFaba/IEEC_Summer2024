#Creat per a fer un experiment a part. El podem considerar l'script 1.1.

#Utilitzat per veure quants dels satèl·lits observats han sigut observats més de 1000 vegades. Al final, però, com que fem la
#classifcació per famílies, no utilitzem més enllà la classificació donada per satèl·lits individuals.


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


dades = pd.read_csv('cataleg.txt', delimiter=' ')

objectes = dades.iloc[:,0]

sat = dict(Counter(objectes))
nom_sat = list(sat.keys())
#hi ha 820 sat diferents

quantitat_sat = []
for i in range(len(sat)):
    quantitat_sat.append(sat[nom_sat[i]])

# histograma
mean_mag = np.mean(quantitat_sat)
q5 = np.percentile(quantitat_sat, 5)
q95 = np.percentile(quantitat_sat, 95)

plt.hist(quantitat_sat, bins=150, edgecolor='blue')
plt.axvline(mean_mag, color='red', label='Mean')
plt.axvline(q5, color='green', label='5th Percentile')
plt.axvline(q95, color='green', label='95th Percentile')

plt.title('Histogram')
plt.xlabel('Quantitat Observacions')
plt.ylabel('Frequency')
plt.grid(False)
plt.show()
plt.close()

max_quantitat = np.max(quantitat_sat)
min_quantitat = np.min(quantitat_sat)

#un altre plot
sat_sorted = dict(sorted(sat.items(), key=lambda item: item[1]))
nom_sat = list(sat_sorted.keys())
quantitat_sat = []
for i in range(len(sat)):
    quantitat_sat.append(sat_sorted[nom_sat[i]])

plt.title('Quantitat observacions per satellit')
plt.bar(np.arange(0,820,1), quantitat_sat)
plt.xlabel('Satellits')
plt.ylabel('Nre observacions')
plt.show()
plt.close()
