
from cekirdek.hatalar import CalismaZamaniHatasi

from cekirdek.turna_ast import (
    Program,
    Sayi,
    Metin,
    Mantiksal,
    Bos,
    Kosul,
    Dongu,
    Degisken,
    IkiliIslem,
    TekliIslem,
    Atama,
    Cagri,
)


class Ortam:

    def __init__(self, ust=None):
        self.degiskenler = {}
        self.ust = ust

    def tanimla(self, isim, deger):
        self.degiskenler[isim] = deger

    def al(self, isim):

        if isim in self.degiskenler:
            return self.degiskenler[isim]

        if self.ust is not None:
            return self.ust.al(isim)

        raise CalismaZamaniHatasi(
            kod="TR004",
            baslik="Tanımsız değişken",
            mesaj=f"'{isim}' isimli değişken tanımlanmamış.",
            oneriler=[
                "Değişkenin adını kontrol edin.",
                "Değişkeni kullanmadan önce tanımlayın.",
            ],
        )


class Yorumlayici:

    AZAMI_DONGU = 100000

    def __init__(self):
        self.ortam = Ortam()

    def calistir(self, dugum):

        metot = getattr(
            self,
            f"calistir_{type(dugum).__name__}",
            None,
        )

        if metot is None:
            raise RuntimeError(
                f"Desteklenmeyen AST düğümü: "
                f"{type(dugum).__name__}"
            )

        return metot(dugum)

    # PROGRAM

    def calistir_Program(self, dugum):
        sonuc = None

        for ifade in dugum.ifadeler:
            sonuc = self.calistir(ifade)

        return sonuc

    # TEMEL VERİ TÜRLERİ

    def calistir_Sayi(self, dugum):
        return dugum.deger

    def calistir_Metin(self, dugum):
        return dugum.deger

    def calistir_Mantiksal(self, dugum):
        return dugum.deger

    def calistir_Bos(self, dugum):
        return None

    # DEĞİŞKENLER

    def calistir_Degisken(self, dugum):
        return self.ortam.al(dugum.isim)

    def calistir_Atama(self, dugum):
        deger = self.calistir(dugum.deger)

        self.ortam.tanimla(
            dugum.isim,
            deger,
        )

        return deger

    # KOŞULLAR

    def calistir_Kosul(self, dugum):
        sonuc = self.calistir(dugum.kosul)

        if sonuc:
            for ifade in dugum.govde:
                self.calistir(ifade)

        elif dugum.alternatif is not None:
            for ifade in dugum.alternatif:
                self.calistir(ifade)

        return None

    # DÖNGÜLER

    def calistir_Dongu(self, dugum):
        tur_sayisi = 0

        while self.calistir(dugum.kosul):

            tur_sayisi += 1

            if tur_sayisi > self.AZAMI_DONGU:
                raise RuntimeError(
                    "TURNA hatası: Döngü izin verilen "
                    "çalışma sınırını aştı."
                )

            for ifade in dugum.govde:
                self.calistir(ifade)

        return None

    # TEKLİ İŞLEMLER

    def calistir_TekliIslem(self, dugum):
        deger = self.calistir(dugum.ifade)

        if dugum.operator == "ARTI":
            return +deger

        if dugum.operator == "EKSI":
            return -deger

        raise RuntimeError(
            f"Bilinmeyen tekli işlem: {dugum.operator}"
        )

    # İKİLİ İŞLEMLER

    def calistir_IkiliIslem(self, dugum):
        sol = self.calistir(dugum.sol)
        operator = dugum.operator

        if operator == "VE":
            return bool(sol) and bool(
                self.calistir(dugum.sag)
            )

        if operator == "VEYA":
            return bool(sol) or bool(
                self.calistir(dugum.sag)
            )

        sag = self.calistir(dugum.sag)

        islemler = {
            "ARTI": lambda: sol + sag,
            "EKSI": lambda: sol - sag,
            "CARPI": lambda: sol * sag,
            "BOL": lambda: sol / sag,
            "TAM_BOL": lambda: sol // sag,
            "MOD": lambda: sol % sag,
            "US": lambda: sol ** sag,
            "ESIT": lambda: sol == sag,
            "ESIT_DEGIL": lambda: sol != sag,
            "BUYUK": lambda: sol > sag,
            "KUCUK": lambda: sol < sag,
            "BUYUK_ESIT": lambda: sol >= sag,
            "KUCUK_ESIT": lambda: sol <= sag,
        }

        if operator not in islemler:
            raise RuntimeError(
                f"Bilinmeyen işlem: {operator}"
            )

        try:
            return islemler[operator]()

        except ZeroDivisionError:
            raise CalismaZamaniHatasi(
                kod="TR009",
                baslik="Sıfıra bölme hatası",
                mesaj="Bir sayı sıfıra bölünemez.",
                oneriler=[
                    "Bölen sayının sıfır olmadığını kontrol edin.",
                ],
            )

        except TypeError:
            raise CalismaZamaniHatasi(
                kod="TR005",
                baslik="Yanlış veri türü",
                mesaj=(
                    "Bu işlem verilen veri türleriyle yapılamıyor."
                ),
                oneriler=[
                    "İşlemde kullanılan değerlerin türlerini kontrol edin.",
                ],
            )

    # İŞLEV ÇAĞRILARI

    def calistir_Cagri(self, dugum):

        if dugum.isim == "yazdır":
            argumanlar = [
                self.calistir(arguman)
                for arguman in dugum.argumanlar
            ]

            print(*argumanlar)
            return None

        raise NameError(
            f"Tanımsız işlev: '{dugum.isim}'"
        )
