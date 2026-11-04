
from cekirdek.turna_ast import (
    Program,
    Sayi,
    Metin,
    Mantiksal,
    Bos,
    Degisken,
    Kosul,
    Dongu,
    IkiliIslem,
    TekliIslem,
    Atama,
    Cagri,
)


class Parser:

    ONCELIKLER = {
        "VEYA": 1,
        "VE": 2,
        "ESIT": 3,
        "ESIT_DEGIL": 3,
        "BUYUK": 3,
        "KUCUK": 3,
        "BUYUK_ESIT": 3,
        "KUCUK_ESIT": 3,
        "ARTI": 4,
        "EKSI": 4,
        "CARPI": 5,
        "BOL": 5,
        "TAM_BOL": 5,
        "MOD": 5,
        "US": 6,
    }

    def __init__(self, tokenlar):
        self.tokenlar = tokenlar
        self.konum = 0

    def simdiki(self):
        if self.konum >= len(self.tokenlar):
            return self.tokenlar[-1]

        return self.tokenlar[self.konum]

    def ilerle(self):
        token = self.simdiki()

        if token.tur != "DOSYA_SONU":
            self.konum += 1

        return token

    def hata(self, mesaj):
        token = self.simdiki()

        raise SyntaxError(
            f"TURNA Parser hatası: {mesaj} "
            f"(satır {token.satir}, sütun {token.sutun})"
        )

    def bekle(self, tur):
        token = self.simdiki()

        if token.tur != tur:
            self.hata(
                f"{tur} bekleniyordu, {token.tur} bulundu"
            )

        return self.ilerle()

    def bos_satirlari_gec(self):
        while self.simdiki().tur == "SATIR_SONU":
            self.ilerle()

    def baslik_sonrasi_girintiyi_bekle(self):
        self.bekle("SATIR_SONU")
        self.bos_satirlari_gec()
        self.bekle("GIRINTI_ARTTI")

    def program(self):
        ifadeler = []

        while self.simdiki().tur != "DOSYA_SONU":

            if self.simdiki().tur in (
                "SATIR_SONU",
                "GIRINTI_AZALDI",
            ):
                self.ilerle()
                continue

            onceki_konum = self.konum

            ifade = self.ifade()
            ifadeler.append(ifade)

            if self.simdiki().tur == "SATIR_SONU":
                self.ilerle()

            elif self.simdiki().tur in (
                "DOSYA_SONU",
                "GIRINTI_AZALDI",
            ):
                pass

            elif isinstance(ifade, (Kosul, Dongu)):
                # Blok ifadeleri kendi girinti kapanışını tüketir.
                # Bu nedenle sonraki komut doğrudan gelebilir.
                pass

            else:
                self.hata("Satır sonu bekleniyordu")

            if self.konum == onceki_konum:
                self.hata("Parser ilerleyemedi")

        return Program(ifadeler)

    def ifade(self):
        token = self.simdiki()

        if token.tur == "ANAHTAR_KELIME":

            if token.deger == "eğer":
                return self.kosul()

            if token.deger == "iken":
                return self.dongu()

        sol = self.islem()

        if self.simdiki().tur == "ATAMA":
            self.ilerle()

            if not isinstance(sol, Degisken):
                self.hata(
                    "Atama hedefi değişken olmalıdır"
                )

            sag = self.ifade()

            return Atama(sol.isim, sag)

        return sol

    def blok(self):
        ifadeler = []

        while self.simdiki().tur not in (
            "GIRINTI_AZALDI",
            "DOSYA_SONU",
        ):

            if self.simdiki().tur == "SATIR_SONU":
                self.ilerle()
                continue

            onceki_konum = self.konum

            ifadeler.append(self.ifade())

            if self.simdiki().tur == "SATIR_SONU":
                self.ilerle()

            if self.konum == onceki_konum:
                self.hata("Blok ayrıştırılamadı")

        if not ifadeler:
            self.hata("Kod bloğu boş olamaz")

        self.bekle("GIRINTI_AZALDI")

        return ifadeler

    def kosul(self):
        self.bekle("ANAHTAR_KELIME")

        kosul_ifadesi = self.islem()

        self.bekle("IKI_NOKTA")
        self.baslik_sonrasi_girintiyi_bekle()

        govde = self.blok()

        self.bos_satirlari_gec()

        alternatif = None
        token = self.simdiki()

        if (
            token.tur == "ANAHTAR_KELIME"
            and token.deger == "değilse"
        ):
            self.ilerle()

            self.bekle("IKI_NOKTA")
            self.baslik_sonrasi_girintiyi_bekle()

            alternatif = self.blok()

        return Kosul(
            kosul_ifadesi,
            govde,
            alternatif,
        )

    def dongu(self):
        self.bekle("ANAHTAR_KELIME")

        kosul_ifadesi = self.islem()

        self.bekle("IKI_NOKTA")
        self.baslik_sonrasi_girintiyi_bekle()

        govde = self.blok()

        return Dongu(
            kosul_ifadesi,
            govde,
        )

    def islem(self, min_oncelik=0):
        sol = self.tekli()

        while True:
            token = self.simdiki()

            operator_turu = token.tur

            if token.tur == "ANAHTAR_KELIME":
                operator_turu = {
                    "ve": "VE",
                    "veya": "VEYA",
                }.get(token.deger, "")

            oncelik = self.ONCELIKLER.get(
                operator_turu,
                -1,
            )

            if oncelik < min_oncelik:
                break

            self.ilerle()

            yeni_oncelik = (
                oncelik
                if operator_turu == "US"
                else oncelik + 1
            )

            sag = self.islem(yeni_oncelik)

            sol = IkiliIslem(
                sol,
                operator_turu,
                sag,
            )

        return sol

    def tekli(self):
        token = self.simdiki()

        if token.tur in ("ARTI", "EKSI"):
            operator = self.ilerle()
            ifade = self.tekli()

            return TekliIslem(
                operator.tur,
                ifade,
            )

        return self.temel()

    def temel(self):
        token = self.simdiki()

        if token.tur == "SAYI":
            self.ilerle()

            deger = (
                float(token.deger)
                if "." in token.deger
                else int(token.deger)
            )

            return Sayi(deger)

        if token.tur == "METIN":
            self.ilerle()
            return Metin(token.deger)

        if token.tur == "ANAHTAR_KELIME":

            if token.deger == "Doğru":
                self.ilerle()
                return Mantiksal(True)

            if token.deger == "Yanlış":
                self.ilerle()
                return Mantiksal(False)

            if token.deger == "Boş":
                self.ilerle()
                return Bos()

        if token.tur == "KIMLIK":
            self.ilerle()

            isim = token.deger

            if self.simdiki().tur == "SOL_PARANTEZ":
                self.ilerle()

                argumanlar = []

                if self.simdiki().tur != "SAG_PARANTEZ":
                    argumanlar.append(self.islem())

                    while self.simdiki().tur == "VIRGUL":
                        self.ilerle()
                        argumanlar.append(self.islem())

                self.bekle("SAG_PARANTEZ")

                return Cagri(
                    isim,
                    argumanlar,
                )

            return Degisken(isim)

        if token.tur == "SOL_PARANTEZ":
            self.ilerle()

            ifade = self.islem()

            self.bekle("SAG_PARANTEZ")

            return ifade

        self.hata("Geçerli bir ifade bekleniyordu")
