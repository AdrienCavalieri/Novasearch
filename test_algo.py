import os
import time
from bs4 import BeautifulSoup
from distance_page import *

"""
print('Algo avec niche et chien')
var = levenshtein("niche","chien")             # test algo avec mots niche et chien
print('La distance est de :' + str(var))
"""

dirpath = "./same_page"
dir = os.listdir(dirpath)
i = 0
page = []
for file in dir:
    try:
        filePath = dirpath + '/' + file
        file = open(filePath, 'r', encoding="utf8")
        soup = BeautifulSoup(file, "html.parser")  # lib pour parser une page html
        text = soup.get_text()  # recupere uniquement le texte
        text = ''.join(text.split())  # recupere les mots du texte tout attaché
        page.append(text)
    except:
        i = i + 1  # nb de fichiers ignoré

print('Algo avec 2 pages de l\'archive')
page1 = page[0]
page2 = page[1]
print('Test hamming')
start = time.time()
var = dist_hamming(page1, page2,1000)
end = time.time()
print(end - start)
print('La distance est de : ' + str(var))
"""
print('Test levenshtein')
start = time.time()
var = levenshtein(page1,page2)
end = time.time()
print(end - start)
print('La distance est de : ' + str(var))
print('La page 1 est : ' + page1)
print('La page 2 est : ' + page2)
"""
