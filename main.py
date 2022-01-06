from hepsiburada import Marka
import sys

nike = Marka("nike")

nike.sayfalar()

nike.urunler(sayfano=3)

for sku, urun in nike.urun_listesi.items():
    print(sku, urun.price)
    urun.yorumlar()
    sys.exit()
