import os
from bs4 import BeautifulSoup
from Page import Page


class Index_inverse():

    def __init__(self, dirPath):
        dir = os.listdir(dirPath) #liste tous les fichiers d'un répertoire
        pages = list()
        i = 0
        j = 0
        for fileName in dir:
            j = j + 1
            filePath = dirPath + "/" + fileName
            print(str(j) + "/" + str(len(dir)))
            try:
                file = open(filePath, 'r', encoding="utf8") # lis le fichier avec encodage utf8
                content = file.read()
                soup = BeautifulSoup(content, "html.parser") # lib pour parser une page html
                text = soup.get_text() # recupere uniquement le texte
                clean_text = ' '.join(text.split()) # supprime les espaces superflu
                mots = clean_text.split() # le texte devient une liste de mots
                href = soup.find_all('a', href=True) # recupere les balises de lien
                liens = list()
                for a in href:
                    liens.append(a['href']) # recupere les liens contenus dans les balises
                pages.append(Page(fileName, mots, liens)) #créer un objet page
                file.close()
            except:
                i = i + 1 # nb de fichiers ignoré
        self._urlsLoad = len(pages)
        self._pages = pages
        self._indexInverse = dict()
        self.loadIndex()

    def loadIndex(self): # on rempli l'index inversé par rapport au page chargée
        i = 1
        for page in self._pages:
            i=i+1
            print(str(i) + "/" + str(len(self._pages)))
            for mot in page.get_mots():
                if mot in self._indexInverse:
                    if page.get_nom() not in self._indexInverse[mot]:
                        self._indexInverse[mot].append(page.get_nom())
                else:
                    self._indexInverse[mot] = list()
                    self._indexInverse[mot].append(page.get_nom())

    def printIndex(self):
        for name, liste in self._indexInverse.items():
            print(name + ":" + str(liste))
