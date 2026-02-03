class File:
    def __init__(self):
        self.f = []

    def enfiler(self,item):
        self.f.append(item)

    def defiler(self):
        if len(self.f) !=0:
            item=self.f[0]
            self.f=self.f[1:]
            return item
        
    def est_vide(self):
        return len(self.f)==0

    def taille(self):
        return len(self.f)
        
    def voir_tete(self):
        return self.f[0]
