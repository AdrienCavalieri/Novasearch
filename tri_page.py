import os
from bs4 import BeautifulSoup
from progress.bar import Bar
from distance_page import dist_hamming


class tri_page():

    def __init__(self, dirPath):
        dir = os.listdir(dirPath)
        i = 0
        page = []
        bar = Bar('Chargement des pages', max=len(dir), suffix='%(percent).1f%% - %(eta)ds')
        for file in dir:
            try:
                filePath = dirPath + '/' + file
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
        self.page = page


    def page_similaire(self):
        list_lier = dict()
        bar = Bar('Comparaison des pages: ', max=len(self.page), suffix='%(percent).1f%% - %(eta)ds')
        for i in range(len(self.page)):
            if self.page[i][1]:
                j = i + 1
                list_lier[self.page[i][2]] = list()  # on met les liens valides dans le dictionnaire
                for k in range(j, len(self.page)):
                    if (self.page[k][1]):
                        # print(i, k)
                        if (dist_hamming(self.page[i][2], self.page[k][2], 10) < 10 and dist_hamming(self.page[i][0], self.page[k][0], 100) < 100):  # si la distance entre 2 pages est similaire (10=5k pages, 100=3k pages 1000=700 pages)
                            self.page[k] = (self.page[k][0], False, self.page[k][2])  # on la retire des comparaisons futur
                            list_lier[self.page[i][2]].append(self.page[k][2])  # on l'ajoute en valeur de la clé

            bar.next()
        bar.finish()
        print(len(list_lier.keys()))
        return list_lier.keys()  # renvoie que les liens valide, c'est-à-dire les clés