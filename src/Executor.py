class Discoverer:
    def __init__(self):
        self.works = []
        self.data = ()
    
    def addWork(self, w):
        self.works.append(w)
    
    def addWorks(self, *ws):
        for w in ws:
            self.works.append(w)
    
    def doWorks(self):
        for work in self.works:
            work(self.data)

if __name__ == "__main__":
    import Analysis_wordcloud, Analysis_sentence, Analysis_character
    d = Discoverer()
    d.addWork(Analysis_wordcloud.MainWork_cn)
    d.addWorks( Analysis_sentence.MainWork_cn, 
                Analysis_character.MainWork_cn)
    d.doWorks()