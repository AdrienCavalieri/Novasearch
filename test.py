import os
from bs4 import BeautifulSoup

mydir = "./pages_web"
l = os.listdir(mydir)
print(len(l))
"""for el in l:
    print(el)
"""
path="./pages_web/lipn.fr_rdos_"
myfile = open(path)
contenu = myfile.read()
soup = BeautifulSoup(contenu,"html.parser")
clean_text = soup.get_text()
text = ' '.join(clean_text.split())
listwords = text.split(' ')
href = soup.find_all('a', href=True)

link = list()
for a in href:
    link.append(a['href'])
print(path)
print(link)
print(listwords)