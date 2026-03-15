import re
import operator

def matematik_iceriyor_mu(metin):
    terimler = [
        "+", "artı", "-", "eksi", "*", "çarpı",
        "/", "bölü", "=", "eşittir", "kaçtır"
    ]

    metin = metin.lower()
    return any(terim in metin for terim in terimler)


# Operatörler
ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv
}


def metni_duzenle(metin):
    metin = metin.lower()

    # Türkçe kelimeleri operatöre çevir
    metin = metin.replace("artı", "+")
    metin = metin.replace("eksi", "-")
    metin = metin.replace("çarpı", "*")
    metin = metin.replace("bölü", "/")

    return metin


def matematik_hesapla(metin):

    metin = metni_duzenle(metin)

    eslesme = re.search(r"(\d+)\s*([\+\-\*/])\s*(\d+)", metin)

    if not eslesme:
        return None

    a = int(eslesme.group(1))
    op = eslesme.group(2)
    b = int(eslesme.group(3))

    return ops[op](a, b)


if __name__ == "__main__":
    mesaj = input("Mesaj: ")

    if matematik_iceriyor_mu(mesaj):
        sonuc = matematik_hesapla(mesaj)
        print("Sonuç:", sonuc)
    else:
        print("Matematik işlemi yok.")