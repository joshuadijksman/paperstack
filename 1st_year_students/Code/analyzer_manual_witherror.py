# Naam: Saladin Shah
# Studentnummer: 15817490

import numpy as np
import matplotlib.pyplot as plt\

from scipy import stats
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
with open(f'E:/Documents/GitHub/2025-Projects_Team-1-Bouncing-on-Paper-The-Surprising-Restitution-Coefficient-of-a-Paper-Stack-/Code/A4 Medium knikker (blauw)/1-1-M.csv', 'r') as yurr:
    hoogte_lijst = []
    frame_lijst = []
    teller = 0
    stuiteraantal = 0
    frame = 0

    for regel in yurr:
        data_opgeknipt = regel.strip().split()

        #print(data_opgeknipt)
        if teller == 3:
            print('daggoe')
        else:    
            if data_opgeknipt and data_opgeknipt[0] != 'Frame':
                if data_opgeknipt and data_opgeknipt[0] != 'Tracks':
                    if data_opgeknipt and data_opgeknipt[0] != 'Track':
                        if frame >= 29:
                            frame = int(data_opgeknipt[0])
                            y1 = float(data_opgeknipt[2])
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

    tijd_lijst = []
    # 1 frame = 1/200 seconden
    for element in range(0,len(frame_lijst)):
        tijd_lijst.append((1/200) * frame_lijst[element])

    print(tijd_lijst)

    # fout op tijd 
    fout_tijd_lijst = []
    for i in range(0, len(tijd_lijst)):
        fout_tijd_lijst.append(0.0025)
    
    print(fout_tijd_lijst)

    # fout op Hoogte
    fout_hoogte_lijst= []
    for i in range(0,len(hoogte_lijst)):
        fout_hoogte_lijst.append(1) # wat is de fout op de pixels?

    plt.plot(tijd_lijst, hoogte_lijst, 'r-')
    plt.xlabel('tijd in seconden')
    plt.ylabel('hoogte in pixels')
    plt.xlim(0.1,0.3)
    plt.errorbar(tijd_lijst, hoogte_lijst, xerr = fout_tijd_lijst, yerr = fout_hoogte_lijst)
    plt.show()

    # Snelheden berekenen (voor bepaling van toppen) in pixels/s
    snelheden_lijst = []
    for i in range(1, len(hoogte_lijst)):
        dy = hoogte_lijst[i] - hoogte_lijst[i - 1]
        dt = tijd_lijst[i] - tijd_lijst[i - 1]
        snelheid = dy / dt if dt != 0 else 0
        snelheden_lijst.append(snelheid)

    print(snelheden_lijst)
    
    fout_snelheden_lijst=[]
    for element in range(0, len(snelheden_lijst)):
        fout_snelheid = snelheden_lijst[element] * ((fout_hoogte_lijst[element]/hoogte_lijst[element])**2 + (fout_tijd_lijst[element]/tijd_lijst[element])**2)**0.5
        fout_snelheden_lijst.append(fout_snelheid)

    print(fout_snelheden_lijst)

    # Toppen detecteren: waar snelheid verandert van positief naar negatief
    maxima_tijden = [0]
    maxima_tijden_schatting= [0]
    maxima_hoogte_schatting= [0]
    fout_maxima_hoogte =[0]
    for i in range(1, len(snelheden_lijst)):
        if snelheden_lijst[i - 1] > 0 and snelheden_lijst[i] < 0 and len(maxima_tijden) <= 3 and i > 50:  # filter op realistische waarde
            maxima_tijden.append(tijd_lijst[i])
            schatting_max_hoogte = hoogte_lijst[i-1] + (snelheden_lijst[i - 1]/(snelheden_lijst[i - 1] - snelheden_lijst[i])) * (hoogte_lijst[i] - hoogte_lijst[i-1])
            schatting_max_tijd = tijd_lijst[i - 1] + (snelheden_lijst[i - 1]/(snelheden_lijst[i - 1] - snelheden_lijst[i])) * 0.005
            fout_maximale_hoogte= ((1-(snelheden_lijst[i-1]/(snelheden_lijst[i-1]-snelheden_lijst[i])))**2 * (fout_hoogte_lijst[i-1])**2 + (snelheden_lijst[i-1]/(snelheden_lijst[i-1]-snelheden_lijst[i]))**2 * (fout_hoogte_lijst[i])**2 + ((snelheden_lijst[i]*(hoogte_lijst[i] - hoogte_lijst[i-1]))/((snelheden_lijst[i-1] - snelheden_lijst[i])**2))**2 * (fout_snelheden_lijst[i-1])**2 + ((snelheden_lijst[i-1]* (hoogte_lijst[i]-hoogte_lijst[i-1]))/((snelheden_lijst[i-1]-snelheden_lijst[i])**2))**2 * (fout_snelheden_lijst[i])**2) **0.5
            maxima_tijden_schatting.append(schatting_max_tijd)
            maxima_hoogte_schatting.append(schatting_max_hoogte)

    print(maxima_tijden)
    print(maxima_tijden_schatting)
    print(maxima_hoogte_schatting)
    print(fout_maxima_hoogte)

    # # Restitutiecoëfficiënten berekenen: hoogte_n / hoogte_(n-1)
    # coefficienten = []
    cor1 = maxima_hoogtes[1] / maxima_hoogtes[0]
    fout_cor1 = cor1 * ((fout_maxima_hoogte[1]/maxima_hoogte_schatting[1])**2 + (fout_maxima_hoogte[0]/maxima_hoogte_schatting[0])**2)**0.5
    cor2 = maxima_hoogtes[2] / maxima_hoogtes[1]
    fout_cor2 = cor2 * ((fout_maxima_hoogte[2]/maxima_hoogte_schatting[2])**2 + (fout_maxima_hoogte[1]/maxima_hoogte_schatting[1])**2)**0.5
    cor3 = maxima_hoogtes[3] / maxima_hoogtes[2]
    fout_cor3 = cor3 * ((fout_maxima_hoogte[3]/maxima_hoogte_schatting[3])**2 + (fout_maxima_hoogte[2]/maxima_hoogte_schatting[2])**2)**0.5

    # coefficienten_1_lijst.append(cor1)
    # coefficienten_2_lijst.append(cor2)
    # coefficienten_3_lijst.append(cor3)


    # print(cor1, cor2, cor3)

# print(coefficienten_1_lijst)
# print(coefficienten_2_lijst)
# print(coefficienten_3_lijst)

#plt.plot(tijd_lijst, hoogte_lijst)
#plt.xlabel('Frame (geen eenheid)')
#plt.ylabel('Hoogte (px)')
#plt.show()