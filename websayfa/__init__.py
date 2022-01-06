import requests
from bs4 import BeautifulSoup as bs
import os
import time

class Sayfa:
    def __init__(self, icerik):
        self.icerik = icerik
        self.tarih = None
        self.soup = bs(self.icerik, "html.parser")

class LokalSayfa(Sayfa):
    def __init__(self, fname):
        self.dosya = fname
        icerik = open(fname,"r").read()
        Sayfa.__init__(self, icerik)
        self.tarih = time.gmtime(os.stat(fname).st_ctime)

    def guncelle(self):
        icerik = open(self.dosya,"r").read()
        Sayfa.__init__(self, icerik)
        self.tarih = time.gmtime(os.stat(self.dosya).st_ctime)

class UzakSayfa(Sayfa):
    def __init__(self, url):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
        self.url = url
        r = requests.get(url, headers=self.headers)
        icerik = r.text
        Sayfa.__init__(self, icerik)
        self.tarih = time.localtime()

    def guncelle(self):
        r = requests.get(self.url, headers=self.headers)
        icerik = r.text
        Sayfa.__init__(self, icerik)
        self.tarih = time.localtime()