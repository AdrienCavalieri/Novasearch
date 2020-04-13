import os
from bs4 import BeautifulSoup
from progress.bar import Bar
from distance_page import dist_hamming
import shutil

dirpath = "./same_page"
dir = os.listdir(dirpath)
i = 0
page = []
bar = Bar('Chargement des pages', max=len(dir), suffix='%(percent).1f%% - %(eta)ds')
for file in dir:
    try:
        filePath = dirpath + '/' + file
        lien = file
        file = open(filePath, 'r', encoding="utf8")
        soup = BeautifulSoup(file, "html.parser")  # lib pour parser une page html
        text = soup.get_text()  # recupere uniquement le texte
        text = ''.join(text.split())  # recupere les mots du texte tout attaché

        page.append((text, True, lien))
    except:
        i = i + 1  # nb de fichiers ignoré
    bar.next()
bar.finish()
page_valide = []
list_lier = dict()


def page_similaire():
    bar = Bar('Comparaison des pages: ', max=len(page), suffix='%(percent).1f%% - %(eta)ds')
    for i in range(len(page)):
        if page[i][1]:
            j = i + 1
            # page_valide.append(page[i][2])
            list_lier[page[i][2]] = list()      # on met les liens valides dans le dictionnaire
            for k in range(j, len(page)):
                if (page[k][1]):
                    # print(i, k)
                    if (dist_hamming(page[i][0], page[k][0], 10) < 10):     #si la distance entre 2 pages est similaire
                        page[k] = (page[k][0], False, page[k][2])           # on la retire des comparaisons futur
                        list_lier[page[i][2]].append(page[k][2])            # on l'ajoute en valeur de la clé

        bar.next()
    return list_lier
    bar.finish()


"""
On met uniquement les clés dans un nouveau dossier. Cela constituera l'index.
"""
index = page_similaire().keys()
dir_dest = "./index_pages"
os.makedirs(dir_dest, exist_ok=True)
bar = Bar('Création de l\'index: ', max=len(page), suffix='%(percent).1f%% - %(eta)ds')
for file in index:
    filePath = dirpath + "/" + file
    shutil.copy(filePath, dir_dest+ "/" +file)
    bar.next()
bar.finish()

#page_valide = list_lier.keys()
#print(page_valide)
#print(list_lier)
#print(len(list_lier))
