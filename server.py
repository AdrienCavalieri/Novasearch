from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
from Index_inverse import Index_inverse

index = Index_inverse("./pages_web")
index.printIndex()


class Server(BaseHTTPRequestHandler):
    def do_GET(self): # Gère les requêtes GET.
        if self.path.endswith('/'):
            self.path = '/index.html' # Page d'accueil (A).
        try:
            content = open('html/' + self.path[1:]).read()
            self.send_response(200) # "OK".
        except:
            content = open('html/404.html').read()
            self.send_response(404) # "Page introuvable".
        self.end_headers()
        self.wfile.write(bytes(content, 'utf-8'))

    def do_POST(self): # Gère les requêtes POST.
        if self.path == '/search':
            self.path = '/search.html'
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                search = fields.get('reverse_index_search')[0]

                print(search) # Debug : affiche la recherche.
                results = list(index.recherche(search).keys())
                s = ""
                for e in results:
                    s += "<li class=\"list-group-item\"><a href=\"https://" + e.replace("_","/") + "\">" + e.replace("_","/") + "</a></li>"
                print(s)

                try:
                    content = open('html/' + self.path[1:]).read().replace("{0}", s)
                    self.send_response(200) # "OK"
                except:
                    content = open('html/404.html').read()
                    self.send_response(404) # "Page introuvable".
                self.end_headers()
                self.wfile.write(bytes(content, 'utf-8'))

def main():
    PORT_NUMBER = 8080
    ADDRESS = 'localhost'
    novasearchServer = HTTPServer((ADDRESS, PORT_NUMBER), Server) # Serveur tournant sur le port 8080.
    novasearchServer.serve_forever() # Boucle pour attendre indéfiniment les requêtes HTTP.

if __name__ == '__main__':
    main()
