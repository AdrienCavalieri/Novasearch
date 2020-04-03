import os
from bs4 import BeautifulSoup
from progress.bar import Bar
from distance_page import dist_hamming

dirpath = "./same_page"
dir = os.listdir(dirpath)
i = 0
page = []
bar = Bar('Chargement des pages dans l\'index', max=len(dir), suffix='%(percent).1f%% - %(eta)ds')
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


def page_similaire(min, max):
    bar = Bar('Thread ', max=max - min, suffix='%(percent).1f%% - %(eta)ds')
    for i in range(min, max):
        if page[i][1]:
            j = i + 1
            # page_valide.append(page[i][2])
            list_lier[page[i][2]] = list()
            for k in range(j, len(page)):
                if (page[k][1]):
                    # print(i, k)
                    if (dist_hamming(page[i][0], page[k][0], 10) < 10):
                        page[k] = (page[k][0], False, page[k][2])
                        list_lier[page[i][2]].append(page[k][2])

        bar.next()
    bar.finish()


page_similaire(0, len(page))
# page_valide = list_lier.keys()
# print(page_valide)
print(list_lier)
print(len(list_lier))
