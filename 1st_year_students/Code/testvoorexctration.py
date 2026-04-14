# Naam: Saladin Shah
# Studentnummer: 15817490


import numpy as np
import math as mt
import matplotlib.pyplot as plt
import csv as csv

test_max_snelheid = []
test_minimale_hoogte = []
coefficienten_1_lijst = []
coefficienten_2_lijst = []
coefficienten_3_lijst = []

# deze heeft alle huidige met data op 1 column
# order_lijst = ["2-1", "3-1", "1-2", "2-2", "3-2", "1-4", "3-4", "1-6", "2-6", "3-6", "1-8", "3-8", "3-10", "1-12", "3-12", "1-14", "2-14", "3-14", "1-16", "2-16", "3-16", "1-30", "2-45", "2-60"]

order_lijst = ["2-1", "2-2", "3-4", "2-6", "3-8", "3-10", "3-12", "2-14", "2-16", "1-30", "2-45", "2-60"]
a_lijst = [1, 2, 3]
b_lijst = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 30, 40, 45, 50, 55, 60]
#for b in b_lijst:
#    for a in a_lijst:
# for o in order_lijst:
with open(f'C:/Users/salad/Documents/GitHub/2025-Projects_Team-1-Bouncing-on-Paper-The-Surprising-Restitution-Coefficient-of-a-Paper-Stack-/Code/A5 Medium knikker (blauw)/1-60-B-A5-imp.csv', 'r') as yurr:
    hoogte_lijst = []
    tijd_lijst = []
    teller = 0
    stuiteraantal = 0

    for regel in yurr:
        data_opgeknipt = regel.strip().split()

        print(data_opgeknipt)

        if teller == 3:
            print('daggoe')
        else:    
            if data_opgeknipt and data_opgeknipt[0] != 'Frame':
                if data_opgeknipt and data_opgeknipt[0] != 'Tracks':
                    if data_opgeknipt and data_opgeknipt[0] != 'Track':
                        tijd = int(data_opgeknipt[0])
                        y1 = float(data_opgeknipt[2])
                        hoogte = 659.0764 - y1

                        tijd_lijst.append(tijd)
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


    # Toppen detecteren: waar snelheid verandert van positief naar negatief
    maxima_tijden = [0]
    for i in range(1, len(snelheden)):
        if snelheden[i - 1] > 0 and snelheden[i] < 0 and len(maxima_tijden) <= 3 and i > 60:  # filter op realistische waarde
            maxima_tijden.append(i)

    print(maxima_tijden)


    # Hoogtes van de toppen
    maxima_hoogtes = [hoogte_lijst[i] for i in maxima_tijden]

    # print(maxima_hoogtes)


    # Restitutiecoëfficiënten berekenen: hoogte_n / hoogte_(n-1)
    coefficienten = []
    cor1 = maxima_hoogtes[1] / maxima_hoogtes[0]
    cor2 = maxima_hoogtes[2] / maxima_hoogtes[1]
    # cor3 = maxima_hoogtes[3] / maxima_hoogtes[2]

    coefficienten_1_lijst.append(cor1)
    coefficienten_2_lijst.append(cor2)
    # coefficienten_3_lijst.append(cor3)

    plt.figure(1)
    plt.plot(tijd_lijst, hoogte_lijst)
    plt.xlabel("Time (frames)")
    plt.ylabel('Height (px)')
    # plt.ylim(0, 200)
    # plt.show()

    test_max_snelheid.append(max(snelheden))
    # print(cor1, cor2, cor3)
    test_minimale_hoogte.append(min(hoogte_lijst))

print(coefficienten_1_lijst)
print(coefficienten_2_lijst)
print(coefficienten_3_lijst)

# papier_lijst = [1, 1, 2, 2, 2, 4, 4, 6, 6, 6, 8, 8, 10, 12, 12, 14, 14, 14, 16, 16, 16, 30, 45, 60]
papier_lijst = [1, 2, 4, 6, 8, 10, 12, 14, 16, 30, 45, 60]

#    plt.figure(2)
#   plt.plot(papier_lijst, coefficienten_1_lijst, label='h1/h0 (first bounce)')
#   plt.plot(papier_lijst, coefficienten_2_lijst, label='h2/h1 (second bounce)')
#   plt.plot(papier_lijst, coefficienten_3_lijst, label='h3/h2 (third bounce)')

plt.xlabel('# of paper pages (amount)')
plt.ylabel('Restitutioncoefficient (ratio)')
plt.legend()
plt.show()

print(min(test_minimale_hoogte))
print(max(test_max_snelheid))