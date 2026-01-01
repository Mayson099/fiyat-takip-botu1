from core.watcher import Watcher

class App:
    def __init__(self, email, password):
        self.watcher = Watcher(email, password)

    def menu(self):
        while True:#Kullanıcı çıkış yapana kadar menünün ekranda kalmasını sağlayan sonsuz döngü
            print("\n" + "="*25)
            print("  FİYAT TAKİP PROGRAMI")
            print("="*25)
            print("1) Ürün Ekle (Link Yapıştır)")
            print("2) Takip Listesi / Ürün Sil")
            print("3) Takibi Başlat")
            print("4) Çıkış")
            
            secim = input("Seçiminiz: ").strip()

            if secim == "1":
                url = input("Ürün linkini girin: ").strip()
                self.watcher.add_product(url)

            elif secim == "2":
                products = self.watcher.list_products() 
                if not products:
                    print("Takip edilen ürün bulunamadı.")
                    continue
                
                print("\n--- Takip Edilen Ürünler ---")
                for i, p in enumerate(products, 1):
                    # Listede son görülen fiyatı gösterme
                    print(f"{i}) {p['name'][:30]}... | Son Fiyat: {p['last_price']}₺")
                
                try:
                    sil_secim = int(input("\nSilmek istediğiniz no (İptal için 0): "))
                    if sil_secim > 0:
                        self.watcher.remove_product_by_index(sil_secim - 1)
                except (ValueError, IndexError):
                    print("Geçersiz numara.")

            elif secim == "3":
                try:
                    self.watcher.start()
                except KeyboardInterrupt:
                    print("\nTakip durduruldu.")

            elif secim == "4":
                break