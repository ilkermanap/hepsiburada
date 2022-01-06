from hepsiburada import Marka
import sys

nike = Marka("nike")

urunler = nike.tum_urunler()

for sku, urun in urunler.items():
    print(sku, urun.price)
