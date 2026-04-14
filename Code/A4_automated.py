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

fout_coefficienten_1_h_lijst = []
fout_coefficienten_2_h_lijst = []
fout_coefficienten_3_h_lijst = []

fout_coefficienten_1_v_lijst = []
fout_coefficienten_2_v_lijst = []
fout_coefficienten_3_v_lijst = []


a_lijst = [1, 2, 3]
b_lijst = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 30, 40, 45, 50, 55, 60, 100, 140, 200, 240, 300, 340]
papier_lijst = []

for b in b_lijst:
  for a in a_lijst:
        with open(f'E:/Documents/GitHub/2025-Projects_Team-1-Bouncing-on-Paper-The-Surprising-Restitution-Coefficient-of-a-Paper-Stack-/Code/A4 Medium knikker (blauw)/{a}-{b}-M.csv', 'r') as yurr:
            hoogte_lijst = []
            frame_lijst = []
            frame_delta = 0
            teller = 0
            stuiteraantal = 0
            delta_hoogte = 600

            for regel in yurr:
                data_opgeknipt = regel.strip().split()

                if teller == 3:
                    print()
                else:    
                    if data_opgeknipt and data_opgeknipt[0] != 'Frame':
                        if data_opgeknipt and data_opgeknipt[0] != 'Tracks':
                            if data_opgeknipt and data_opgeknipt[0] != 'Track':
                                if float(data_opgeknipt[2]) < 60:
                                    frame_delta = int(data_opgeknipt[0])
                                    if float(data_opgeknipt[2]) < delta_hoogte:
                                        delta_hoogte = float(data_opgeknipt[2])
                                        echte_hoogte = 678.33695 - float(data_opgeknipt[2])
                                else:
                                    frame = int(data_opgeknipt[0]) - frame_delta
                                    y1 = float(data_opgeknipt[2])
                                    hoogte = 678.33695 - y1

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

            # print(tijd_lijst)

            # fout op tijd 
            fout_tijd_lijst = []
            for i in range(0, len(tijd_lijst)):
                fout_tijd_lijst.append(0.0025)
            
            # print(fout_tijd_lijst)

            # fout op Hoogte
            fout_hoogte_lijst= []
            for i in range(0,len(hoogte_lijst)):
                fout_hoogte_lijst.append(1) # wat is de fout op de pixels?

            # Snelheden berekenen (voor bepaling van toppen)
            snelheden = []

            for i in range(0, len(hoogte_lijst)):
                dy = hoogte_lijst[i] - hoogte_lijst[i - 1]
                dt = frame_lijst[i] - frame_lijst[i - 1]
                snelheid = dy / dt if dt != 0 else 0
                snelheden.append(snelheid)
            
            fout_snelheden_lijst=[]
            for element in range(0, len(snelheden)):
                fout_snelheid = snelheden[element] * ((fout_hoogte_lijst[element]/hoogte_lijst[element])**2 + (fout_tijd_lijst[element]/tijd_lijst[element])**2)**0.5
                fout_snelheden_lijst.append(fout_snelheid)

            # Toppen detecteren: waar snelheid verandert van positief naar negatief
            maxima_frames = [0]
            maxima_hoogtes = [echte_hoogte]
            maxima_tijden_schatting= []
            maxima_hoogte_schatting= []
            fout_maxima_hoogte = []
            impact_frames = []
            impact_snelheden = []

            for i in range(0, len(snelheden)):
                if snelheden[i - 1] > 0 and snelheden[i] < 0 and len(maxima_frames) <= 4 and i > 20:  # filter op realistische waarde
                    maxima_frames.append(i)
                    maxima_hoogtes.append(hoogte_lijst[i])
                    schatting_max_hoogte = hoogte_lijst[i-1] + (snelheden[i - 1]/(snelheden[i - 1] - snelheden[i])) * (hoogte_lijst[i] - hoogte_lijst[i-1])
                    schatting_max_tijd = tijd_lijst[i - 1] + (snelheden[i - 1]/(snelheden[i - 1] - snelheden[i])) * 0.005
                    fout_maximale_hoogte = ((1-(snelheden[i-1]/(snelheden[i-1]-snelheden[i])))**2 * (fout_hoogte_lijst[i-1])**2 + (snelheden[i-1]/(snelheden[i-1]-snelheden[i]))**2 * (fout_hoogte_lijst[i])**2 + ((snelheden[i]*(hoogte_lijst[i] - hoogte_lijst[i-1]))/((snelheden[i-1] - snelheden[i])**2))**2 * (fout_snelheden_lijst[i-1])**2 + ((snelheden[i-1]* (hoogte_lijst[i]-hoogte_lijst[i-1]))/((snelheden[i-1]-snelheden[i])**2))**2 * (fout_snelheden_lijst[i])**2) **0.5
                    maxima_tijden_schatting.append(schatting_max_tijd)
                    maxima_hoogte_schatting.append(schatting_max_hoogte)
                    fout_maxima_hoogte.append(fout_maximale_hoogte)
                if snelheden[i - 1] < 0 and snelheden[i] > 0 and len(impact_snelheden) <= 3 and i > 20:
                    impact_snelheden.append(abs(snelheden[i - 4]))
                    impact_snelheden.append(snelheden[i + 1])
                    impact_frames.append(i - 4)
                    impact_frames.append(i + 1)

            print(f'maximum points zijn {maxima_frames}')
            print(f'maximum hoogtes zijn {maxima_hoogtes}')


            # Restitutiecoëfficiënten berekenen: hoogte_n / hoogte_(n-1)
            coefficienten_h = []
            cor1_h = maxima_hoogtes[1] / maxima_hoogtes[0]
            fout_cor1_h = cor1_h * ((fout_maxima_hoogte[1]/maxima_hoogte_schatting[1])**2 + (fout_maxima_hoogte[0]/maxima_hoogte_schatting[0])**2)**0.5
            # cor2_h = maxima_hoogtes[2] / maxima_hoogtes[1]
            #fout_cor2_h = cor2_h * ((fout_maxima_hoogte[2]/maxima_hoogte_schatting[2])**2 + (fout_maxima_hoogte[1]/maxima_hoogte_schatting[1])**2)**0.5
            # cor3_h = maxima_hoogtes[3] / maxima_hoogtes[2]
            # fout_cor3_h = cor3_h * ((fout_maxima_hoogte[3]/maxima_hoogte_schatting[3])**2 + (fout_maxima_hoogte[2]/maxima_hoogte_schatting[2])**2)**0.5

            coefficienten_v = []
            cor1_v = impact_snelheden[1] / impact_snelheden[0]
            # cor2_v = impact_snelheden[3] / impact_snelheden[2]
            # cor3_v = impact_snelheden[3] / impact_snelheden[2]

            coefficienten_1_h_lijst.append(cor1_h)
            fout_coefficienten_1_h_lijst.append(fout_cor1_h)
            # coefficienten_2_h_lijst.append(cor2_h)
            # coefficienten_3_lijst.append(cor3_h)

            coefficienten_1_v_lijst.append(cor1_v)
            # coefficienten_2_v_lijst.append(cor2_v)
            # coefficienten_3_v_lijst.append(cor3_v)

            plt.figure(1, figsize=(15, 15))
            plt.suptitle('A4 Format. Position and speed graphs, of all measurements combined (messy)')
            plt.subplot(211)
            plt.title('Height over time, all measurements')
            plt.plot(frame_lijst, hoogte_lijst, label=b)
            plt.errorbar(frame_lijst, hoogte_lijst, yerr=fout_hoogte_lijst)
            plt.xlabel('Time (frames)')
            plt.ylabel('Height (px)')
            # plt.legend()
            # plt.show()
          
            plt.subplot(212)
            plt.title('Speed over time, all measurements')
            plt.plot(frame_lijst, snelheden, label=b)
            plt.xlabel('Time (frames)')
            plt.ylabel('Speed (px/frame)')
            # plt.xlim(0, 400)
            # plt.ylim(-20, 20)
            plt.savefig('A4_AUTOMATED_POS_AND_SPEED.png')

            test_max_snelheid.append(max(snelheden))
            # print(cor1, cor2, cor3)
            test_minimale_hoogte.append(min(hoogte_lijst))
            
            print(f'impact frames zijn: {impact_frames}')
            print(f'impact snelheden zijn: {impact_snelheden}')
            print(f'File: {a}-{b}')
            
            papier_lijst.append(b)

