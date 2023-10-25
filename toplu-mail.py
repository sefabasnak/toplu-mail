# BULK MAIL APP & TOPLU MAIL UYGULAMASI
# Author: Sefa Basnak
# E-posta: info@sefabasnak.com


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# E-posta gönderme işlevi
def dosya_gonder(email, sifre, alici_email, konu, icerik, dosya_yolu=""):
    # E-posta oluşturma
    msg = MIMEMultipart()
    msg['From'] = email  # Gönderen e-posta adresi
    msg['To'] = alici_email  # Alıcı e-posta adresi
    msg['Subject'] = konu  # E-posta konusu

    # E-posta metni eklemek
    msg.attach(MIMEText(icerik, 'plain'))  # E-posta içeriği

    if dosya_yolu:
        with open(dosya_yolu, "rb") as dosya:
            part = MIMEApplication(dosya.read(), Name="dosya.pdf")  # Dosya adını dilediğiniz gibi değiştirebilirsiniz
            part['Content-Disposition'] = f'attachment; filename="{dosya_yolu}"'
            msg.attach(part)  # Dosya ekleme

    try:
        server = smtplib.SMTP('smtp.outlook.com', 587)  # Outlook için SMTP sunucusu ve portunu ayarlayın
        server.starttls()  # Güvenli bağlantı (TLS) başlatma
        server.login(email, sifre)  # Gönderen e-posta ve şifre ile giriş yapma
        server.sendmail(email, alici_email, msg.as_string())  # E-posta gönderme
        server.quit()
        print("E-posta başarıyla gönderildi.")
    except Exception as e:
        print("E-posta gönderme hatası:", str(e))

# Tekil e-posta gönderme işlevi
def tekil_mail_gonder():
    alici_email = input("Alıcı E-posta Adresini Girin: ")
    gonderici_email = input("Gönderici Mail:")
    gonderici_sifre = input("Gönderici Mail Şifresi:")
    konu = input("Konu: ")
    icerik = input("İçerik: ")
    dosya_yolu = input("Dosya Eklemek İster misiniz? Dosya yolunu girin (veya boş bırakın): ")

    dosya_gonder(gonderici_email, gonderici_sifre, alici_email, konu, icerik, dosya_yolu)

# Çoklu e-posta gönderme işlevi
def coklu_mail_gonder():
    dosya_adresleri_yolu = input("Alıcı e-posta adreslerini içeren dosyanın yolunu girin: ")
    gonderici_email = input("Gönderici Mail:")
    gonderici_sifre = input("Gönderici Mail Şifresi:")
    konu = input("Konu: ")
    icerik = input("İçerik: ")
    dosya_yolu = input("Dosya Eklemek İster misiniz? Dosya yolunu girin (veya boş bırakın): ")

    with open(dosya_adresleri_yolu, "r") as dosya:
        eposta_adresleri = dosya.readlines()  # E-posta adreslerini içeren dosyayı okuma

    for alici_email in eposta_adresleri:
        dosya_gonder(gonderici_email, gonderici_sifre, alici_email.strip(), konu, icerik, dosya_yolu)  # Her bir e-posta adresine e-posta gönderme

# Kullanıcıya tekil veya çoklu e-posta gönderme seçeneği sunma
secim = input("Tekil mail göndermek için 't', çoklu mail göndermek için 'c' girin: ").lower()

if secim == 't':
    tekil_mail_gonder()
elif secim == 'c':
    coklu_mail_gonder()
else:
    print("Geçersiz seçim. 't' veya 'c' girin.")
