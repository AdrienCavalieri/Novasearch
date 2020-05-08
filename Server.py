from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
from Index_inverse import Index_inverse

index = Index_inverse("../pages_web") # On déclare l'index rempli en tant que variable globale.
index.printIndex() # Génère un fichier log.

class Server(BaseHTTPRequestHandler):
    def do_GET(self): # Gère les requêtes GET.
        if self.path.endswith('/'): # S'il on accède à la page d'accueil (A) par requête GET ...
            self.path = '/index.html'
        try:
            content = open('html/' + self.path[1:]).read() # On essaye de lire dans le fichier HTML.
            self.send_response(200) # On envoit le code "OK".
        except:
            content = open('html/404.html').read() # On lit la page d'erreur sinon.
            self.send_response(404) # On envoie le code "Page introuvable".
        self.end_headers()
        self.wfile.write(bytes(content, 'utf-8')) # On affiche la page HTML.

    def do_POST(self): # Gère les requêtes POST.
        if self.path.endswith('/search'): # S'il on accède à la page de recherche (B) par la méthode POST ...
            self.path = '/search.html'
            # Récupération du content-type et création d'un dictionnaire contenant les paramètres du content-type.
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            # Récupération de la clé permettant de séparer les attributs du formulaire et conversion de la clé en octets.
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            # Ajout de la taille du contenu au dictionnaire de paramètres.
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype == 'multipart/form-data': # Si le content-type est de type "multipart/form-data" ...
                # Récupération des champs du formulaire.
                fields = cgi.parse_multipart(self.rfile, pdict)
                # Récupère la recherche effectuée grâce à l'attribut "name" de la balise <input> présente dans la page HTML
                search = fields.get('reverse_index_search')[0]
                print("Recherche : \"" + search + "\"") # Affiche la recherche effectuée dans le terminal.
                # Récupère les clés (les liens) du dictionnaire contenant les résultats et les stocke sous forme de liste.
                results = list(index.recherche(search).keys())
                link_list_html = "" # Chaîne de caractère de stockage.
                for e in results: # Pour chaque lien de la liste ...
                    # 1. Ajoute le lien dans une balise HTML <a>, elle-même contenue dans une balise d'élément de liste <li>.
                    # 2. Ajoute des "http://" devant les liens  et remplace les _ des liens par des / afin de reformer un lien valide.
                    link_list_html += "<li class=\"list-group-item\"><a href=\"http://" + e.replace("_","/") + "\">" + e.replace("_","/") + "</a></li>"
        try:
            # On essaye de lire dans le fichier HTML.
            # Note : si on essaye d'accéder à page de recherche (B) par la méthode POST,
            # on remplace le marqueur de place "{0}", présent dans "search.html", par la liste des liens généré.
            content = open('html/' + self.path[1:]).read().replace("{0}", link_list_html)
            self.send_response(200) # On envoit le code "OK".
        except:
            content = open('html/404.html').read() # On lit la page d'erreur sinon.
            self.send_response(404) # On envoie le code "Page introuvable".
        self.end_headers()
        self.wfile.write(bytes(content, 'utf-8')) # On affiche la page HTML.

def main():
    PORT_NUMBER = 8080
    ADDRESS = 'localhost'
    novasearchServer = HTTPServer((ADDRESS, PORT_NUMBER), Server) # Serveur tournant sur le port 8080 en local.
    print("Serveur prêt")
    novasearchServer.serve_forever() # Boucle pour attendre indéfiniment les requêtes HTTP.

if __name__ == '__main__':
    main()
