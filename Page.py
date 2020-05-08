class Page:
    def __init__(self, nom, mots, liens):
        self._nom = nom
        self._mots = mots
        self._liens = liens
        self.setScoreMots()

    def get_nom(self):
        return self._nom

    def get_mots(self):
        return self._mots

    def get_liens(self):
        return self._liens

    def setScoreMots(self):
        newMots = dict()
        for mot in self._mots:
            if mot not in newMots:
                newMots[mot] = 1
            else:
                newMots[mot] = newMots[mot] + 1
        self._mots = newMots

    def getScoreMot(self, mot):
        if mot not in self._mots:
            return 0
        else:
            return self._mots[mot]

    def getTotalScore(self):
        total = 0
        for mot in self._mots:
            total = total + self._mots[mot]
        return total

    def __str__(self):
        return "La page " + self._nom + " contiens les " + str(
            len(self._mots)) + " mots suivants:\n" + str(self._mots) + "\n et les " + str(
            len(self._liens)) + " liens suivants:\n" + str(self._liens)