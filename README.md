# Python Fiyat Takip Botu 

Bu proje, belirlenen e-ticaret sitelerindeki (Trendyol, Amazon, Kitapyurdu, İtopya) ürün fiyatlarını otomatik olarak takip eder ve fiyat düştüğünde size e-posta ile bildirim gönderir.

# Özellikler
Otomatik Takip: Belirlenen aralıklarla ürün fiyatlarını kontrol eder.

Dinamik Bildirim: Fiyat bir önceki kontrol edilen fiyata göre düştüğü an e-posta gönderir.

Geniş Site Desteği: JSON tabanlı yapı sayesinde yeni siteler kolayca eklenebilir.

Engel Tanımaz: Cloudflare korumalarını aşmak için `cloudscraper` kullanır.


# Kurulum
1. 
Bilgisayarınızda Python'un (sürüm 3.8 veya üzeri) yüklü olduğundan emin olun.

Kontrol etmek için terminale python --version yazabilirsiniz.

2. 
Projeyi bir klasöre indirin ve terminali  bu klasörün içinde açın.

3. 
Sistemin internete bağlanması ve verileri işlemesi için gereken kütüphaneleri şu komutla yükleyin:
pip install -r requirement.txt

4.
main.py dosyasını bir metin düzenleyici (Not Defteri, VS Code vb.) ile açın ve şu satırları kendi bilgilerinizle güncelleyin:

NOT:Gmail hesabınızın normal şifresi güvenlik nedeniyle bu tür botlarda çalışmaz.

Google hesabınızda 2 Adımlı Doğrulamayı açın.

Google arama çubuğuna "Uygulama Şifreleri" yazın ve o sayfaya gidin.

Uygulama adı olarak "Fiyat Botu" yazıp şifre oluşturun.

Size verilen 16 haneli özel kodu bir yere not edin.

email = "seninmailin@gmail.com"

password = "16_haneli_özel_kod"

Her şey hazır olduktan sonra terminale şu komutu yazarak botu başlatın:

python main.py

# Nasıl Kullanılır
Ürün Ekleme: Menüden 1'i seçin ve takip etmek istediğiniz ürünün (Trendyol, Amazon, Kitapyurdu, İtopya) linkini yapıştırın.

Arka Planda Çalıştırma: Botu başlattıktan sonra bilgisayarınız açık kaldığı sürece fiyatları kontrol etmeye devam edecektir.

Durdurma: Takibi durdurmak için terminalde CTRL + C tuşlarına basmanız yeterlidir.









