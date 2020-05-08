import math
import os
import string
from bs4 import BeautifulSoup
from Page import Page
from progress.bar import Bar
from tri_page import tri_page
from distance_page import *
import time


class Index_inverse():

    def __init__(self, dirPath):
        tpage = tri_page(dirPath)
        dir = tpage.page_similaire()    # on enleve les pages similaires de l'index
        pages = list()
        i = 0
        j = 0
        bar = Bar('Chargement des pages dans l\'index', max=len(dir), suffix='%(percent).1f%% - %(eta)ds')
        for fileName in dir:
            j = j + 1
            filePath = dirPath + "/" + fileName
            try:
                file = open(filePath, 'r', encoding="utf8")  # lis le fichier avec encodage utf8
                content = file.read()
                soup = BeautifulSoup(content, "html.parser")  # lib pour parser une page html
                text = soup.get_text()  # recupere uniquement le texte

                mots = text.split()
                mots = [mot.lower() for mot in mots]
                table = str.maketrans('', '', string.punctuation)
                mots = [mot.translate(table) for mot in mots]

                href = soup.find_all('a', href=True)  # recupere les balises de lien
                liens = list()
                for a in href:
                    liens.append(a['href'])  # recupere les liens contenus dans les balises
                pages.append(Page(fileName, mots, liens))  # créer un objet page
                file.close()
            except:
                i = i + 1  # nb de fichiers ignoré
            bar.next()
        bar.finish()
        self._urlsLoad = len(pages)
        self._pages = pages

        taillesMotsPages = [len(page.get_mots()) for page in self._pages]
        if len(taillesMotsPages) == 0:
            self._avgNbMots = 0
        else:
            self._avgNbMots = (float(sum(taillesMotsPages))) / len(taillesMotsPages)
        self._indexInverse = dict()
        self.loadIndex()
        self._dict_mots = self.dict_mots()

    def loadIndex(self):  # on rempli l'index inversé par rapport au page chargée
        i = 0
        bar = Bar('Chargement des mots de chaque page dans l\'index', max=len(self._pages),
                  suffix='%(percent).1f%% - %(eta)ds')
        for page in self._pages:
            i = i + 1
            for mot in page.get_mots():
                if mot in self._indexInverse:
                    if page.get_nom() not in self._indexInverse[mot]:
                        self._indexInverse[mot].append(page.get_nom())
                else:
                    self._indexInverse[mot] = list()
                    self._indexInverse[mot].append(page.get_nom())
            bar.next()
        bar.finish()

    def printIndex(self):
        if os.path.exists("log.txt"):
            os.remove("log.txt")
        f = open("log.txt", "a+", encoding="utf8")

        for name, liste in self._indexInverse.items():
            try:
                f.write(name + ":" + str(liste) + "\r\n")
                # f.write(name + ":\r\n")
            except:
                pass
        f.close()

    def tf(self, mot, namePage):
        for page in self._pages:
            if page.get_nom() == namePage:
                #print(page)
                try:
                    return page.getScoreMot(mot) / page.getTotalScore()
                except:
                    return 0
        return 0

    def idf(self, mot):
        if mot not in self._indexInverse:
            return 0
        else:
            # print(self._indexInverse[mot])
            return math.log(len(self._pages) / len(self._indexInverse[mot]))

    def tf_idf(self, mot, namePage):
        return self.tf(mot, namePage) * self.idf(mot)

    def bm25(self, listMots, namePage):
        total = 0
        k = 2.0
        b = 0.75
        for mot in listMots:
            idf = self.idf(mot)
            dividende = self.tf_idf(mot, namePage) * (k + 1)
            diviseur = self.tf_idf(mot, namePage) + k * (1 - b + b * self._urlsLoad / self._avgNbMots)
            score = idf * (dividende / diviseur)
            #print("pour " + mot + ": " + str(idf) + " * (" + str(dividende) + " / " + str(diviseur) + ") = "+str(score))
            total += score
        return total

    def recherche(self,chaine):
        mots = chaine.split()
        mots = [mot.lower() for mot in mots]
        table = str.maketrans('', '', string.punctuation)
        mots = [mot.translate(table) for mot in mots]
        mots = self.motsimilaire(mots)
        print('lancement de la recherche')


        listScore = dict()
        bar = Bar('Chargement des score de page', max=len(self._pages), suffix='%(percent).1f%% - %(eta)ds')
        for page in self._pages:
            listScore[page.get_nom()] = self.bm25(mots,page.get_nom())
            bar.next()
        bar.finish()
        listScore = {k: v for k, v in sorted(listScore.items(), key=lambda item: item[1], reverse=True)[:10]}
        print('fin de la recherche')
        return listScore

    # on découpe la liste de mots en plusieurs clé valeurs pour faire des recherches plus courtes.
    def dict_mots(self):
        listMots = self._indexInverse.keys()
        dictMots = {'0':[], '1':[], '2':[], '3':[], '4':[], '5':[], '6':[], '7':[], '8':[], '9':[], 'a':[], 'b':[], 'c':[], 'd':[], 'e':[], 'f':[], 'g':[], 'h':[], 'i':[], 'j':[], 'k':[], 'l':[], 'm':[], 'n':[], 'o':[], 'p':[], 'q':[], 'r':[], 's':[], 't':[], 'u':[], 'v':[], 'w':[], 'x':[], 'y':[], 'z':[]}
        for mot in listMots:
            if(mot ==''):
                continue
            if (mot[0] in dictMots):
                dictMots[mot[0]].append(mot)
        return dictMots


    def motsimilaire(self,mots):
        tmp = []
        for mot in mots:
            tmp.append(mot)
        listMots = self._dict_mots
        bar = Bar('Recherche mots similaires', max=len(tmp), suffix='%(percent).1f%% - %(eta)ds')
        for mot in tmp:             # pour les mots rechercher
            if(mot ==''):           # evite les caractères spéciaux
                continue
            if(mot in listMots[mot[0]]):    # si le mot est dans l'index on ne cherche pas d'autres mots similaire
                continue
            for list in listMots[mot[0]]:   # les mots de la liste
                if(list in tmp):    # si le mot est deja dans la liste on le saute
                    pass
                elif (len(mot) < 3):                                                        # mot entre 0 et 2 lettres
                    if ((len(list) >= len(mot) - 1) and (len(list) <= len(mot) + 1)):       # entre n-1 n+1
                        if(dist_hamming(mot,list,len(mot))==0):                             # hamming(+ rapide) sans erreur
                            mots.append(list)
                elif(len(mot)<6):                                                           # mot entre 3 et 5 lettres
                    if ((len(list) >= len(mot) - 1) and (len(list) <= len(mot) + 1)):
                        if(levenshtein(mot,list,)<2):                                       # levenshtein 1 erreur max
                            mots.append(list)
                else:                                                                       # > 6 lettres
                    if( (len(list)>=len(mot)-1) and (len(list)<=len(mot)+1) ):
                        if(levenshtein(mot,list)<3):                                        # levenshtein 2 erreurs max
                            mots.append(list)
            bar.next()
        bar.finish()
        #print(mots)
        return mots
