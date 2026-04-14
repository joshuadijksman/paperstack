# Naam: Saladin Shah
# Studentnummer: 15817490


import numpy as np
import math as mt
import matplotlib.pyplot as plt
import csv as csv

test_max_snelheid = []
test_minimale_hoogte = []
coefficienten_1_h_lijst = []
coefficienten_2_h_lijst = []
coefficienten_3_h_lijst = []
coefficienten_1_v_lijst = []
coefficienten_2_v_lijst = []
coefficienten_3_v_lijst = []

# deze heeft alle huidige met data op 1 column
order_lijst = ["2-1", "3-1", "1-2", "2-2", "3-2", "1-4", "3-4", "1-6", "2-6", "3-6", "1-8", "3-8", "3-10", "1-12", "3-12", "1-14", "2-14", "3-14", "1-16", "2-16", "3-16", "1-30", "2-45", "2-60"]

# order_lijst = ["2-1", "2-2", "3-4", "2-6", "3-8", "3-10", "3-12", "2-14", "2-16", "1-30", "2-45", "2-60"]
a_lijst = [1, 2, 3]
b_lijst = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 30, 40, 45, 50, 55, 60]
for b in b_lijst:
   for a in a_lijst:
# for o in order_lijst:
        with open(f'{a}-{b}-M.csv', 'r') as yurr:
            hoogte_lijst = []
            tijd_lijst = []
            teller = 0
            stuiteraantal = 0

            for regel in yurr:
                data_opgeknipt = regel.strip().split()

                if teller == 3:
                    print('daggoe')
                else:    
                    if data_opgeknipt and data_opgeknipt[0] != 'Frame':
                        if data_opgeknipt and data_opgeknipt[0] != 'Tracks':
                            if data_opgeknipt and data_opgeknipt[0] != 'Track':
                                tijd = int(data_opgeknipt[0])
                                y1 = float(data_opgeknipt[2])
                                hoogte = 678.43695 - y1

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
            snelhedenN = []
            n = 1

            for i in range(1, len(hoogte_lijst)):
                dy = hoogte_lijst[i] - hoogte_lijst[i - 1]
                dt = tijd_lijst[i] - tijd_lijst[i - 1]
                dyn = hoogte_lijst[i - n] - hoogte_lijst[i - n - 1]
                dtn = tijd_lijst[i - n] - tijd_lijst[i - n - 1]
                snelheid = dy / dt if dt != 0 else 0
                snelheidn = dyn / dtn if dtn != 0 else 0
                snelhedenN.append(snelheidn)
                snelheden.append(snelheid)


            # Toppen detecteren: waar snelheid verandert van positief naar negatief
            maxima_tijden = [0]
            impact_tijden = []
            impact_snelheden = []
            j = 0
            for i in range(1, len(snelheden)):
                if snelheden[i - 1] > 0 and snelheden[i] < 0 and len(maxima_tijden) <= 3 and i > 60:  # filter op realistische waarde
                    maxima_tijden.append(i)
                if snelheden[i - 1] < 0 and snelheden[i] > 0 and len(impact_snelheden) <= 1 and i > 60:
                    j = i
                    impact_snelheden.append(abs(snelheden[i - 1]))
                    impact_snelheden.append(snelheden[i])
                    impact_tijden.append(i - 1)
                    impact_tijden.append(i)

            print(f'maximum points zijn {maxima_tijden}')


            # Hoogtes van de toppen
            maxima_hoogtes = [hoogte_lijst[i] for i in maxima_tijden]
            # print(maxima_hoogtes)


            # Restitutiecoëfficiënten berekenen: hoogte_n / hoogte_(n-1)
            coefficienten_h = []
            cor1_h = maxima_hoogtes[1] / maxima_hoogtes[0]
            cor2_h = maxima_hoogtes[2] / maxima_hoogtes[1]
            # cor3_h = maxima_hoogtes[3] / maxima_hoogtes[2]

            coefficienten_v = []
            cor=[]
            m_list = []
            #cor1_v = impact_snelheden[1] / impact_snelheden[0]
            for m in range(1,20):
                cor1_v = abs(snelheden[j+m]) / abs(snelheden[j-m])
                cor.append(cor1_v)
                m_list.append(m)

            print("Frame of impact:", j)
            print("Velocity used for cor:", snelheden[j-1], snelheden[j+1])
            # cor1_v = cor1_v**2
            # cor2_v = impact_snelheden[3] / impact_snelheden[2]
            # cor3_v = impact_snelheden[3] / impact_snelheden[2]

            coefficienten_1_h_lijst.append(cor1_h)
            coefficienten_2_h_lijst.append(cor2_h)
            # coefficienten_3_lijst.append(cor3_h)

            coefficienten_1_v_lijst.append(cor1_v)
            # coefficienten_2_v_lijst.append(cor2_v)
            # coefficienten_3_v_lijst.append(cor3_v)

            # plt.figure(1)
            # plt.plot(tijd_lijst, hoogte_lijst)
            # plt.xlabel("Time (frames)")
            # plt.ylabel('Height (px)')
            # plt.ylim(0, 200)
            # plt.show()

            snelheden.append(0)            
            plt.figure(4)
            plt.plot(tijd_lijst, snelheden)
            plt.xlim(0, 400)
            plt.ylim(-20, 20)

            test_max_snelheid.append(max(snelheden))
            # print(cor1, cor2, cor3)
            test_minimale_hoogte.append(min(hoogte_lijst))
            print(impact_tijden)
            print(impact_snelheden)

# print(coefficienten_1_lijst)
# print(coefficienten_2_lijst)
# print(coefficienten_3_lijst)
# print(impact_snelheden)

papier_lijst = [1, 1, 1, 2, 2, 2, 4, 4, 4, 6, 6, 6, 8, 8, 8, 10, 10, 10, 12, 12, 12, 14, 14, 14, 16, 16, 16, 18, 18, 18, 20, 20, 20, 30, 30, 30, 40, 40, 40, 45, 45, 45, 50, 50, 50, 55, 55, 55, 60, 60, 60]
# papier_lijst = [1, 2, 4, 6, 8, 10, 12, 14, 16, 30, 45, 60]

plt.figure(2)
plt.plot(papier_lijst, coefficienten_1_h_lijst, 'o', label='h1/h0 (first bounce)')
# plt.plot(papier_lijst, coefficienten_2_h_lijst, 'o', label='h2/h1 (second bounce)')
# plt.plot(papier_lijst, coefficienten_3_h_lijst, label='h3/h2 (third bounce)')

plt.xlabel('# of paper pages (amount)')
plt.ylabel('Restitutioncoefficient (ratio)')
plt.legend()
# plt.show()


plt.figure(3)
plt.plot(papier_lijst, coefficienten_1_v_lijst, 'o', label='v1/v0 (first impact)')
# plt.plot(papier_lijst, coefficienten_2_v_lijst, 'o', label='v2/v1 (second impact)')
# plt.plot(papier_lijst, coefficienten_3_v_lijst, label='v3/v2 (third impact)')

# plt.ylim(0, 0.6)
plt.xlabel('# of paper pages (amount)')
plt.ylabel('Restitutioncoefficient (ratio)')
plt.legend()
plt.show()

plt.figure(4)
plt.plot(tijd_lijst, snelheden)
plt.xlim(0, 400)
plt.ylim(-20, 20)

print(min(test_minimale_hoogte))
print(max(test_max_snelheid))