# print(impact_snelheden)


plt.figure(2, figsize=(15, 10))
plt.suptitle('A4 Format. CoR against amount of paper pages, all measurements')
plt.subplot(221)
plt.title('CoR calculated with height ratio (h_after_bounce / h_initial)')
# plt.plot(papier_lijst, coefficienten_1_h_lijst, 'o', label='h1/h0 (first bounce)', markersize = '2')
plt.errorbar(papier_lijst, coefficienten_1_h_lijst, yerr=fout_coefficienten_1_h_lijst, fmt='o', ecolor = "black", label='h1/h0 (first bounce)', markersize = '2')
# plt.plot(papier_lijst, coefficienten_2_h_lijst, 'o', label='h2/h1 (second bounce)')
# plt.plot(papier_lijst, coefficienten_3_h_lijst, label='h3/h2 (third bounce)')
plt.xlabel('# of paper pages (amount)')
plt.ylabel('Restitutioncoefficient (ratio)')
# plt.ylim(0, 0.6)
plt.legend()


plt.subplot(222)
plt.title('CoR calculated with speed ratio (v_after_impact / v_before_impact)')
plt.plot(papier_lijst, coefficienten_1_v_lijst, 'o', label='v1/v0 (first impact)')
# plt.plot(papier_lijst, coefficienten_2_v_lijst, 'o', label='v2/v1 (second impact)')
# plt.plot(papier_lijst, coefficienten_3_v_lijst, label='v3/v2 (third impact)')
plt.xlabel('# of paper pages (amount)')
plt.ylabel('Restitutioncoefficient (ratio)')
# plt.ylim(0, 0.6)
plt.legend()
plt.savefig('A4_AUTOMATED_COR.png')
plt.show()


print(min(test_minimale_hoogte))
print(max(test_max_snelheid))