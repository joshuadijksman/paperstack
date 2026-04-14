# Naam: Saladin Shah
# Studentnummer: 15817490


import numpy as np
import math as mt
import matplotlib.pyplot as plt
import csv as csv


test_max_snelheid = []
test_minimale_hoogte = []

coefficienten_1_h_M_lijst = []
coefficienten_2_h_M_lijst = []
coefficienten_3_h_M_lijst = []

coefficienten_1_h_K_lijst = []
coefficienten_2_h_K_lijst = []
coefficienten_3_h_K_lijst = []

coefficienten_1_v_M_lijst = []
coefficienten_2_v_M_lijst = []
coefficienten_3_v_M_lijst = []

coefficienten_1_v_K_lijst = []
coefficienten_2_v_K_lijst = []
coefficienten_3_v_K_lijst = []

starting_height_M = []
starting_height_K = []



a_lijst = ['M', 'K']
b_lijst = [1, 2, 3, 4]

for b in b_lijst:
  for a in a_lijst:
        with open(f'E:/Documents/GitHub/2025-Projects_Team-1-Bouncing-on-Paper-The-Surprising-Restitution-Coefficient-of-a-Paper-Stack-/Code/HOOGTETESTS/HT-{b}-{a}.csv', 'r') as yurr:
            hoogte_lijst = []
            frame_lijst = []
            teller = 0
            stuiteraantal = 0

            for regel in yurr:
                data_opgeknipt = regel.strip().split()

                if teller == 3:
                    print()
                else:    
                    if data_opgeknipt and data_opgeknipt[0] != 'Frame':
                        if data_opgeknipt and data_opgeknipt[0] != 'Tracks':
                            if data_opgeknipt and data_opgeknipt[0] != 'Track':
                                frame = int(data_opgeknipt[0])
                                y1 = float(data_opgeknipt[2])
                                hoogte = 656.4737 - y1

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

            for i in range(0, len(hoogte_lijst)):
                dy = hoogte_lijst[i] - hoogte_lijst[i - 1]
                dt = frame_lijst[i] - frame_lijst[i - 1]
                snelheid = dy / dt if dt != 0 else 0
                snelheden.append(snelheid)


            # Toppen detecteren: waar snelheid verandert van positief naar negatief
            maxima_frames = [0]
            impact_frames = []
            impact_snelheden = []
            for i in range(0, len(snelheden)):
                if snelheden[i - 1] > 0 and snelheden[i] < 0 and len(maxima_frames) <= 3 and i > 20:  # filter op realistische waarde
                    maxima_frames.append(i)
                if snelheden[i - 1] < 0 and snelheden[i] > 0 and len(impact_snelheden) <= 3 and i > 20:
                    impact_snelheden.append(abs(snelheden[i - 4]))
                    impact_snelheden.append(snelheden[i + 1])
                    impact_frames.append(i - 4)
                    impact_frames.append(i + 1)

            print(f'maximum points zijn {maxima_frames}')


            # Hoogtes van de toppen
            maxima_hoogtes = [hoogte_lijst[i] for i in maxima_frames]
            # print(maxima_hoogtes)


            # Restitutiecoëfficiënten berekenen: hoogte_n / hoogte_(n-1)
            coefficienten_h = []
            cor1_h = maxima_hoogtes[1] / maxima_hoogtes[0]
            cor2_h = maxima_hoogtes[2] / maxima_hoogtes[1]
            # cor3_h = maxima_hoogtes[3] / maxima_hoogtes[2]

            coefficienten_v = []
            cor1_v = impact_snelheden[1] / impact_snelheden[0]
            cor2_v = impact_snelheden[3] / impact_snelheden[2]
            # cor3_v = impact_snelheden[3] / impact_snelheden[2]

            if a == 'M':
                starting_height_M.append(maxima_hoogtes[0])
                coefficienten_1_h_M_lijst.append(cor1_h)
                coefficienten_2_h_M_lijst.append(cor2_h)
                # coefficienten_3_lijst.append(cor3_h)

                coefficienten_1_v_M_lijst.append(cor1_v)
                coefficienten_2_v_M_lijst.append(cor2_v)
                # coefficienten_3_v_lijst.append(cor3_v)
            else:
                starting_height_K.append(maxima_hoogtes[0])
                coefficienten_1_h_K_lijst.append(cor1_h)
                coefficienten_2_h_K_lijst.append(cor2_h)
                # coefficienten_3_lijst.append(cor3_h)

                coefficienten_1_v_K_lijst.append(cor1_v)
                coefficienten_2_v_K_lijst.append(cor2_v)
                # coefficienten_3_v_lijst.append(cor3_v)

            plt.figure(1, figsize=(15, 15))
            plt.suptitle('Position and speed graphs, of different heights from both marbles (Small metal, medium blue), combined (messy)')
            plt.subplot(311)
            plt.title('Height over time, all measurements')
            plt.plot(frame_lijst, hoogte_lijst)
            plt.xlabel('Time (frames)')
            plt.ylabel('Height (px)')
          
            plt.subplot(312)
            plt.title('Speed over time, all measurements')
            plt.plot(frame_lijst, snelheden)
            plt.xlabel('Time (frames)')
            plt.ylabel('Speed (px/frame)')
            plt.xlim(0, 400)
            plt.ylim(-20, 20)
            plt.savefig('HEIGHTDIFF_POS_AND_SPEED.png', bbox_inches='tight')

            test_max_snelheid.append(max(snelheden))
            # print(cor1, cor2, cor3)
            test_minimale_hoogte.append(min(hoogte_lijst))
            
            print(impact_frames)
            print(impact_snelheden)
            print(f'File: {b}-{a}')

