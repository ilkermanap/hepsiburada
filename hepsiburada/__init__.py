from websayfa import UzakSayfa

URL="https://www.hepsiburada.com"

class Marka(UzakSayfa):
    def __init__(self, marka):
        UzakSayfa.__init__(self, URL+"/"+marka)
        self.sayfa_sayisi = 0

    def sayfalar(self):
        pagination = self.soup.select_one(".pagination")
        li = pagination.find_all("li")
        self.sayfa_sayisi = int(li[-1].text)
