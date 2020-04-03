import os
from bs4 import BeautifulSoup
from distance_page import dist_hamming


dirpath = "../pages_web"
dir = os.listdir(dirpath)
i=0
page = []
for file in dir:
    try:
        filePath = dirpath+ '/' + file
        lien = file
        file = open(filePath, 'r', encoding="utf8")
        soup = BeautifulSoup(file, "html.parser")  # lib pour parser une page html
        text = soup.get_text()  # recupere uniquement le texte
        text = ''.join(text.split()) # recupere les mots du texte tout attaché

        page.append((text,True,lien))
    except:
        i = i + 1  # nb de fichiers ignoré

list1 = []


for i in range(len(page)):
    if page[i][1]:
        j = i+1
        list1.append(page[i][2])
        for k in range(j,len(page)):
            print(i,k)
            if(page[k][1]):
                if(dist_hamming(page[i][0],page[k][0])==0):
                    page[k] = (page[k][0],False)

print(list1)
print(len(list1))

