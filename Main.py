from Index_inverse import Index_inverse
from tri_page import tri_page

index = Index_inverse("../algo/same_page")
#index = Index_inverse("../pages_web")
#index.printIndex()
#print(index.tf("université","cas.univ-paris13.fr_cas_login_service=https%3A%2F%2Fwww.lipn.univ-paris13.fr%2F%7Ebreuvart%2FProjets%2F"))
#print(index.idf("université"))
#print(index.tf_idf("université",))
#print(index.bm25(["salut","à","tous"],"cas.univ-paris13.fr_cas_login_service=https%3A%2F%2Fwww.lipn.univ-paris13.fr%2F%7Ebreuvart%2FProjets%2F"))
print(index.recherche("Licence Université Paris13"))
#print(len(index.getmots()))
#print(index.motsimilaire("Université"))

