import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def dosya_gonder(email, sifre, alici_email, konu, icerik, dosya_yolu=""):
    # E-posta oluşturma
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = alici_email
    msg['Subject'] = konu

    # E-posta metni eklemek
    msg.attach(MIMEText(icerik, 'plain'))

    # Dosya eklemek
    if dosya_yolu:
        with open(dosya_yolu, "rb") as dosya:
            part = MIMEApplication(dosya.read(), Name="dosya.pdf")  # Dosya adını istediğiniz gibi değiştirin
            part['Content-Disposition'] = f'attachment; filename="{dosya_yolu}"'
            msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.outlook.com', 587)  # Outlook için SMTP sunucusu ve portunu ayarlayın
        server.starttls()  # Güvenli bağlantı (TLS) başlatma
        server.login(email, sifre)
        server.sendmail(email, alici_email, msg.as_string())
        server.quit()
        print("E-posta başarıyla gönderildi.")
    except Exception as e:
        print("E-posta gönderme hatası:", str(e))

def tekil_mail_gonder():
    alici_email = input("Alıcı E-posta Adresini Girin: ")
    gonderici_email = input("Gönderici Mail:")
    gonderici_sifre = input("Gönderici Mail Şifresi:")
    konu = input("Konu: ")
    icerik = input("İçerik: ")
    dosya_yolu = input("Dosya Eklemek İster misiniz? Dosya yolunu girin (veya boş bırakın): ")

    dosya_gonder(gonderici_email, gonderici_sifre, alici_email, konu, icerik, dosya_yolu)

def coklu_mail_gonder():
    dosya_yolu = input("E-posta adreslerini içeren dosyanın yolunu girin: ")
    gonderici_email = input("Gönderici Mail:")
    gonderici_sifre = input("Gönderici Mail Şifresi:")
    konu = input("Konu: ")
    icerik = input("İçerik: ")
    dosya_yolu = input("Dosya Eklemek İster misiniz? Dosya yolunu girin (veya boş bırakın): ")

    with open(dosya_yolu, "r") as dosya:
        eposta_adresleri = dosya.readlines()

    for alici_email in eposta_adresleri:
        dosya_gonder(gonderici_email, gonderici_sifre, alici_email.strip(), konu, icerik, dosya_yolu)

# Kullanıcıya seçim yapma şansı verme
secim = input("Tekil mail göndermek için 't', çoklu mail göndermek için 'c' girin: ").lower()

if secim == 't':
    tekil_mail_gonder()
elif secim == 'c':
    coklu_mail_gonder()
else:
    print("Geçersiz seçim. 't' veya 'c' girin.")
