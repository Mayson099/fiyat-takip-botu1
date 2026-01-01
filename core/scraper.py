# request bot engelini aşamadı cloudscraper daha iyi
import cloudscraper
from bs4 import BeautifulSoup
import json
import re

class PriceScraper:
    #Ürün adı ve fiyat bulma
    
    def __init__(self, config_path="config/site.json"):
        with open(config_path, "r", encoding="utf-8") as f:
            self.sites = json.load(f)
        
        
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
        )

    def detect_site(self, url):
        #Girilen Url`nin hangi site olduğunu bulmaya çalıştığı kısım


        for site in self.sites.keys():
            if site in url:
                return site
        return None

    def fetch(self, url):#site tanıma
        site = self.detect_site(url)
        if not site:#hata engelleme
            print(f"Site desteklenmiyor: {url}")
            return None
        
        rules = self.sites[site]

        try:
            
            response = self.scraper.get(url, timeout=15)
            
            
            if response.status_code != 200:
                print(f"Siteye erişilemedi. Hata Kodu: {response.status_code}")#eğer siteye girmezse hata kodu vermesi için
                return None

            soup = BeautifulSoup(response.text, "html.parser")
            
            #Ürün adını bulma
            title = None
            for selector in rules["title"]:
                tag = soup.select_one(selector)
                if tag:
                    title = tag.get_text(strip=True)
                    break

            #Fiyat Bulma
            raw_price = None
            for p in rules["price"]:
                
                
                selector = f"{p['tag']}.{p.get('class').replace(' ', '.')}"
                tag = soup.select_one(selector)
                if tag:
                    raw_price = tag.get_text(strip=True)
                    break

            if not title or not raw_price:
                
                print(f" Sayfa Başlığı: {soup.title.string if soup.title else 'Bulunamadı'}")
                return None

            #gereksiz karakterleri temizleme
            cleaned_price = re.sub(r'[^\d.,]', '', raw_price)
            if "," in cleaned_price and "." in cleaned_price:
                cleaned_price = cleaned_price.replace(".", "").replace(",", ".")
            elif "," in cleaned_price:
                cleaned_price = cleaned_price.replace(",", ".")
            
            return {
                "name": title,
                "price": float(cleaned_price),
                "url": url
            }

        except Exception as e:
            print(f"Hata: {e}")
            return None