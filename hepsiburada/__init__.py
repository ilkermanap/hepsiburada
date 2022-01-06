
from websayfa import UzakSayfa

URL="https://www.hepsiburada.com"

class Marka(UzakSayfa):
    def __init__(self, marka):
        self.marka = marka
        UzakSayfa.__init__(self, URL+"/"+marka)
        self.sayfa_sayisi = 0
        self.urun_listesi = {}
        pagination = self.soup.select_one(".pagination")
        li = pagination.find_all("li")
        self.sayfa_sayisi = int(li[-1].text)

    def tum_urunler(self):
        for sayfa in range(1, self.sayfa_sayisi+1):
            self.urunler(sayfano=sayfa)
        return self.urun_listesi

    def urunler(self, sayfano=1):
        content = None
        if sayfano == 1:
            content = self.soup
        else:
            temp = UzakSayfa(f"{self.url}?sayfa={sayfano}")
            content = temp.soup

        product_list = content.find("ul", class_="product-list").find_all("li")

        for product in product_list:
            a = product.find("a")
            temp = Urun(a.attrs)
            try:
                temp.rating = int(a.find("span", class_="ratings active").attrs["style"].split()[1].split("%")[0])
            except AttributeError:
                temp.rating = None
            temp.title = product.find(class_ = "product-title").attrs["title"]

            fp = float(product.find("div", class_="first-price-area").find("span").text.replace(".","").replace(",",".").split()[0])
            temp.first_price = fp

            try:
                temp.second_price = float(product.find("div", class_="second-price-area").find("span").text.replace(".","").replace(",",".").split()[0])
            except AttributeError:
                pass
            self.urun_listesi[temp.sku] = temp

class Urun:
    def __init__(self, kwargs):
        self.url = kwargs.get("href")
        self.sku = kwargs.get("data-sku")
        self.productid = kwargs.get("data-productid")
        self.listing_id = kwargs.get("data-listing_id")
        self.shipping_type = kwargs.get("data-shipping_type")
        self.isinstock = kwargs.get("data-isinstock")
        self.ispreorder = kwargs.get("data-ispreorder")
        self.isproductlive =  kwargs.get("data-isproductlive")
        self.price = kwargs.get("data-price")
        self.rating = None
        self.title = None
        self.first_price = None
        self.second_price = None

    def yorumlar(self):
        yorum = UzakSayfa(f"{URL}{self.url}-yorumlari")
        print(yorum.icerik)
        print(yorum.url)