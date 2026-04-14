Bij dit experiment is er gekeken naar de invloed van de luchtdruk op de restitutie coefficient van een knikker die op een stapel papier valt.

De vallende knikker is gefilmd en vervolgens getracked. 
Hieruit kwam een tabel met de hoogte van de knikker bij elk frame. Deze resultaten zijn te zien in de CSV bestanden.
Deze hebben als naam: datum van de meting_results_'aantal vellen papier die als ondergrond zijn gebruikt'_'luchtdruk met eenheid'.csv

In het bestand genaamd 'drukVScor.ipynb' wordt er een grafiek gemaakt waarbij de restitutie coëfficiënt wordt uitgezet tegen de luchtdruk. 
Hiervoor worden de meetingen gebruikt met 100 vellen papier. 
Deze dingen worden er uitgevoerd in het bestand:
1. Er wordt een grafiekje gemaakt van elke meting, waarbij de hoogte van de knikker wordt uitgezet tegen de frames.
2. Er wordt een lijst gemaakt met de maximale hoogtes die de knikker bereikt. Hieruit wordt de restitutie coëfficiënt berekend.
3. De fout op het restitutie coëfficiënt wordt berekend.
4. Er wordt daarna van alle verschillende luchtdrukken met de bijbehoorende restitutie coëfficiënten een eerste grafiek gemaakt.
5. Vervolgens wordt er een periode tussen 2 stuiters geisoleerd van één meting. Hier wordt een parabool op gefit. De wortel van de reduced chi-sqaured is namelijk gelijk aan de fout die de trackingssoftware heeft. Dit wordt dus gebruikt om de fout op de restitutie coëfficiënt te berekenen (deze waarde wordt al eerder in de code gebruikt).
6. Tot slot wordt er nog een grafiek gemaakt waarbij de restitutie coëfficiënt wordt uitgezet tegen de luchtdruk, maar nu bevat de grafiek ook de bijbehoorende foutvlaggen. Door de lekende vacuumkamer zit er een grote fout op de luchtdruk. Zowel voor als na het uitvoeren van een meting is de luchtdruk afgelezen. Dit had vaak een verschil van 10mbar. Maar er zit ook nog een fout van het aflezen bij van ±10mbar.
   
NOTE:  edit the tracking of the 95/100 & 190&200 mbar files; error suspected due to outlier.


In het bestand genaamd 'amount_of_paperVScor_at_30mbar.ipynb' wordt er een grafiek gemaakt waarbij de restitutie coëfficiënt wordt uitgezet tegen de aantal vellen papier met een standaard luchtdruk van 30mbar ± 10. 
Hiervoor worden de meetingen gebruikt een druk van 30mbar.
Deze dingen worden er uitgevoerd in het bestand:
1. Er wordt een grafiekje gemaakt van elke meting, waarbij de hoogte van de knikker wordt uitgezet tegen de frames.
2. Er wordt een lijst gemaakt met de maximale hoogtes die de knikker bereikt. Hieruit wordt de restitutie coëfficiënt berekend.
3. De fout op het restitutie coëfficiënt wordt berekend. (Hiervoor wordt stap 5 gebruikt van het bestand: 'drukVScor.ipynb'.)
4. Er wordt daarna van alle verschillende luchtdrukken met de bijbehoorende restitutie coëfficiënten een eerste grafiek gemaakt.
5. Tot slot wordt er nog een grafiek gemaakt waarbij de restitutie coëfficiënt wordt uitgezet tegen de aantal vellen papier, maar nu bevat de grafiek ook de bijbehoorende foutvlaggen. Voor de fout op het aantal lagen papier is er gekozen voor 2 vellen. 
