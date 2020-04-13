from http.server import HTTPServer, BaseHTTPRequestHandler

class Server(BaseHTTPRequestHandler):

    print("Server ready to use...")

    def do_GET(self): #
        if self.path == '/':
            self.path = '/index.html' # Page d'accueil (A).
        if self.path == '/search':
            self.path = '/search.html' # Page de recherche (B).
        try:
            file_to_open = open(self.path[1:]).read() #
            self.send_response(200) # "OK".
        except:
            file_to_open = "File not found"
            self.send_response(404) # "Page introuvable".
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

novasearchServer = HTTPServer(('localhost', 8080), Server) # Serveur tournant sur le port 8080.
novasearchServer.serve_forever() # Boucle infinie.
