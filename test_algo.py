import os
from distance_page import levenshtein

print('Algo avec niche et chien')
var = levenshtein("niche","chien")             # test algo avec mots niche et chien
print('La distance est de :' + str(var))

page = []       #stock des noms des pages web de l'archive
for root, directories, files in os.walk("./pages_web"):    #charge les fichiers de l'archive
    for file in files:
        page.append(file)   # on ajoute à la liste

print('Algo avec 2 pages de l\'archive')
page1 = page[0]
page2 = page[5000]
var = levenshtein(page1,page2)
print('La distance est de : ' + str(var))
print('La page 1 est : ' + page1)
print('La page 2 est : ' + page2)
