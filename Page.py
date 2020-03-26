class Page:
    def __init__(self, nom, mots, liens):
        self._nom = nom
        self._mots = mots
        self._liens = liens

    def get_nom(self):
        return self._nom

    def get_mots(self):
        return self._mots

    def get_liens(self):
        return self._liens

    def __str__(self):
        return "La page " + self._nom + " contiens les " + str(
            len(self._mots)) + " mots suivants:\n" + str(self._mots) + "\n et les " + str(
            len(self._liens)) + " liens suivants:\n" + str(self._liens)
