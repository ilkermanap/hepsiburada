from websayfa import UzakSayfa
import sys

URL = "https://www.hepsiburada.com"

import traceback as tb

class Marka(UzakSayfa):
    def __init__(self, marka):
        self.marka = marka
        UzakSayfa.__init__(self, URL+"/"+marka)
        self.sayfa_sayisi = 0
        self.urun_listesi = {}
        pagination = self.soup.select_one(".pagination")
        li = pagination.find_all("li")
        self.sayfa_sayisi = int(li[-1].text)

    def csv(self):
        fhandle = open(f"{self.marka}.csv", "w", encoding="utf-8")
        i=1
        for urun in self.urun_listesi.values():
            urun.csv(fhandle)
        fhandle.close()

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
            try:
                temp = Urun(a.attrs)
            except:
                tb.print_exc()
            try:
                temp.rating = int(a.find("span", class_="ratings active").attrs["style"].split()[1].split("%")[0])
            except AttributeError:
                temp.rating = None
            temp.title = product.find(class_="product-title").attrs["title"]

            fp = float(product.find("div", class_="first-price-area").find("span").text.replace(".", "").replace(",",".").split()[0])
            temp.first_price = fp

            try:
                f = product.find("div", class_="second-price-area").find("span").text.replace(".","").replace(",",".").split()[0]
                temp.second_price = float(f)
            except AttributeError:
                pass

            resimler = product.find_all("img", class_="product-image")
            for resim in resimler:
                attribstr = resim.attrs["data-bind"]
                parts = attribstr.split("'")
                for part in parts:
                    if part.find("hepsiburada") > 0:
                        temp.resim_ekle(part.split()[0])
            self.urun_listesi[temp.sku] = temp

class Urun:
    def __init__(self, kwargs):
        self.url = kwargs.get("href")
        self.sku = kwargs.get("data-sku")
        print(self.sku, kwargs.keys())

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
        self.soup = None
        self.yorum = []
        self.resimler = []
        self.yorumlar()


    def csv(self, fhandle):
        head = f"{self.sku}|{self.price}|{self.title}|{self.resimler[0]}|"
        for yorum in self.yorum:
            fhandle.write(head+yorum.csv())

    def resim_ekle(self, yeni_url):
        if yeni_url not in self.resimler:
            self.resimler.append(yeni_url)

    def yorumlar(self):
        yorum = UzakSayfa(f"{URL}{self.url}-yorumlari")
        self.soup = yorum.soup
        pagination = yorum.soup.select_one(".paginationBarHolder")
        try:
            li = pagination.find_all("li")
            sayfa_sayisi = int(li[-1].text)
        except:
            sayfa_sayisi=1
        for sayfa in range(1,sayfa_sayisi+1):
            self.yorum_sayfasi(sayfa)

    def yorum_sayfasi(self, sayfano):
        try:
            soup = None
            if sayfano == 1:
                soup = self.soup
            else:
                temp = UzakSayfa(f"{URL}{self.url}-yorumlari?sayfa={sayfano}")
                soup = temp.soup
            yorum_divs = soup.select_one(".paginationContentHolder")
            yorum_listesi = yorum_divs.find_all("div", recursive = False)
            for yorumcart in yorum_listesi:
                #her bir yorum cart, bir yorumun tum bilgilerini icerir
                self.yorum.append(Yorum(yorumcart))
        except:
            #hic yorum olmayanlarda buradan cikar
            pass

class Yorum:
    date_published = None
    author = None
    author_age = None
    description = None
    location = None

    def __init__(self, soup):
        divs = soup.find_all("div", recursive=False)
        content = divs[1]
        datespan = content.find("span", class_="hermes-ReviewCard-module-3fj8Y")
        authordiv = content.find("div", class_="hermes-ReviewCard-module-1-Wp3")
        authspans=authordiv.find_all("span")
        try:
            descriptiondiv = content.find("div", class_="hermes-ReviewCard-module-2dVP9")
            self.description = descriptiondiv.find("span").text.replace("\n"," ")
        except:
            self.description = ""
        self.date_published = datespan.attrs["content"]
        self.author = authspans[0].text
        self.author_age = authspans[1].text.replace("(","").replace(")","")
        self.location = authspans[2].text.replace(" - ","")

    def csv(self):
        return f"{self.date_published}|{self.author}|{self.author_age}|{self.location}|{self.description}\n"