# print(impact_snelheden)

papier_lijst = [1, 2, 3, 4]

plt.figure(2, figsize=(15, 10))
plt.suptitle('CoR against starting height, Medium (blue) marble')
plt.subplot(321)
plt.title('CoR calculated with height ratio (h_after_bounce / h_initial)')
plt.plot(coefficienten_1_h_M_lijst, starting_height_M, 'o', label='h1/h0 (first bounce)')
# plt.plot(papier_lijst, coefficienten_2_h_M_lijst, 'o', label='h2/h1 (second bounce)')
# plt.plot(papier_lijst, coefficienten_3_h_M_lijst, label='h3/h2 (third bounce)')

plt.xlabel('Restitutioncoefficient (ratio)')
plt.ylabel('Starting height (px)')
plt.legend()


plt.subplot(322)
plt.title('CoR calculated with speed ratio (v_after_impact / v_before_impact)')
plt.plot(coefficienten_1_v_M_lijst, starting_height_M, 'o', label='v1/v0 (first impact)')
# plt.plot(papier_lijst, coefficienten_2_v_lijst, 'o', label='v2/v1 (second impact)')
# plt.plot(papier_lijst, coefficienten_3_v_lijst, label='v3/v2 (third impact)')
# plt.ylim(0, 0.6)
plt.xlabel('Restitutioncoefficient (ratio)')
plt.ylabel('Starting height (px)')
plt.legend()
plt.savefig('HEIGHTDIFF_MEDIUM_BLUE_MARBLE_COR.png')


plt.figure(3, figsize=(20, 10))
plt.suptitle('CoR against starting height, Small (metal) marble')
plt.subplot(331)
plt.title('CoR calculated with height ratio (h_after_bounce / h_initial)')
plt.plot(coefficienten_1_h_K_lijst, starting_height_M, 'o', label='h1/h0 (first bounce)')
# plt.plot(papier_lijst, coefficienten_2_h_M_lijst, 'o', label='h2/h1 (second bounce)')
# plt.plot(papier_lijst, coefficienten_3_h_M_lijst, label='h3/h2 (third bounce)')
plt.xlabel('Restitutioncoefficient (ratio)')
plt.ylabel('Starting height (px)')
plt.legend()


plt.subplot(332)
plt.title('CoR calculated with speed ratio (v_after_impact / v_before_impact)')
plt.plot(coefficienten_1_v_K_lijst, starting_height_M, 'o', label='v1/v0 (first impact)')
# plt.plot(papier_lijst, coefficienten_2_v_lijst, 'o', label='v2/v1 (second impact)')
# plt.plot(papier_lijst, coefficienten_3_v_lijst, label='v3/v2 (third impact)')
# plt.ylim(0, 0.6)
plt.xlabel('Restitutioncoefficient (ratio)')
plt.ylabel('Starting height (px)')
plt.legend()
plt.savefig('HEIGHTDIFF_SMALL_METAL_MARBLE_COR.png')
plt.show()


print(min(test_minimale_hoogte))
print(max(test_max_snelheid))