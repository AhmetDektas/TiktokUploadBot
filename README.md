# TiktokUploadBot
İndirmeniz gereken kütüphaneler:
pip install requests google-api-python-client google-auth google-auth-oauthlib tkinter beautifulsoup4



Tiktok Url'sini Youtube'a Video Olarak Yükleyen Bot

YouTube API kullanarak videolar yüklemek için bir OAuth 2.0 kimlik bilgisi oluşturmalısınız. Aşağıdaki adımları uygulayın:

📌 1. Google Cloud Console'a giriş yapın
Google Cloud Console adresine gidin.
Google hesabınızla giriş yapın.

📌 2. Yeni proje oluşturun
Üst menüden "Select a project" veya "Proje seçin" kısmına tıklayın.
"Yeni proje" butonuna basın.
Projeye bir isim verin (örneğin: YouTubeUploader).
"Oluştur" seçeneğine tıklayın.

📌 3. YouTube Data API'yi etkinleştirin
Arama kısmına "YouTube Data API v3" yazın ve seçin.
Açılan sayfada "Enable" veya "Etkinleştir" düğmesine tıklayın.

📌 4. OAuth 2.0 kimlik bilgileri oluşturun
Sol menüden "Kimlik Bilgileri (Credentials)" bölümüne gidin.
"Kimlik Bilgisi Oluştur (Create credentials)" → "OAuth istemci kimliği (OAuth Client ID)" seçeneğine tıklayın.
Öncelikle "Consent screen (İzin ekranı)" ayarlamanız gerekebilir. Bu ekranda uygulamanıza basitçe isim ve e-posta adresi girip kaydedin. (Harici (External) uygulama seçin.)
Sonrasında tekrar "OAuth istemci kimliği oluştur" adımına dönün.
"Masaüstü uygulaması (Desktop application)" türünü seçin.
"Oluştur" butonuna basın.

📌 5. client_secrets.json dosyasını indirin
Oluşturduktan sonra açılan pencerede "JSON'ı indir (Download JSON)" butonuna basın.
İndirilen JSON dosyasını adını client_secrets.json olarak değiştirin.
Bu dosyayı, Python scriptinizin (app.py) bulunduğu klasöre koyun.
📁 Dosya Yapınız Şöyle Olmalıdır:
📂 Uygulama Klasörünüz
├── 📄 app.py
└── 📄 client_secrets.json

Google API'yi ilk defa kullanırken, uygulamanızı yalnızca Test Kullanıcıları çalıştırabilir. Bu yüzden Google hesabınızı uygulamaya test kullanıcısı olarak eklemelisiniz:

🔸 Adımlar:
Google Cloud Console adresine girin.
Sol menüden "APIs & Services (API'ler ve Hizmetler)" → "OAuth consent screen (OAuth izin ekranı)" kısmına girin.
"Test users (Test kullanıcıları)" sekmesine tıklayın.
"ADD USERS (Kullanıcı ekle)" düğmesine basın.
Uygulamayı kullanacağınız Google hesabının e-posta adresini girin ve "SAVE (Kaydet)" tıklayın.
⚠️ Notlar:
Uygulama "Yayınlama (Publish)" işlemi yapılmadan yalnızca buraya eklediğiniz kullanıcılar giriş yapabilir.
Uygulamanızı genel kullanıma açmak isterseniz "Publish App (Uygulamayı Yayınla)" seçeneğini kullanabilirsiniz.

Kolay gelsin.
