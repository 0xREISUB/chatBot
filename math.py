def matematik_iceriyor_mu(metin):
    # Kontrol edilmesini istediğin operatörler ve kelimeler
    terimler = [
        "+", "artı", "-", "eksi", "*", "çarpı",
        "/", "bölü", "=", "eşittir", "kaçtır"
    ]

    # Metni küçük harfe çevirerek kullanıcı büyük harf yazsa bile yakalamasını sağlıyoruz
    metin = metin.lower()

    # Herhangi bir terim metnin içinde geçiyorsa True, geçmiyorsa False döner
    return any(terim in metin for terim in terimler)

if __name__ == "__main__":
    print(matematik_iceriyor_mu("deneme"))