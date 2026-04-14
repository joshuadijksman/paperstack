
# Naam: Saladin Shah
# Studentnummer: 15817490


import numpy as np
import math as mt
import matplotlib.pyplot as plt
import csv as csv

coefficienten_1_lijst = []
coefficienten_2_lijst = []
coefficienten_3_lijst = []


a_lijst = [1, 2, 3]
b_lijst = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 30, 40, 45, 50, 55, 60]
#for b in b_lijst:
#    for a in a_lijst:
with open(f'/Users/noor/Documents/GitHub/2025-Projects_Team-1-Bouncing-on-Paper-The-Surprising-Restitution-Coefficient-of-a-Paper-Stack-/Code/{1}-{60}-M.csv', 'r') as yurr:
    hoogte_lijst = []
    frame_lijst = []
    teller = 0
    stuiteraantal = 0
    frame = 0

    for regel in yurr:
        data_opgeknipt = regel.strip().split()

        print(data_opgeknipt)
        if teller == 3:
            print('daggoe')
        else:    
            if data_opgeknipt and data_opgeknipt[0] != 'Frame':
                if data_opgeknipt and data_opgeknipt[0] != 'Tracks':
                    if data_opgeknipt and data_opgeknipt[0] != 'Track':
                        if frame >= 29:
                            frame = int(data_opgeknipt[0])
                            y1 = float(data_opgeknipt[4])
                            hoogte = 1000 - y1

                            frame_lijst.append(frame)
                            hoogte_lijst.append(hoogte)
                        else:
                            frame = int(data_opgeknipt[0])
                            y1 = float(data_opgeknipt[2])
                            hoogte = 1000 - y1

                            frame_lijst.append(frame)
                            hoogte_lijst.append(hoogte)        
                    else:
                        teller +=1
                else:
                    teller +=1
            else:
                teller +=1


    # Snelheden berekenen (voor bepaling van toppen)
    snelheden = []
    for i in range(1, len(hoogte_lijst)):
        dy = hoogte_lijst[i] - hoogte_lijst[i - 1]
        dt = tijd_lijst[i] - tijd_lijst[i - 1]
        snelheid = dy / dt if dt != 0 else 0
        snelheden.append(snelheid)


    print(snelheden)


    # Toppen detecteren: waar snelheid verandert van positief naar negatief
    maxima_tijden = [0]
    for i in range(1, len(snelheden)):
        if snelheden[i - 1] > 0 and snelheden[i] < 0 and len(maxima_tijden) <= 3 and i > 50:  # filter op realistische waarde
            maxima_tijden.append(i)

    print(maxima_tijden)


    # Hoogtes van de toppen
    maxima_hoogtes = [hoogte_lijst[i] for i in maxima_tijden]

    print(maxima_hoogtes)


    # Restitutiecoëfficiënten berekenen: hoogte_n / hoogte_(n-1)
    coefficienten = []
    cor1 = maxima_hoogtes[1] / maxima_hoogtes[0]
    cor2 = maxima_hoogtes[2] / maxima_hoogtes[1]
    cor3 = maxima_hoogtes[3] / maxima_hoogtes[2]

    coefficienten_1_lijst.append(cor1)
    coefficienten_2_lijst.append(cor2)
    coefficienten_3_lijst.append(cor3)


    print(cor1, cor2, cor3)

print(coefficienten_1_lijst)
print(coefficienten_2_lijst)
print(coefficienten_3_lijst)

#plt.plot(tijd_lijst, hoogte_lijst)
#plt.xlabel('Frame (geen eenheid)')
#plt.ylabel('Hoogte (px)')
#plt.show()

# errors toepassen
# error op aantal pixels (hoogte)
# error op frames?
#
#plt.errorbar(x,y, yerr=fouten, fmt = 'o', label='""')