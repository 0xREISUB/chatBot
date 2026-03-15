import re


def matematik_hesapla_zincir(metin):
    metin = metin.lower()

    donusumler = {
        "artı": "+", "daha": "+", "ile": "+", "toplamı": "+", "topla": "+",
        "eksi": "-", "çıkar": "-", "farkı": "-",
        "çarpı": "*", "kere": "*", "defa": "*",
        "bölü": "/", "taksim": "/", "eşittir": "", "eder": ""
    }

    # 1. Güvenlik Kontrolü
    operator_sembolleri = ['+', '-', '*', '/']
    matematiksel_kelime_var_mi = any(kelime in metin for kelime in donusumler.keys())
    matematiksel_sembol_var_mi = any(sembol in metin for sembol in operator_sembolleri)

    if not (matematiksel_kelime_var_mi or matematiksel_sembol_var_mi):
        return None

    # Kelimeleri sembollere çevir
    for kelime, sembol in donusumler.items():
        metin = metin.replace(kelime, sembol)

    # 2. Rakamları ve Operatörleri Ayıkla
    parcalar = re.findall(r"(\d+|[\+\-\*/])", metin)

    sayi_kontrol = [p for p in parcalar if p.isdigit()]
    if len(sayi_kontrol) < 2:
        return None

    # 3. Saf İşlem Listesi Oluşturma
    saf_liste = []
    for p in parcalar:
        if p.isdigit():
            saf_liste.append(int(p))
        else:
            saf_liste.append(p)

    # --- KRİTİK DÜZELTME BURASI ---
    # Eğer operatör sonda kalmışsa (örn: [2, 2, '+']), onu araya çek
    if len(saf_liste) >= 3 and not isinstance(saf_liste[-1], int):
        op = saf_liste.pop()
        # Operatörü ilk iki sayının arasına yerleştir
        saf_liste.insert(1, op)

    # Eğer hala liste yapısı [Sayı, Operatör, Sayı...] şeklinde değilse iptal et
    if len(saf_liste) < 3 or not isinstance(saf_liste[1], str):
        return None

    # --- 4. İşlem Önceliği (Çarpma / Bölme) ---
    i = 0
    while i < len(saf_liste):
        if i < len(saf_liste) and saf_liste[i] in ["*", "/"]:
            if i > 0 and i < len(saf_liste) - 1:
                sol = saf_liste.pop(i - 1)
                op = saf_liste.pop(i - 1)
                sag = saf_liste.pop(i - 1)
                saf_liste.insert(i - 1, sol * sag if op == "*" else sol / sag)
                i -= 1
        i += 1

    # --- 5. Toplama / Çıkarma ---
    try:
        sonuc = saf_liste[0]
        for i in range(1, len(saf_liste), 2):
            if i + 1 < len(saf_liste):
                op = saf_liste[i]
                sag = saf_liste[i + 1]
                if op == "+":
                    sonuc += sag
                elif op == "-":
                    sonuc -= sag
        return sonuc
    except:
        return None