import json
import time
import os
from core.scraper import PriceScraper
from core.mailer import Mailer

class Watcher:
    def __init__(self, email, password, product_file="config/product.json", interval=3600):
        self.scraper = PriceScraper() #sitelerden veri çekmek için scraper dosyasını başlatma 
        self.mailer = Mailer(email, password)#giriş yapan kullanıcının e-posta adresini saklar
        self.user_email = email #email saklar
        self.product_file = product_file #takip edilen ürünlerin kaydedileceği dosya 
        self.interval = interval #kontrol periyodu
        self.products = self.load_products()#program açıldığında kayıtlı ürünleri dosyadan belleğe yükleme

    def load_products(self):
        #her ihtimale karşı config klasörü yoksa klasör oluştur
        os.makedirs(os.path.dirname(self.product_file), exist_ok=True)
        try:
            #ürün dosyasını okuma modunda açar
            with open(self.product_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_products(self):
        #ürün kaydetme 
        with open(self.product_file, "w", encoding="utf-8") as f:
            json.dump(self.products, f, indent=4, ensure_ascii=False)

    def list_products(self):
        #app.py de listelemek için mevcut ürün listesini döndürür
        return self.products

    def add_product(self, url):
        #ürünün anlık bilgilerini çekme(scraper)
        item = self.scraper.fetch(url)
        if item:
            item["url"] = url
            item["last_price"] = item["price"]  
            self.products.append(item)
            self.save_products()
            print(f" ✅ Takibe Alındı: {item['name'][:30]}...")
            return True
        return False

    def remove_product_by_index(self, index):
        #sıra numarasına göre ürün silme
        if 0 <= index < len(self.products):
            removed = self.products.pop(index)
            #güncel listeyi kaydetme
            self.save_products()
            print(f" 🗑️ Silindi: {removed['name']}")

    def start(self):
        #takip edilecek ürün yoksa hata vermemesi için
        if not self.products:
            print(" ⚠️ Takip edilecek ürün yok.")
            return

        print(f" 🚀 {self.user_email} için indirim takibi başladı...")

        while True: #program kapatılana kadar fiyat kontrolü
            for product in self.products:
                data = self.scraper.fetch(product["url"])
                if data:
                    current_price = data["price"]
                    old_price = product["last_price"]

                    print(f"🔍 {data['name'][:25]}.. | Güncel: {current_price}₺ | Eski: {old_price}₺")

                    if current_price < old_price:
                        self._send_price_drop_alert(product, current_price, old_price)
                        product["last_price"] = current_price # Yeni fiyatı kaydet
                        self.save_products()
                    elif current_price > old_price:
                        product["last_price"] = current_price # Yükselişi kaydet
                        self.save_products()

            time.sleep(self.interval)

    def _send_price_drop_alert(self, product, new_price, old_price):
        fark = old_price - new_price
        #MAİL İÇERİĞİ
        mesaj = (f"📉 FİYAT DÜŞTÜ!\n\nÜrün: {product['name']}\n"
                 f"Eski Fiyat: {old_price} TL\nYeni Fiyat: {new_price} TL\n"
                 f"İndirim: {fark} TL\nLink: {product['url']}")
        
        self.mailer.send_mail(self.user_email, "📉 İndirim Yakalandı!", mesaj)
        print(f" 📧 İndirim bildirimi gönderildi!")